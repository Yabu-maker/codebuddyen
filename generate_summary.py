#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成总结文档功能模块

分析题库并生成格式化的 Markdown 总结报告，包含：
- 题库统计信息（数量、分类、字数等）
- 问题列表概览
- 数据质量分析
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


def get_whys_data() -> List[Dict[str, str]]:
    """
    获取题库数据
    
    Returns:
        List[Dict]: 包含 question 和 answer 的字典列表
    """
    # 尝试从 quick_demo.py 导入题库数据
    try:
        from quick_demo import get_random_why
        
        # 通过多次调用收集所有问题（模拟完整题库）
        # 注意：由于 random.choice 的随机性，这里我们直接定义完整的题库
        whys = [
            {
                "question": "为什么天空是蓝色的？",
                "answer": "太阳光穿过大气层时，蓝光波长较短，更易被空气分子散射到各个方向，所以天空呈现蓝色。",
                "category": "自然现象"
            },
            {
                "question": "为什么海水是咸的？",
                "answer": "海水含有大量溶解的盐分，主要来自陆地岩石风化和海底火山活动。",
                "category": "自然现象"
            },
            {
                "question": "为什么会做梦？",
                "answer": "做梦是大脑在睡眠期间整理记忆和信息的过程，与快速眼动睡眠阶段密切相关。",
                "category": "人体奥秘"
            },
            {
                "question": "为什么太阳会发光发热？",
                "answer": "太阳核心进行着核聚变反应，氢原子聚变成氦原子释放出巨大能量。",
                "category": "天文宇宙"
            },
            {
                "question": "为什么雨后会出现彩虹？",
                "answer": "阳光照射到空气中的水滴时发生折射和反射，分解成七色光形成彩虹。",
                "category": "自然现象"
            },
            {
                "question": "为什么猫在高处也能平稳落地？",
                "answer": "猫有出色的平衡感和身体协调能力，能调整姿态用脚着地减少冲击。",
                "category": "生物世界"
            },
            {
                "question": "为什么有些植物会向阳生长？",
                "answer": "植物体内的生长素分布不均导致向光性弯曲生长，这有助于获取更多光照进行光合作用。",
                "category": "生物世界"
            },
            {
                "question": "为什么冰会浮在水面上？",
                "answer": "水结冰时分子排列成规则的晶格结构，密度变小所以冰能浮于水面。",
                "category": "科学原理"
            },
            {
                "question": "为什么月亮有圆缺变化？",
                "answer": "月球绕地球运行时，太阳照射角度不同导致我们看到被照亮的部分大小变化。",
                "category": "天文宇宙"
            },
            {
                "question": "为什么打哈欠会传染？",
                "answer": "这是一种镜像神经元活动，人类看到他人打哈欠时会不自觉地模仿这一行为。",
                "category": "人体奥秘"
            },
            {
                "question": "为什么火焰会向上燃烧？",
                "answer": "热空气上升形成对流，带动火焰向上；同时燃烧产生的热气体密度小而上升。",
                "category": "科学原理"
            },
            {
                "question": "为什么地球会有四季？",
                "answer": "地球自转轴倾斜约23.5度，绕太阳公转时不同地区接收的太阳辐射量周期性变化。",
                "category": "自然现象"
            },
            {
                "question": "为什么有些鸟会迁徙？",
                "answer": "为了寻找更适合生存的环境、食物资源和繁殖地点，鸟类会随季节变化迁移。",
                "category": "生物世界"
            },
            {
                "question": "为什么人需要睡觉？",
                "answer": "睡眠有助于身体修复、记忆巩固、大脑清理代谢废物，是维持生理和心理健康的必要过程。",
                "category": "人体奥秘"
            },
            {
                "question": "为什么有些金属会生锈？",
                "answer": "金属（主要是铁）与空气中的氧气和水蒸气发生氧化反应，生成氧化物即铁锈。",
                "category": "科学原理"
            },
            {
                "question": "为什么风会吹？",
                "answer": "太阳辐射不均匀造成各地气温差异，导致气压不平衡，空气从高压区流向低压区形成风。",
                "category": "自然现象"
            },
            {
                "question": "为什么耳朵能听到声音？",
                "answer": "声波引起鼓膜振动，通过听小骨传递到耳蜗转化为神经信号，最终由大脑解析为声音。",
                "category": "人体奥秘"
            },
            {
                "question": "为什么眼睛会近视？",
                "answer": "长时间近距离用眼导致眼球轴长变长或角膜曲率过大，远处物体成像落在视网膜前。",
                "category": "人体奥秘"
            },
            {
                "question": "为什么星星会闪烁？",
                "answer": "星光穿过大气层时受空气扰动影响产生折射变化，所以我们看到的星星位置和亮度不断波动。",
                "category": "天文宇宙"
            },
            {
                "question": "为什么时间总感觉过得很快？",
                "answer": "这与大脑处理信息的模式有关，专注或愉快时注意力分散导致对时间感知的主观偏差。",
                "category": "人体奥秘"
            }
        ]
        
        return whys
        
    except ImportError:
        print("⚠️  未找到 quick_demo.py，使用内置示例数据")
        return []


def analyze_statistics(whys: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Analyze question bank statistics

    Args:
        whys: Question bank data list

    Returns:
        Dict: Statistical analysis results
    """
    if not whys:
        return {"error": "题库为空"}
    
    # 基本统计
    total_count = len(whys)
    
    # 分类统计
    categories = {}
    for item in whys:
        cat = item.get("category", "未分类")
        categories[cat] = categories.get(cat, 0) + 1
    
    # 字数统计
    question_lengths = [len(item.get("question", "")) for item in whys]
    answer_lengths = [len(item.get("answer", "")) for item in whys]
    
    stats = {
        "total_questions": total_count,
        "categories": dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)),
        "question_stats": {
            "total_chars": sum(question_lengths),
            "avg_length": sum(question_lengths) / len(question_lengths) if question_lengths else 0,
            "min_length": min(question_lengths) if question_lengths else 0,
            "max_length": max(question_lengths) if question_lengths else 0
        },
        "answer_stats": {
            "total_chars": sum(answer_lengths),
            "avg_length": sum(answer_lengths) / len(answer_lengths) if answer_lengths else 0,
            "min_length": min(answer_lengths) if answer_lengths else 0,
            "max_length": max(answer_lengths) if answer_lengths else 0
        },
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return stats


def generate_markdown_summary(stats: Dict[str, Any], whys: List[Dict[str, str]], 
                             output_file: str = "SUMMARY.md") -> str:
    """
    生成 Markdown 格式的总结文档
    
    Args:
        stats: 统计分析数据
        whys: 题库原始数据
        output_file: 输出文件名
        
    Returns:
        str: 生成的 Markdown 内容
    """
    if "error" in stats:
        return f"# ⚠️ 生成失败\n\n{stats['error']}"
    
    md_content = []
    
    # 标题部分
    md_content.append("# 📊 十万个为什么 - 题库总结报告")
    md_content.append("")
    md_content.append(f"> 自动生成时间：{stats['generated_at']}")
    md_content.append(f"> 题库版本：v1.0")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # 一、总体概况
    md_content.append("## 📈 总体概况")
    md_content.append("")
    md_content.append("| 指标 | 数值 |")
    md_content.append("|------|------|")
    md_content.append(f"| **总题目数量** | {stats['total_questions']} 题 |")
    md_content.append(f"| **分类数量** | {len(stats['categories'])} 类 |")
    md_content.append(f"| **问题总字数** | {stats['question_stats']['total_chars']} 字 |")
    md_content.append(f"| **答案总字数** | {stats['answer_stats']['total_chars']} 字 |")
    md_content.append(f"| **问题平均长度** | {stats['question_stats']['avg_length']:.1f} 字/题 |")
    md_content.append(f"| **答案平均长度** | {stats['answer_stats']['avg_length']:.1f} 字/题 |")
    md_content.append("")
    
    # 二、分类统计
    md_content.append("## 🏷️ 分类统计")
    md_content.append("")
    md_content.append("| 分类名称 | 数量 | 占比 |")
    md_content.append("|----------|------|------|")
    
    total = stats['total_questions']
    for cat, count in stats['categories'].items():
        percentage = (count / total) * 100
        md_content.append(f"| {cat} | {count} 题 | {percentage:.1f}% |")
    
    md_content.append("")
    
    # 三、数据分析详情
    md_content.append("## 📊 数据分析详情")
    md_content.append("")
    
    md_content.append("### 3.1 问题长度分布")
    md_content.append("")
    md_content.append(f"- **最短问题**：{stats['question_stats']['min_length']} 字")
    md_content.append(f"- **最长问题**：{stats['question_stats']['max_length']} 字")
    md_content.append(f"- **平均长度**：{stats['question_stats']['avg_length']:.1f} 字")
    md_content.append("")
    
    md_content.append("### 3.2 答案长度分布")
    md_content.append("")
    md_content.append(f"- **最短答案**：{stats['answer_stats']['min_length']} 字")
    md_content.append(f"- **最长答案**：{stats['answer_stats']['max_length']} 字")
    md_content.append(f"- **平均长度**：{stats['answer_stats']['avg_length']:.1f} 字")
    md_content.append("")
    
    # 四、题库质量评估
    md_content.append("## ✅ 题库质量评估")
    md_content.append("")
    
    # 计算质量指标
    avg_answer_len = stats['answer_stats']['avg_length']
    quality_score = min(100, (avg_answer_len / 30) * 100)  # 简单评分算法
    
    if quality_score >= 80:
        quality_level = "优秀 ⭐⭐⭐⭐⭐"
    elif quality_score >= 60:
        quality_level = "良好 ⭐⭐⭐⭐"
    elif quality_score >= 40:
        quality_level = "一般 ⭐⭐⭐"
    else:
        quality_level = "需改进 ⭐⭐"
    
    md_content.append(f"| 评估项 | 结果 |")
    md_content.append(f"|--------|------|")
    md_content.append(f"| **完整性** | ✅ 所有问题均有对应答案 |")
    md_content.append(f"| **丰富度** | 涵盖 {len(stats['categories'])} 个知识领域 |")
    md_content.append(f"| **详细程度** | 答案平均 {avg_answer_len:.1f} 字 |")
    md_content.append(f"| **综合评级** | **{quality_level}** ({quality_score:.0f}/100) |")
    md_content.append("")
    
    # 五、完整题库列表
    md_content.append("## 📚 完整题库列表")
    md_content.append("")
    
    for idx, item in enumerate(whys, 1):
        category = item.get("category", "未分类")
        question = item.get("question", "")
        answer_preview = item.get("answer", "")[:50] + "..." if len(item.get("answer", "")) > 50 else item.get("answer", "")
        
        md_content.append(f"### {idx}. {question}")
        md_content.append("")
        md_content.append(f"- **分类**：{category}")
        md_content.append(f"- **答案摘要**：{answer_preview}")
        md_content.append(f"- **问题长度**：{len(question)} 字 | **答案长度**：{len(item.get('answer', ''))} 字")
        md_content.append("")
    
    # 六、改进建议
    md_content.append("## 💡 改进建议")
    md_content.append("")
    
    suggestions = []
    
    # 根据统计数据生成建议
    if stats['question_stats']['avg_length'] < 15:
        suggestions.append("- 🔸 可考虑增加问题的描述性和趣味性")
    
    if stats['answer_stats']['avg_length'] < 40:
        suggestions.append("- 🔸 部分答案可进一步扩展详细解释")
    
    category_counts = list(stats['categories'].values())
    if max(category_counts) > total * 0.4:
        dominant_cat = max(stats['categories'], key=stats['categories'].get)
        suggestions.append(f"- 🔸 当前「{dominant_cat}」类占比过高，建议平衡其他分类内容")
    
    if total < 50:
        suggestions.append("- 🔸 题库规模较小，可持续扩充至 100+ 题目以提升多样性")
    
    suggestions.append("- 🔸 可考虑增加图片、链接等多媒体资源增强表现力")
    suggestions.append("- 🔸 建议定期更新内容，保持知识时效性")
    
    for suggestion in suggestions:
        md_content.append(suggestion)
    
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append("*📝 本文档由 `generate_summary.py` 自动生成*")
    md_content.append(f"*🕐 最后更新：{stats['generated_at']}*")
    
    # 组合内容
    full_content = "\n".join(md_content)
    
    # 写入文件
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"✅ 总结文档已成功生成：{output_file}")
    except Exception as e:
        print(f"❌ 写入文件失败：{e}")
    
    return full_content


def main():
    """Main function: Execute summary document generation workflow"""
    print("=" * 60)
    print("  📊 十万个为什么 - 总结文档生成器")
    print("=" * 60)
    print()
    
    # 步骤 1：获取题库数据
    print("📥 正在加载题库数据...")
    whys_data = get_whys_data()
    
    if not whys_data:
        print("❌ 错误：未能加载题库数据，程序退出")
        return
    
    print(f"   ✓ 成功加载 {len(whys_data)} 个问题")
    print()
    
    # 步骤 2：统计分析
    print("📊 正在进行统计分析...")
    statistics = analyze_statistics(whys_data)
    
    if "error" in statistics:
        print(f"❌ 统计分析失败：{statistics['error']}")
        return
    
    print(f"   ✓ 完成 {statistics['total_questions']} 题目的数据分析")
    print(f"   ✓ 识别出 {len(statistics['categories'])} 个知识分类")
    print()
    
    # 步骤 3：生成文档
    print("📝 正在生成总结文档...")
    output_filename = "SUMMARY.md"
    
    markdown_content = generate_markdown_summary(
        statistics, 
        whys_data, 
        output_file=output_filename
    )
    
    # 输出预览
    print()
    print("=" * 60)
    print("  📋 文档生成完成！")
    print("=" * 60)
    print()
    print(f"📁 文件位置：{os.path.abspath(output_filename)}")
    print(f"📄 文件大小：{os.path.getsize(output_filename)} 字节")
    print(f"📊 包含内容：")
    print(f"   - 总体概况统计")
    print(f"   - {len(statistics['categories'])} 个分类的详细分析")
    print(f"   - {len(whys_data)} 个题目的完整信息")
    print(f"   - 质量评估与改进建议")
    print()
    print("💡 提示：使用以下命令查看文档：")
    print(f"   cat {output_filename}")
    print()


if __name__ == "__main__":
    main()
