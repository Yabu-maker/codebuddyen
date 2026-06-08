import React, { useMemo, useState } from "react";

type WhyQuestionCardProps = {
  title?: string;
  questions?: string[];
};

const DEFAULT_QUESTIONS = [
  "为什么天空是蓝色的？",
  "为什么海水是咸的？",
  "为什么雨后会出现彩虹？",
  "为什么星星会闪烁？",
  "为什么月亮会有阴晴圆缺？",
  "为什么冰会浮在水面上？",
  "为什么风会吹？",
  "为什么火焰会向上燃烧？",
  "为什么人需要睡觉？",
  "为什么打哈欠会传染？",
  "为什么有些鸟要迁徙？",
  "为什么眼睛会近视？",
  "为什么耳朵能听到声音？",
  "为什么地球会有四季？",
  "为什么有些金属会生锈？",
  "为什么猫常常喜欢晒太阳？",
  "为什么树叶会变黄再落下？",
  "为什么植物会向光生长？",
  "为什么声音在空气中能传播？",
  "为什么时间会让人感觉忽快忽慢？"
];

function getRandomIndex(length: number, exclude: number): number {
  if (length <= 1) return 0;

  let next = exclude;
  while (next === exclude) {
    next = Math.floor(Math.random() * length);
  }
  return next;
}

export function WhyQuestionCard({
  title = "十万个为什么",
  questions = DEFAULT_QUESTIONS
}: WhyQuestionCardProps) {
  const safeQuestions = useMemo(
    () => (questions.length > 0 ? questions : DEFAULT_QUESTIONS),
    [questions]
  );

  const [index, setIndex] = useState(() => Math.floor(Math.random() * safeQuestions.length));
  const [fade, setFade] = useState(true);

  const randomNext = () => {
    setFade(false);

    window.setTimeout(() => {
      setIndex((prev) => getRandomIndex(safeQuestions.length, prev));
      setFade(true);
    }, 120);
  };

  return (
    <div
      style={{
        width: "100%",
        maxWidth: 520,
        margin: "0 auto",
        borderRadius: 20,
        padding: 24,
        color: "#0f172a",
        background:
          "linear-gradient(145deg, rgba(255,255,255,0.95), rgba(245,247,255,0.95))",
        boxShadow: "0 12px 36px rgba(15, 23, 42, 0.14)",
        border: "1px solid rgba(148, 163, 184, 0.2)",
        backdropFilter: "blur(6px)"
      }}
    >
      <div
        style={{
          display: "inline-flex",
          fontSize: 12,
          letterSpacing: 0.8,
          color: "#475569",
          background: "rgba(148, 163, 184, 0.16)",
          borderRadius: 999,
          padding: "6px 10px",
          marginBottom: 12
        }}
      >
        MAGIC GENERATED IDEA
      </div>

      <h2
        style={{
          margin: 0,
          fontSize: 28,
          lineHeight: 1.2,
          color: "#111827"
        }}
      >
        {title}
      </h2>

      <p
        style={{
          marginTop: 8,
          marginBottom: 18,
          color: "#475569",
          fontSize: 14
        }}
      >
        每次点击按钮，随机出现一个新的“为什么”。
      </p>

      <div
        style={{
          minHeight: 88,
          borderRadius: 14,
          padding: "16px 14px",
          background: "#ffffff",
          border: "1px solid rgba(148, 163, 184, 0.22)",
          display: "flex",
          alignItems: "center"
        }}
      >
        <span
          style={{
            fontSize: 22,
            lineHeight: 1.5,
            color: "#0f172a",
            opacity: fade ? 1 : 0,
            transform: fade ? "translateY(0px)" : "translateY(4px)",
            transition: "opacity 160ms ease, transform 160ms ease"
          }}
        >
          {safeQuestions[index]}
        </span>
      </div>

      <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
        <button
          onClick={randomNext}
          style={{
            cursor: "pointer",
            border: 0,
            borderRadius: 12,
            padding: "10px 16px",
            color: "#ffffff",
            fontWeight: 600,
            background: "linear-gradient(135deg, #2563eb, #7c3aed)",
            boxShadow: "0 6px 18px rgba(59, 130, 246, 0.35)"
          }}
        >
          再问一个为什么
        </button>
      </div>
    </div>
  );
}

export default WhyQuestionCard;
