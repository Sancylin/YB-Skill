# 体验决策契约

本契约位于 Requirement Spec 与 UX Freeze 之间。目标不是产出页面，而是先得到可审查、可比较、可复用的体验决策。未通过本阶段，不进入页面地图、Screen Spec、组件解析或视觉生成。

## 1. 核心原则

1. **先任务，后界面**：先回答用户要完成什么、在什么上下文、受什么约束，再讨论 Page / Modal / Drawer / Inline 等实现模型。
2. **不把 PRD 中的现有页面描述当成唯一答案**：若 PRD 明确指定业务结果、入口或平台约束则遵守；若只是沿用旧方案或描述实现形态，记录为 constraint/candidate，不自动视为最佳体验。
3. **不从组件库反推体验**：体验决策阶段可以读取产品事实、验证过的体验案例和任务模式，不读取组件目录来决定主流程。
4. **不机械制造备选**：只有存在会显著改变步骤、上下文保持、风险、信息密度或恢复成本的实质方案时，才比较候选。
5. **设计判断必须可复盘**：重要决定至少写清依据、牺牲、失败方式和验证方法；“更简洁/更美观/更符合习惯”不能单独作为理由。

## 2. Experience Decision Record

每个主任务至少形成一份 EDR：

```yaml
experienceDecision:
  taskId: task-xxx
  userJob:
    actor: "..."
    goal: "..."
    context: "..."
    frequency: low | medium | high | unknown
    urgency: low | medium | high | unknown
    expertise: novice | mixed | expert | unknown
  success:
    userOutcome: "..."
    businessOutcome: "..."
    completionSignal: "..."
  constraints:
    businessRules: []
    permissions: []
    dataShape: []
    deviceConstraints: []
    knownUnknowns: []
  taskModel:
    primaryTask: "..."
    secondaryTasks: []
    prerequisites: []
    nextLikelyTasks: []
  decisionAxes:
    informationVolume: low | medium | high | variable
    inputComplexity: low | medium | high | variable
    operationFrequency: low | medium | high
    reversibility: easy | costly | irreversible
    risk: low | medium | high
    contextRetention: low | medium | high
    comparisonNeed: low | medium | high
    interruptionTolerance: low | medium | high
    latency: instant | short | long | variable
  criticalMoments:
    - "用户最容易犹豫、误解、犯错或失去上下文的时刻"
  candidateModels: []
  chosenModel:
    id: "..."
    rationale: []
    tradeoffs: []
    rejectedBecause: []
  continuity:
    entryState: "..."
    preserveOnReturn: []
    cancellation: "..."
    recovery: "..."
  criticalStates: []
  evidence:
    productFacts: []
    experienceCases: []
    taskPatterns: []
  confidence: high | medium | low
  unresolved: []
```

## 3. 先做 Task Model

进入候选方案前，必须明确：

- 用户进入时已经知道什么、正在做什么、手里有什么上下文；
- 主任务是什么，哪些只是辅助任务；
- 任务频率、风险、数据量、输入复杂度、可逆性、等待时间；
- 完成后最可能继续做什么；
- 哪些信息需要跨步骤或跨页面保留；
- 用户最可能犯错、犹豫、重复操作或中断的地方。

如果上述事实不足以改变主流程，不阻塞，使用 `unknown` 并降低 confidence；如果会改变业务结果或主路径，按原有澄清规则处理。

## 4. 候选体验模型

候选描述体验结构，不描述视觉皮肤。可使用：

- 当前上下文内完成 vs 离开上下文完成；
- 单步 vs 分步；
- 直接操作 vs 先选择/预览/确认；
- 浏览优先 vs 搜索优先；
- 即时提交 vs 草稿/保存；
- 单对象 vs 批量；
- 同步反馈 vs 异步任务中心/进度；
- 自动完成 vs 用户确认。

候选比较至少使用与任务相关的 3 个轴：完成步数、上下文保持、错误成本、信息密度、认知负担、可恢复性、可扩展性、高频效率、首次理解成本、系统反馈清晰度。不要用视觉偏好代替体验取舍。

## 5. 决策优先级

发生冲突时优先级：

1. 明确业务规则与用户授权；
2. 用户完成核心任务的可达性与安全性；
3. 经过验证的产品事实与同类体验案例；
4. 当前任务模式与可解释启发式；
5. 视觉一致性与实现便利。

组件存在与否不能让一个明显更差的主流程获胜；若最佳体验需要缺口组件，交给后续复用阶梯解决。

## 6. 体验决策门禁

进入 UX Freeze 前必须成立：

- 主任务、成功结果、入口上下文明确；
- 关键业务规则、权限、数据与风险已纳入；
- 至少标出关键犹豫/错误/等待/中断点；
- 有实质替代方案时完成比较；没有则说明为何不存在有意义替代；
- chosenModel 的理由不依赖组件可用性或纯视觉偏好；
- 回退、取消、返回、恢复和完成后下一步已考虑；
- 独立 Experience Reviewer 完成任务级评审，P0～P2 清零；
- `confidence=low` 且低置信事项会改变主流程时，不得冻结。

通过后，chosenModel 才允许展开成任务流、页面/浮层地图、状态矩阵和 Screen Spec。
