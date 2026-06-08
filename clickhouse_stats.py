"""
ClickHouse 事件统计器（10行核心逻辑）
"""

from collections import Counter
from typing import Optional


def count_events_by_user(events: list) -> dict[str, int]:
    """按 user_id 统计事件数量"""
    return Counter(getattr(e, "user_id", e.get("user_id")) for e in events)


def get_top_users(events: list, top_n: int = 5) -> list[tuple[str, int]]:
    """获取事件数最多的前 N 个用户"""
    return count_events_by_user(events).most_common(top_n)


def get_enterprise_stats(events: list) -> Optional[dict[str, int]]:
    """按企业 ID 统计事件分布"""
    if not events:
        return None
    return Counter(getattr(e, "enterprise_id", e.get("enterprise_id")) for e in events)


if __name__ == "__main__":
    print("📊 ClickHouse 事件统计工具已就绪")
