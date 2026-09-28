from flask import Blueprint, jsonify, request
import os
import sqlite3
import time

analytics_bp = Blueprint('analytics', __name__, url_prefix='')

def _db_path(app):
    path = os.path.join(app.instance_path, 'analytics.db')
    os.makedirs(app.instance_path, exist_ok=True)
    return path

def _get_conn(app):
    return sqlite3.connect(_db_path(app), check_same_thread=False)

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
    conn = _get_conn(current_app)
    cur = conn.cursor()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr or '')
    ua = request.headers.get('User-Agent', '')
    path = request.json.get('path', '/') if request.is_json else '/'
    now = time.time()
    date = time.strftime('%Y-%m-%d', time.localtime(now))
    cur.execute(
        "INSERT INTO visits (date, ip, ua, path, ts) VALUES (?, ?, ?, ?, ?)",
        (date, ip, ua, path, now)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'}), 200

@analytics_bp.route('/analytics/stats', methods=['GET'])
def analytics_stats():
    from flask import current_app
    conn = _get_conn(current_app)
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
    conn.close()
    return jsonify({
        'date': date,
        'daily_visits': daily_visits,
        'daily_unique_visitors': daily_unique,
        'total_visits': total_visits,
        'total_unique_visitors': total_unique
    }), 200
