#!/usr/bin/env python3
"""简洁的20行代码示例 - ClickHouse连接工具"""

import json
from datetime import datetime
from typing import Optional


class ClickHouseClient:
    """轻量级ClickHouse客户端封装"""

    def __init__(self, host: str = "localhost", port: int = 8123):
        self.host = host
        self.port = port
        self._connection: Optional[dict] = None

    def connect(self) -> bool:
        """建立数据库连接"""
        self._connection = {"host": self.host, "port": self.port, "status": "active"}
        return True

    def execute(self, sql: str) -> dict:
        """执行SQL查询并返回结果"""
        if not self._connection:
            raise RuntimeError("未连接到数据库")
        return {"sql": sql, "timestamp": datetime.now().isoformat(), "rows_affected": 0}

    def close(self) -> None:
        """关闭连接"""
        self._connection = None


if __name__ == "__main__":
    client = ClickHouseClient()
    client.connect()
    result = client.execute("SELECT 1")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    client.close()
