"""
ClickHouse 查询修复示例
解决 genCodeDesc 列不存在的问题
"""

import clickhouse_connect

# 连接配置
CLIENT = clickhouse_connect.get_client(
    host='your-clickhouse-host',
    port=8123,
    username='default',
    password='your-password',
    database='otel'
)


def get_code_change_events(limit: int = 200) -> list[dict]:
    """
    获取 code_change_event 事件
    注意：先检查表结构，避免使用不存在的列
    """
    
    # 方案1：只使用确认存在的列
    query_safe = """
        SELECT 
            timestamp,
            eventCode,
            enterpriseId,
            userId,
            toolCallId
        FROM otel.events 
        WHERE eventCode = 'code_change_event' 
        ORDER BY timestamp DESC 
        LIMIT %(limit)s
    """

    # 执行安全查询
    result = CLIENT.query(query_safe, parameters={'limit': limit})
    return result.result_rows


def check_table_schema() -> None:
    """查看表结构，确认可用列"""
    schema = CLIENT.query("DESCRIBE otel.events")
    print("可用列：")
    for row in schema.result_rows:
        print(f"  - {row[0]} ({row[1]})")


if __name__ == '__main__':
    check_table_schema()
    events = get_code_change_events()
    print(f"\n获取到 {len(events)} 条事件")
