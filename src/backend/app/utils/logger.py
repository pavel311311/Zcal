"""
日志配置模块
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(name: str = "zcal", level: str = "INFO") -> logging.Logger:
    """
    设置应用日志器
    
    Args:
        name: 日志器名称
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        配置好的日志器实例
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 创建格式化器
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（可选）
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"无法创建文件日志处理器: {e}")
    
    return logger

def log_request(logger: logging.Logger, request_data: dict, endpoint: str):
    """记录API请求日志"""
    logger.info(f"API请求 [{endpoint}]: {request_data}")

def log_response(logger: logging.Logger, response_data: dict, endpoint: str, duration: float = None):
    """记录API响应日志"""
    duration_str = f" (耗时: {duration:.3f}s)" if duration else ""
    logger.info(f"API响应 [{endpoint}]{duration_str}: {response_data}")

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """记录错误日志"""
    logger.error(f"错误 [{context}]: {type(error).__name__}: {str(error)}", exc_info=True)

def log_calculation(logger: logging.Logger, model_type: str, params: dict, result: dict):
    """记录计算过程日志"""
    logger.info(f"计算 [{model_type}] 参数: {params} -> 结果: {result}")