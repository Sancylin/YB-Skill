# PRD 到设计冻结契约

本契约把 PRD、自然语言需求或现有问题转换成三层明确产物：**Requirement Spec → Experience Decision → UX/UI Freeze**。核心要求是先把“要解决什么”与“准备怎么做”分开，避免文字需求阶段过早锚定页面结构。

## 1. Requirement Spec：只冻结问题，不冻结解法

先按 [输入分流](input-routing.md) 判定输入类型。文字需求先产出 Requirement Spec/PRD；上传 PRD 默认原文直读。此阶段允许读取业务事实、设备与能力边界，但**禁止因为已有组件、历史页面或通用 UI 习惯提前决定 Page / Modal / Drawer、页面地图和具体布局**。

必须明确：

- 业务目标、目标用户、使用场景、用户要完成的任务与成功标准；
- 范围内 / 范围外；
- 平台、设备类别、交付物与可访问性要求；
- 数据来源、内容模型、权限、业务规则、异常和依赖；
- 用户进入任务前已有的上下文与完成后需要得到的结果；
- PRD 中的硬约束、假设和仍需确认的问题。

Requirement Spec 可以包含用户旅程中的事实步骤，例如“从聊天详情进入分享”，但不能把 AI 自己选择的“新开页面/底部弹层/三步向导”写成需求事实。PRD 明确指定某种实现时，记录为 explicit constraint，并在体验阶段判断它是否是必须遵守的业务约束还是可讨论的既有方案。

缺少会改变业务结果或主流程的信息时，只问必要问题；不为装饰偏好阻塞。

## 2. Experience Decision：先做任务级体验判断

进入任务流、页面/浮层地图和 Screen Spec 前，必须读取并执行：

- [体验决策契约](experience/experience-decision-contract.md)
- [产品体验模型](experience/product-experience-model.md)
- [任务体验模式](experience/task-experience-patterns.md)
- 若存在 verified 案例，按 [体验案例契约](experience/experience-case-contract.md) 检索 1～3 个最相似案例

输出 Experience Decision Record，明确 user job、上下文、决策轴、关键犹豫/错误/等待点、候选体验模型、chosen model、连续性和关键状态。

这一阶段：

- 可以决定“当前上下文内完成 / 独立任务空间 / 分步 / 批量 / 异步”等体验模型；
- 不解析 Figma 组件；
- 不允许用“组件库里正好有这个组件”作为主流程理由；
- 不默认读取 verified case 的最终截图、组件树和像素结构；
- 有实质替代方案时做 pairwise/取舍；没有则说明为什么不存在有意义替代。

由与 Designer 隔离的 Experience Reviewer 按 [任务模拟评审](experience/task-simulation-review.md) 审定。P0～P2 清零后才能进入 UX Freeze。

## 3. UX Freeze：把体验决策展开成可执行结构

基于已审定的 chosen model 输出：

- 入口 → 操作 → 结果 → 退出的任务流；
- 页面/浮层地图与导航关系；
- 默认、加载、空、错误、禁用、无网络、成功、重试等必要状态；
- 每个空 / 错 / 弱网状态的 `surfaceLevel`：`page` / `overlay` / `in-stream`；
- 每个状态的恢复路径、返回/取消行为、状态保留；
- 字段语义、校验、内容优先级和真实文案方向；
- 关键任务之后的下一步连续性；
- chosen model 与 Requirement / EDR 的追溯关系。

此时读完整份 [典型交互模式](interaction-patterns.md)，只把 `when` 命中的 UI/state `patternId` 写入状态矩阵。对话生成中弱网用 `in-stream-weak-network`，落地页弱网用 `page-weak-network`，落地页空状态用 `page-empty`；圆角表单/列表旁有标题或底注时用 `rounded-group-caption-inset`。未命中的不套用。

注意：`任务体验模式` 用于体验决策；`典型交互模式` 用于已确定方案后的状态/UI 表达，两者职责不同。

## 4. UI Freeze：抽象槽位与 Screen Spec

创建抽象槽位，不写具体组件名：

```text
slotId:
  responsibility:
  scene:
  states:
  contentType:
  interaction:
  layoutRelationship:
  accessibility:
```

Screen Spec 只写：

- 容器角色和层级；
- `canvasRole`：`grouped` 或 `primary`；
- 内容柱、滚动层、页面边距、贴边壳层关系；
- 布局宿主的方向、水平/垂直对齐目标及理由、紧凑/两端分布、固定/自适应/填充策略；
- 滚动、溢出、浮层和安全区；
- 主题、设备适配和内容增长；
- 视觉权重与语义角色；各层表面与承载背景的区分理由；纯布局层明确无视觉。

具体尺寸若 PRD 未给出，先扫描目标文件和正式模板，不从体验案例或历史视觉稿猜。

## 5. 内容脚本

- 使用真实业务语义，不写 lorem 或组件说明书话术；
- 组件默认内容不作为业务文案来源；
- Figma 与 Demo 共用同一内容模型；
- 文案必须覆盖关键决策点、错误、恢复、部分成功、长任务等体验状态，而不是只覆盖 happy path。

## 6. 冻结门禁

Plan 门禁前至少包含：

```text
Requirement Spec
Experience Decision Record
Experience Review / Task Simulation
任务流 / 页面地图
状态矩阵 / 恢复路径 / 连续性
命中的 task pattern 与 UI pattern
抽象槽位
Screen Spec
内容脚本
验收标准
重要取舍
未决问题
```

硬性要求：

- Requirement Spec 中 AI 派生的页面方案不得冒充 explicit requirement；
- Experience Decision 必须先于页面地图和组件解析；
- 有实质候选时必须说明取舍，不机械制造被否决方案；
- Experience Reviewer 与 Designer 隔离；
- `confidence=low` 且低置信项会改变主流程时不得冻结；
- 通过 plan 后才解析正式组件。

结构变化重新内部审定；改变业务结果的未知选择才询问用户。

## 7. 原文追溯、职责拆解与冲突

读取主文档、必要附件、表格、图示与被引用材料；记录 sourceId、位置、版本、readStatus、evidenceRefs。必要材料无法读取时不能宣称需求完整。

每项需求记录 requirementId / sourceIds / 原文位置 / statement / origin（explicit、derived、team）/ targets / acceptance。推导出的 Experience Decision 与 UI 决定不能冒充原文；分别记录依据、影响、恢复策略。

在组件候选搜索前按用户任务拆职责树，包括内容、操作、恢复、容器和可变状态。不存在匹配父组件也继续解析子职责；页面布局不是天然缺口。

评审职责：

- **Requirements**：原文、业务规则、漏项、越界、成功标准；
- **Experience**：任务模型、上下文、决策轴、候选取舍、连续性、关键失败点；
- **UX**：入口、步骤、恢复、退出、状态保留、反馈和认知负担；
- **UI/内容**：真实文案、层级、密度、主次操作、内容增长、主题与适配；
- **系统可行性**：选型后确认能按正式规范实现；如影响体验方案则回 Experience/plan review。

不同角色结论冲突回查业务与证据，不靠投票；无足够事实则记录未决。组件可用性和实现便利不得静默覆盖已经成立的体验理由。
