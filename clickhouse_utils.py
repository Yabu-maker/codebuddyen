"""
ClickHouse 辅助工具（约30行示例代码）
"""
import typing
from datetime import datetime

def build_safe_select(json_col: str, key: str, alias: str) -> str:
    """构造 JSONExtractString 选择列（假设 json_col 存在）"""
    return f"JSONExtractString({json_col}, '{key}') AS {alias}"

def build_events_query(event_code: str, limit: int = 200, extra_select: typing.Optional[str] = None) -> str:
    """构造事件查询 SQL，避免直接引用未知列"""
    parts = [
        "SELECT",
        "  timestamp,",
        "  eventCode,",
        "  enterpriseId,",
        "  userId,",
        "  toolCallId" + ("," if extra_select else ""),
    ]
    if extra_select:
        parts.append(f"  {extra_select}")
    parts.extend([
        "FROM otel.events",
        f"WHERE eventCode = '{event_code}'",
        "ORDER BY timestamp DESC",
        f"LIMIT {limit}",
    ])
    return "\n".join(parts)

def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec='seconds') + "Z"

if __name__ == '__main__':
    # 示例：仅在确认列存在时传入 extra_select
    extra = build_safe_select('genCodeDesc', 'reportScope', 'scope')
    print(build_events_query('code_change_event', 100, extra_select=extra))
    print("generated at", now_iso())
