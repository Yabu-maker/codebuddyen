# 十万个为什么卡片组件（Magic 生成版）说明

## 1. 背景

该组件通过 **Magic MCP（21st）** 获取卡片组件灵感后，整理为一个可直接复用的 React 单文件组件：`why_question_card.tsx`。

## 2. 组件目标

- 展示一个“为什么”问题。
- 每次点击按钮时随机切换到另一个问题。
- 卡片风格现代化，适合直接嵌入页面。

## 3. 文件位置

- 组件文件：`why_question_card.tsx`
- 说明文档：`README_why_question_card.md`

## 4. 主要实现点

### 4.1 随机问题逻辑

- 使用 `getRandomIndex(length, exclude)` 随机索引。
- 通过 `exclude` 保证下一次问题尽量不与当前重复（当题库大于 1 时）。

### 4.2 数据来源

- 内置 `DEFAULT_QUESTIONS` 作为默认题库。
- 组件支持通过 `questions` 属性传入自定义题库。
- 若传入空数组，自动回退到默认题库，避免空白渲染。

### 4.3 交互动画

- 点击“再问一个为什么”时：
  1. 先将文本透明度降低（淡出）；
  2. 约 120ms 后切换问题；
  3. 文本恢复可见（淡入）。
- 通过内联 `transition` 实现轻量动画，无需额外动画库。

## 5. 组件 API

`WhyQuestionCardProps`：

- `title?: string`：卡片标题，默认 `"十万个为什么"`。
- `questions?: string[]`：自定义问题列表。

## 6. 使用示例

```tsx
import WhyQuestionCard from "./why_question_card";

export default function App() {
  return <WhyQuestionCard />;
}
```

传入自定义题库：

```tsx
<WhyQuestionCard
  title="科学小问答"
  questions={[
    "为什么云会下雨？",
    "为什么水会蒸发？",
    "为什么会有白天和黑夜？"
  ]}
/>
```

## 7. 可扩展建议

- 将题库改为从 JSON 文件或后端接口加载。
- 增加“收藏问题”“上一题/下一题”功能。
- 增加主题切换（浅色/深色）与响应式样式。
