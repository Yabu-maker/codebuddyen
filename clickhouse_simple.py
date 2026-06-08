"""
ClickHouse 安全查询器 - 优化版
特性: 参数化防注入、完整类型注解、异常处理、结构化返回
"""
from __future__ import annotations

import typing
from dataclasses import dataclass

import clickhouse_connect


@dataclass(frozen=True)
class ClickHouseConfig:
    host: str = "localhost"
    port: int = 8123
    username: str = "default"
    password: str = ""
    database: str = "otel"


@dataclass(slots=True)
class EventRow:
    timestamp: str
    event_code: str
    enterprise_id: str
    user_id: str
    tool_call_id: str


class SafeClickHouseClient:
    """封装 ClickHouse 连接，支持参数化查询防止 SQL 注入"""

    def __init__(self, config: ClickHouseConfig | None = None):
        self._config = config or ClickHouseConfig()
        self._client = clickhouse_connect.get_client(
            host=self._config.host,
            port=self._config.port,
            username=self._config.username,
            password=self._config.password,
            database=self._config.database,
        )

    def query_events(self, event_code: str, limit: int = 200) -> list[EventRow]:
        """参数化查询事件，自动映射到结构化对象"""
        sql = """
            SELECT timestamp, eventCode, enterpriseId, userId, toolCallId
            FROM otel.events
            WHERE eventCode = %(event_code)s
            ORDER BY timestamp DESC
            LIMIT %(limit)s
        """
        try:
            result = self._client.query(
                sql, parameters={"event_code": event_code, "limit": limit}
            )
            return [EventRow(*row) for row in result.result_rows]
        except Exception as exc:
            raise RuntimeError(f"ClickHouse 查询失败: {exc}") from exc

    def check_connection(self) -> bool:
        """检测 ClickHouse 连接是否可用"""
        return self._client.ping()

    def get_table_columns(self, table: str = "otel.events") -> list[str]:
        """获取指定表的列名列表"""
        sql = f"DESCRIBE TABLE {table}"
        result = self._client.query(sql)
        return [str(row[0]) for row in result.result_rows]


def main() -> None:
    client = SafeClickHouseClient()
    rows = client.query_events("code_change_event", limit=100)
    print(f"✅ 查询到 {len(rows)} 条记录")
    if rows:
        print(f"📌 最新一条时间戳: {rows[0].timestamp}")


if __name__ == "__main__":
    main()
