# 体验案例契约

体验案例用于把团队已验证的设计判断变成可检索知识。它和“历史稿参考”不同：体验决策阶段只读取结构化决策、约束、备选和结果，不读取最终视觉结构来直接复刻页面。

## 1. 可进入案例库的条件

案例必须满足：

- `status=verified`，由指定设计负责人/团队明确认证；
- 能回指需求或真实任务，不是脱离业务的漂亮截图；
- 关键决定有理由，至少一个关键 edge case 或失败方式；
- 如果有上线结果、研究或反馈，标明证据边界；没有也允许，但不能编造成已验证成效。

未经认证的 AI 生成稿、探索稿、历史失败稿不得进入 verified 池。

## 2. Schema

```yaml
experienceCase:
  caseId: case-xxx
  status: verified
  title: "..."
  productArea: "..."
  sourceRefs: []
  task:
    actor: "..."
    goal: "..."
    context: "..."
  constraints: []
  hardProblems: []
  decisionAxes: {}
  alternatives:
    - id: A
      model: "..."
      strengths: []
      weaknesses: []
      rejectedReason: []
  selected:
    model: "..."
    reasons: []
    tradeoffs: []
  criticalStates: []
  continuityRules: []
  outcomeEvidence:
    type: none | expert-review | usability | analytics | user-feedback
    refs: []
    finding: "..."
  reusableLessons: []
  nonReusableDetails: []
```

## 3. 检索方式

体验决策阶段按以下特征检索，而不是按页面名：

- user goal / task type；
- operation frequency / risk / reversibility；
- data volume / input complexity；
- context retention / comparison need；
- latency / interruption；
- permission / partial success 等异常形态。

默认返回 1～3 个最接近案例。相似案例不是答案：必须写出“相同点 / 不同点 / 哪些 lesson 可迁移”。

## 4. 防复制边界

Experience Planner 默认**不能读取**案例最终 Figma 截图、组件树和像素尺寸；这些材料只允许在 UX Freeze 后用于现网/视觉基线或实现对照。案例中可写抽象体验模型，例如“当前上下文内完成”“独立编辑任务空间”，不要写“使用组件 X、宽度 Y”。

若用户明确要求复刻历史方案，按授权扩大读取范围并记录。

## 5. 负例的价值

被否定方案可以记录，但必须带具体原因。优先记录：

- 为什么 Modal 不适合；
- 为什么少一步反而更差；
- 为什么需要保留上下文；
- 为什么需要 partial success；
- 为什么需要独立任务空间；
- 为什么某个看似简洁的方案在真实数据量/权限下失败。

这些负例只用于比较和评审，不自动升级为“永远禁止”。
