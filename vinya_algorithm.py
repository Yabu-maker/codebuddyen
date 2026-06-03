# vinya_algorithm.py - 优化后的排序算法实现
from typing import List
import time
from datetime import datetime

def bubble_sort(arr: List[int]) -> List[int]:
    """
    冒泡排序算法（优化版）
    时间复杂度: O(n^2)（最坏情况）
    空间复杂度: O(1)
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def quick_sort(arr: List[int]) -> List[int]:
    """
    快速排序算法（优化版）
    时间复杂度: O(n log n) 平均情况
    空间复杂度: O(log n)
    """
    if len(arr) <= 10:
        return insertion_sort(arr)
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def insertion_sort(arr: List[int]) -> List[int]:
    """
    插入排序算法（用于小数组优化）
    时间复杂度: O(n^2)
    空间复杂度: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def save_to_file(filename: str, content: str):
    """
    将内容保存到文件
    :param filename: 文件名
    :param content: 要保存的内容
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_test_data() -> List[int]:
    """
    生成测试数据
    :return: 测试数据列表
    """
    return [64, 34, 25, 12, 22, 11, 90]

if __name__ == "__main__":
    # 测试数据
    data = generate_test_data()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 执行排序
    bubble_result = bubble_sort(data.copy())
    quick_result = quick_sort(data.copy())
    
    # 打印结果
    print("原始数组:", data)
    print("冒泡排序结果:", bubble_result)
    print("快速排序结果:", quick_result)
    
    # 保存结果到文件
    result_content = f"原始数组: {data}\n冒泡排序结果: {bubble_result}\n快速排序结果: {quick_result}"
    save_to_file(f"sort_results_{timestamp}.txt", result_content)
    print(f"排序结果已保存到: sort_results_{timestamp}.txt")

python vinya_stress_test.py > vinya_10k_lines.py

# TCSAS_ENV = 'private_test'  # 私有化2.0测试环境
# TCSAS_ENV = 'private_overall_test'  # 私有化2.0 DPO升级测试环境
# TCSAS_ENV = 'private_upgrade_test'  # 私有化2.0原地升级
TCSAS_ENV = 'test_env'    # 公有云测试环境
# TCSAS_ENV = 'pre_env'     # 预发环境
# TCSAS_ENV = 'sg_env'      # 新加坡现网环境
# TCSAS_ENV = 'hk_env'      # 香港现网环境
# TCSAS_ENV = 'fk_env'      # 法兰克福现网环境
# TCSAS_ENV = 'spl_env'     # 圣保罗现网环境
# TCSAS_ENV = 'jkt_env'     # 雅加达标准节点
# TCSAS_ENV = 'test_openapi_env'    # 公有云测试环境（OpenAPI）
# TCSAS_ENV = 'jkt_ts_env'     # 雅加达ts节点
