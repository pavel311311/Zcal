from flask import Blueprint, jsonify, request
import os
import sqlite3
import time
import threading
from collections import deque

analytics_bp = Blueprint('analytics', __name__, url_prefix='')

# 【健壮性增强】写限频：同一 IP 每 60s 最多 N 次，超过则返回 status: ok 但不落库
# 限频仅作用于写接口（/analytics/hit），读接口（/analytics/stats）不受影响
WRITE_RATE_LIMIT_WINDOW_SEC = 60
WRITE_RATE_LIMIT_MAX_HITS = 30

# 进程内限频状态：ip -> 最近 hit 时间戳列表
_rate_lock = threading.Lock()
_rate_buckets = {}


def _db_path(app):
    path = os.path.join(app.instance_path, 'analytics.db')
    os.makedirs(app.instance_path, exist_ok=True)
    return path


def _get_conn(app):
    """获取 SQLite 连接：开启 WAL 与 busy_timeout，缓解并发锁库"""
    conn = sqlite3.connect(_db_path(app), check_same_thread=False, timeout=5.0)
    try:
        # WAL 模式提升并发读写性能，避免写阻塞读
        conn.execute("PRAGMA journal_mode=WAL")
        # 设置 busy_timeout 让 SQLite 在库被锁时等待一段时间再抛错
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA synchronous=NORMAL")
    except Exception:
        # pragma 设置失败不影响主流程，继续使用普通连接
        pass
    return conn


def _parse_client_ip():
    """解析客户端 IP：取 X-Forwarded-For 的第一个；回退 remote_addr"""
    xff = request.headers.get('X-Forwarded-For')
    if xff:
        # XFF 可能为 "ip1, ip2, ip3"，取最左侧（最近的代理客户端）
        first = xff.split(',', 1)[0].strip()
        if first:
            return first
    return request.remote_addr or ''


def _check_and_record_write_rate(ip: str) -> bool:
    """
    检查并记录一次写入。返回 True 表示允许写入；False 表示被限频。
    内存中维护滑动窗口（最近 N 秒内的 hit 时间戳）。
    """
    now = time.time()
    window_start = now - WRITE_RATE_LIMIT_WINDOW_SEC
    with _rate_lock:
        bucket = _rate_buckets.get(ip)
        if bucket is None:
            bucket = deque()
            _rate_buckets[ip] = bucket
        # 清理窗口外的时间戳
        while bucket and bucket[0] < window_start:
            bucket.popleft()
        if len(bucket) >= WRITE_RATE_LIMIT_MAX_HITS:
            return False
        bucket.append(now)
        return True


def init_analytics(app):
    conn = _get_conn(app)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            ip TEXT,
            ua TEXT,
            path TEXT,
            ts REAL
        )
    """)
    conn.commit()
    conn.close()


@analytics_bp.route('/analytics/hit', methods=['POST'])
def analytics_hit():
    from flask import current_app
    ip = _parse_client_ip()

    # 【健壮性增强】超过限频则直接返回 ok，但不落库
    if not _check_and_record_write_rate(ip):
        return jsonify({'status': 'ok'}), 200

    conn = _get_conn(current_app)
    try:
        cur = conn.cursor()
        ua = request.headers.get('User-Agent', '')
        path = request.json.get('path', '/') if request.is_json else '/'
        now = time.time()
        date = time.strftime('%Y-%m-%d', time.localtime(now))
        cur.execute(
            "INSERT INTO visits (date, ip, ua, path, ts) VALUES (?, ?, ?, ?, ?)",
            (date, ip, ua, path, now)
        )
        conn.commit()
    finally:
        conn.close()
    return jsonify({'status': 'ok'}), 200


@analytics_bp.route('/analytics/stats', methods=['GET'])
def analytics_stats():
    from flask import current_app
    conn = _get_conn(current_app)
    try:
        cur = conn.cursor()
        date = request.args.get('date') or time.strftime('%Y-%m-%d', time.localtime())
        cur.execute("SELECT COUNT(*) FROM visits WHERE date = ?", (date,))
        daily_visits = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT ip) FROM visits WHERE date = ?", (date,))
        daily_unique = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM visits")
        total_visits = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT ip) FROM visits")
        total_unique = cur.fetchone()[0]
    finally:
        conn.close()
    return jsonify({
        'date': date,
        'daily_visits': daily_visits,
        'daily_unique_visitors': daily_unique,
        'total_visits': total_visits,
        'total_unique_visitors': total_unique
    }), 200
