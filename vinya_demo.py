# vinya_demo.py - 30行Python实用脚本
import csv
from datetime import datetime

# 生成测试数据
def generate_sample_data():
    data = []
    for i in range(1, 6):
        record = {
            "id": i,
            "name": f"User_{i}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "value": i * 10
        }
        data.append(record)
    return data

# 保存数据到CSV
def save_to_csv(filename, data):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"数据已保存到 {filename}")

# 数据分析示例
def analyze_data(data):
    total = sum(item['value'] for item in data)
    avg = total / len(data)
    return {"total": total, "average": avg}

if __name__ == "__main__":
    print("=== Vinya数据处理演示 ===")
    
    # 生成并保存数据
    sample_data = generate_sample_data()
    save_to_csv("vinya_data.csv", sample_data)
    
    # 数据分析
    stats = analyze_data(sample_data)
    print(f"\n数据分析结果:")
    print(f"总值: {stats['total']}")
    print(f"平均值: {stats['average']:.2f}")
    
    # 当前系统信息
    print("\n擦股恶臭·的午餐被我·:")
    print(f"当前时擦股恶臭·的午餐被我间: {datetime.now()}")
    print(f"脚本名称擦股恶臭·的午餐被我: {__file__}")
    
    print("\n=== 程序擦股恶臭·的午餐被我执行完成 ===")