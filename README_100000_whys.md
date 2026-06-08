# 十万个为什么 (100,000 Whys)

> 每次运行，随机抛出一个"为什么"，让代码执行多一点趣味。

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 功能目标

在脚本执行时，随机展示一个"为什么"科普问题，以《十万个为什么》风格为终端输出增添知识性和趣味性。

---

## 快速开始

```bash
python quick_demo.py
```

### 示例输出

```
==================================================
  🌟 十万个 why — 每日一问 🌟
==================================================

❓ 为什么天空是蓝色的？

  太阳光穿过大气层时，蓝光波长较短，
  更容易被空气分子散射到各个方向，
  所以我们看到的天空呈现蓝色。

==================================================
```

每次运行都会从题库中随机抽取一个问题（含答案），可能重复也可能不同。

---

## 实现架构

```
quick_demo.py
├── whys (list)          # 问题库数据结构
│   ├── question: str    # 问题文本
│   └── answer: str      # 答案文本
│
├── get_random_why()     # 核心函数：随机抽取
│   ├── random.choice()  # 随机选择算法
│   └── return dict      # 返回 {question, answer}
│
└── main()               # 入口：格式化输出
    ├── 分隔线装饰
    ├── 调用 get_random_why()
    └── print 输出
```

### 核心代码逻辑

```python
import random

def get_random_why():
    """从内置问题库中随机返回一个问题及答案。"""
    whys = [
        {
            "question": "为什么天空是蓝色的？",
            "answer": "太阳光穿过大气层时，蓝光波长较短，更易被散射。"
        },
        {
            "question": "为什么星星会闪烁？",
            "answer": "星光经过大气层时受空气扰动影响，产生折射变化。"
        },
        # ... 更多条目
    ]
    return random.choice(whys)

# 主程序调用
if __name__ == "__main__":
    result = get_random_why()
    print(f"❓ {result['question']}\n\n  {result['answer']}")
```

---

## 设计决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 数据存储 | 内存中的 Python list | 零依赖、启动快、适合小规模题库 |
| 随机算法 | `random.choice()` | 标准库、O(1) 时间复杂度 |
| 输出格式 | 终端纯文本 + Unicode 装饰 | 兼容所有终端、无需额外依赖 |
| 问题结构 | dict (question + answer) | 结构清晰、易于扩展字段 |

### 为什么不选择其他方案？

- **不使用 JSON/文件存储**：当前题库规模小（~几十条），内存足够；外部文件增加 I/O 开销和部署复杂度
- **不使用数据库**：单机脚本场景，SQLite/MySQL 属于过度工程
- **不实现去重逻辑**：简单随机抽样允许自然重复，符合"每日一问"的随机感；去重需要维护状态，增加复杂度

---

## 当前题库分类

| 分类 | 数量 | 示例问题 |
|------|------|----------|
| 🌍 自然现象 | ~10+ | 天空为什么是蓝色的？ |
| 🔬 科学原理 | ~8+ | 铁为什么会生锈？ |
| 🧑‍🔬 人体奥秘 | ~6+ | 人为什么会打哈欠？ |
| 🌌 天文宇宙 | ~5+ | 月亮为什么会变形状？ |
| 🐾 生物世界 | ~5+ | 蜜蜂为什么会跳舞？ |

> 具体条目见 `quick_demo.py` 中 `whys` 列表定义。

---

## 扩展指南

### 方式一：直接追加条目（推荐新手）

在 `quick_demo.py` 的 `whys` 列表中追加字典：

```python
{
    "question": "你的新问题？",
    "answer": "对应的答案解释。"
}
```

### 方式二：外部 JSON 文件（推荐大量条目）

创建 `whys.json`：

```json
[
  {"q": "为什么...", "a": "因为..."},
  {"q": "怎么...", "a": "通过..."}
]
```

修改 `get_random_why()` 从文件加载：

```python
import json

def get_random_why(filepath="whys.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        whys = json.load(f)
    return random.choice(whys)
```

### 方式三：支持主题分类

```python
def get_random_why(category=None):
    """可选按分类抽取。"""
    all_whys = load_whys()
    if category:
        filtered = [w for w in all_whys if w["category"] == category]
        return random.choice(filtered)
    return random.choice(all_whys)

# 用法
get_random_why("nature")   # 只抽自然类
get_random_why()           # 全类随机
```

### 方式四：避免连续重复

```python
_last_index = None

def get_random_why_no_repeat():
    global _last_index
    while True:
        idx = random.randrange(len(whys))
        if idx != _last_index:
            _last_index = idx
            return whys[idx]
```

---

## 后续优化路线图

- [x] 基础随机问答功能
- [ ] 外部 JSON / YAML 文件加载题库
- [ ] 连续去重机制（不与上次相同）
- [ ] 主题分类标签系统
- [ ] CLI 参数支持 (`--category nature --count 3`)
- [ ] i18n 多语言切换（中英日）
- [ ] Web API 版本（Flask/FastAPI）
- [ ] 每日定时推送（微信/邮件/TG Bot）
- [ ] 用户贡献题库（GitHub Issues / PR）

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `quick_demo.py` | 主程序，包含 `get_random_why()` 函数和问题库 |
| `test_test.py` | 单元测试文件（如有） |

---

## License

MIT — 自由使用、修改和分发。
