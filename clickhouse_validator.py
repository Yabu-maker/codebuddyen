"""
ClickHouse 数据校验器（10行核心逻辑）
"""

import re
from typing import Optional


def validate_event_code(code: str) -> bool:
    """校验事件码格式（字母+下划线，3-50字符）"""
    return bool(re.match(r"^[a-zA-Z_][\w]{2,49}$", code))


def validate_limit(limit: int) -> bool:
    """校验查询限制参数（1-10000）"""
    return isinstance(limit, int) and 1 <= limit <= 10000


def safe_validate_query(event_code: str, limit: int) -> Optional[str]:
    """综合校验查询参数，返回错误信息或 None"""
    if not validate_event_code(event_code):
        return f"❌ 无效的事件码: {event_code}"
    if not validate_limit(limit):
        return f"❌ 无效的limit值: {limit} (需在1-10000之间)"
    return None
