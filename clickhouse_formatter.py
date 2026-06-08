"""
ClickHouse 查询结果格式化器（10行核心逻辑）
"""

import json
from datetime import datetime


def format_events_to_json(events: list, filepath: str = "events_output.json") -> str:
    """将查询结果格式化为可读 JSON 并保存到文件"""
    output = [
        {
            "timestamp": row.timestamp,
            "event_code": row.event_code,
            "enterprise_id": row.enterprise_id,
            "user_id": row.user_id,
        }
        for row in events
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    return f"✅ 已导出 {len(output)} 条记录到 {filepath}"


if __name__ == "__main__":
    print(format_events_to_json([], "demo.json"))
