# 证据化评审清单

以下布局/视觉模式仅在现场团队规范可追溯且场景命中时作为 team-rule；无依据时为可解释调整的 heuristic，不以本文措辞独立阻断。工具限制、实例身份保护和需求覆盖仍为硬性不变量。规则分类见 [采集与验证契约](capture-and-validation.md)。
清单先验收视觉和组件调用，再抽查记录。记录格式问题优先补记录，不要为过脚本改坏可见稿。

## 完成优先级

1. **视觉**：截图上的层级、对比、示意填充、文案和主任务是否成立。
2. **组件**：槽位是否用了现场搜到的正式件，变体和 description 是否用对；没有手绘冒充、detach、换字体。
3. **记录**：能追溯上面两件事即可。缺白名单路径或快照多字段不是视觉缺陷。

## 分级

- **P0**：主任务阻断、错误操作语义、无恢复/退出、改错目标或破坏规范源。
- **P1**：明显体验/视觉/系统不一致、缺状态、非法实例写入、缺现场证据、仿制正式资产、隐瞒 degraded。
- **P2**：有依据、可复现的局部体验或规范缺陷，如局部截断、同类间距不一致、次要反馈不清楚。
- **建议项**：不违反需求/规范且无已证实体验缺陷的偏好或范围外建议；必须写理由，不能将成立的 P2 降级。

P0～P2 全部复验关闭才能交付；必需 degraded、blocked、unknown、未审或待复验同样阻断。唯一完成条件见 [完成门禁](orchestration-and-completion-gates.md)。

## A0. Experience Decision

- [ ] Requirement 与 Solution 已分离；AI 派生的 Page / Modal / Drawer / 页面地图没有冒充原文需求。
- [ ] UX/UI Freeze 后已扫描原输入文件页面，并检查组件库 `【AI参考案例】Template` 与用户参考；命中页面已按 `direct-reuse / adapt-reuse / reference-only` 决策，直接/改造复用现有页面时对应 unit 有匹配 `liveBaseline`，且没有覆盖 PRD、改变写入目标或替代现场组件解析。
- [ ] 每个主任务都有 user job、进入上下文、成功结果、关键约束和 decision axes。
- [ ] 已指出用户最容易犹豫、犯错、等待、中断或失去上下文的关键时刻。
- [ ] 有实质替代方案时完成比较；没有则说明不存在有意义替代，而不是机械制造弱方案。
- [ ] chosen model 的理由主要来自任务结果、上下文、风险、恢复、效率，而不是“组件库里有”或“看起来更简洁”。
- [ ] verified 体验案例只迁移可复用 lesson，并明确当前任务的差异；没有直接复刻历史视觉/组件结构。
- [ ] 返回、取消、中断、失败、完成后下一步的连续性已考虑。
- [ ] 独立 Experience Reviewer 已按 [自适应执行分级](adaptive-execution-profiles.md) 复核当前 profile；`happy-path` 必跑，其余 simulation 按风险触发。Full 仍跑 happy path + first-use + error + interrupt + post-success，并补适用专项。

## A. PRD 与 UX

- [ ] 目标、用户、范围和成功标准清楚。
- [ ] 任务流从入口到结果和退出闭环。
- [ ] 必要状态、异常和恢复路径完整；空 / 错 / 弱网状态有 `surfaceLevel`（`page` / `overlay` / `in-stream`）。
- [ ] 已读完整份典型交互模式；`when` 命中条目的 `stay` / `never` 成立；未命中的模式没有被套用。
- [ ] 对话生成中弱网仍停在输出或思考中，并允许延迟非阻断轻提示；没有在完成态之后改成整页空。
- [ ] 主操作和信息优先级明确；字段语义不重复。
- [ ] 内容真实匹配业务，不是组件示例或元话术。MCP 无法加载字体时按 [云端字体配置](team-font-configuration.md) 恢复，未恢复时记录 `degraded` 和恢复入口，不能因此伪造完成；必需内容未写入仍阻断整体交付。
- [ ] 可访问性、内容增长和设备适配已考虑。
- [ ] 实现未反向改变冻结需求。

## B. UI 与装配

- [ ] 每个槽位角色、尺寸策略、滚动、overlay 和适配符合 Screen Spec。
- [ ] 复用现网已有屏幕/模式时，Screen Spec 的尺寸、间距和状态来自 `liveBaseline`；逐元素 `live/ours/delta` 在容差内或已写授权理由。
- [ ] 每个可见区域都做过 overflow/裁切检查：后代没有被中间容器或视口裁掉，`scrollWidth` 没有超出可滚动容器。
- [ ] 内容脚本 → Figma 文案 → Demo 渲染逐项对齐；没有用默认说明或占位文案冒充。
- [ ] 每个本次新建/修改布局宿主都有方向、水平/垂直对齐、分布及理由；对照主/交叉轴读回实际参数与几何，不因工具默认左上而放过，也不强制改成居中；每个 visible unit 有 [布局几何门禁](layout-quality-gate.md) 的结构化 `layout-geometry` 证据。
- [ ] 检查 padding 内可用空间、父级 Hug / 子级 Fill、SPACE_BETWEEN 与 gap、混合子组锚点；短/长内容、子项数量和目标尺寸变化后仍成立。
- [ ] 容器位置、文本框内部对齐、基线分别验证；换行时行内与多行分布分别验证。正式实例内部问题不靠越权改后代解决。description 要求的示意填充处理不算越权，未处理则不能过。
- [ ] 最终可见边界正确；中间容器未误裁后代效果。
- [ ] 逐个检查本次自建布局包装的 fills / strokes / effects 为空，覆盖所有层级和容器用途；不得仅凭白底截图看不出色块就判通过。检查范围不包含正式实例内部的批量清空。
- [ ] Screen Spec 有 `canvasRole` 和表面区分理由；检查透明祖先背后的实际背景、主题解析值与正常阅读尺度截图。递归检查每个独立表面与承载背景、同层兄弟的区分是否符合职责，不能只核验某类组件或第一层；正式组件使用合法属性且保留 token。
- [ ] 不能因为存在非空 strokes / effects 就判定边界有效；验证描边可见、投影未被裁切，未盲目叠加多种分隔手段。
- [ ] 页面级空/弱网没有出现在内容流；流内失败没有被整页空态替换。
- [ ] 页面级空/错/弱网缺省相对整机画板垂直居中；没有在顶栏下方剩余列里居中导致偏下。
- [ ] 浮层内容很少时没有顶到分档或最大高度。
- [ ] 已有表面的纯布局槽无多余底色；独立子表面有职责与规范依据。
- [ ] 业务屏或模块根不是 Group；结构关系是 auto-layout，不是绝对坐标拼装。
- [ ] 圆角表单/列表旁的标题或底注已判断是否内收：左对齐但对齐内边内容，而不是贴外框；Markdown 正文除外。
- [ ] 贴边壳层（顶栏、长按条、锁定操作条、键盘、Tab）铺满画布，与画布或同屏已铺满的条齐平；页面边距只包内容卡片/文本框。没有把左右 padding 加在「内容 + 贴边底栏」的同一个父级上，底栏两侧不能露出页面背景或蒙层。
- [ ] 需要系统输入法升起的屏已用正式系统输入法键盘主组件；没有手绘键帽，也没有用键盘图标或外部系统库代替。未命中 `system-ime-keyboard` 的页不要硬套。
- [ ] 内容流内部间距示意层没有被删掉；示意填充已按 description 处理。
- [ ] 主题、对比、密度和层级符合现场设计系统。
- [ ] 正式实例保持自身尺寸约束和内部规范。
- [ ] 无异常固定高度、碰撞、散落节点或默认命名。

布局层无依据视觉、表面层级丢失、有依据的对齐或分布错误按影响列 P1/P2，须修复复验；不能当作纯偏好跳过。

## C. 组件与写入

- [ ] 每个实现槽位都有 requirementsBasis、searchAttempts、逐候选 gateDecision/理由和 description 摘录。
- [ ] 每个槽位 `reuseLadder` 走完 `formal-instance → compose → gap`，没有跳级；首次生成就成立，不靠用户提醒才改用正式件。
- [ ] 纯布局宿主记 `compose`（`layoutOnly` + `layoutReason`），没有被写成 `gap` 手绘；有视觉表面的宿主来自正式件。
- [ ] gap 的 `inventory.complete=true`、`eligibleIds = libraryCatalog.ids`、`eligibleIds = scannedIds ∪ exclusions`，有 `composeTrials` 证明组合失败，无证据不足候选；`formal-instance` / `compose` 记 `inventoryCoverage=not-required`。review-observed 未实例化或判 gap。
- [ ] 规范说明、禁止实例化或文档画板资产未被 `createInstance`。
- [ ] 根节点与槽位职责对应，来自现场证据选中的正式资产或已登记 gap。
- [ ] 复合结构的 chosenAssets、childSlots 和 slotBindings 均完成递归解析。
- [ ] 实例从当次 live key 新建，无 clone/detach。
- [ ] 写入落在公开属性、合法子槽位、外层布局和 description 要求的示意填充。白名单是抽查日志，缺路径不是缺陷。
- [ ] pre/post 能核对组件身份；名称和布局变化不要求路径级白名单。
- [ ] blocked 未画成功态；degraded 有具体恢复入口；illegal-mutation 已回滚。

## D. 评审顺序

- [ ] 先截图评 UX，再截图评 UI，最后读节点评系统。
- [ ] 没有因先看到组件名而忽略可见问题。
- [ ] 没有因“里面有 Instance”而跳过区域根节点核验。
- [ ] 评审结论包含截图和节点证据。
- [ ] 全量复评已刷新范围内所有区域根资产与递归 slotBindings；抽样评审明确 coverage 且未宣称全量清零。

## E. 交互原型

- [ ] 与 Figma 共用冻结包、槽位语义和内容脚本。
- [ ] 已解析槽位映射到正式封装和合法 props。
- [ ] 每个 chosen asset 都有原型映射证据（`Demo Mapping Evidence`），manifest 身份和属性 schema 已验证。
- [ ] 页面层未重画已有正式资产。
- [ ] 主要状态和恢复路径可操作。
- [ ] 关键视觉对照当次现场截图/description。
- [ ] `deliverable=both` 时 Figma 与 Demo 的结构、层级、元素和文案对齐，有当次两端截图和差异对照。
- [ ] `both` 的交互等级按端记录：Figma 静态状态屏 `design`，可点走查 Demo `executed`；不能把 Figma 伪造成 `executed`。
- [ ] 只读报告可以 `verdict=issues`，但每条 P0～P2 finding 都回指问题台账并附当次截图。
- [ ] 工程自身验收通过；实现缺陷没有回写成工作流配方。

## 输出

```text
P0 / P1 / P2
位置或槽位 | 截图/节点/description 证据 | 问题 | 修复 | 状态

Degraded
位置或节点 | 目标 | 当前 | 缺失能力 | 人工接管
```

## F. 运行闭环

- [ ] 原始需求/附件与需求 ID 双向追溯；AI 推导没有伪装原文。
- [ ] 独立评审维度与 `executionProfile` 一致：Fast plan requirements+experience、final ui；Standard plan requirements+experience+ux、final ux+ui；Full plan requirements+experience+ux+ui、final ux+ui+system。reviewerId 不得等于 designerId；同阶段同时存在 UX/UI 时必须不同评审者；profile 升级后刷新受影响评审。
- [ ] 盲审者没有继承历史结论；材料包与待审版本一致。
- [ ] 独立评审来自无历史继承的上下文，能力证据记录隔离机制与评审者身份；`findings` 是含位置和证据的结构化数组，P0/P1/P2 finding 带 `issueId` 且与台账 severity 一致。
- [ ] 每个可见 unit 的 visual 检查引用当次截图，没有用写入日志、导出链接或人工摘要代替。
- [ ] 原始评审发现全部进入 issues，合并/误报/关闭有证据，不删除原报告。
- [ ] 修复由不同于修复者的复验者关闭；当前版本证据覆盖影响范围。
- [ ] 所有必需字体、文本、Slot 等能力预检通过；无必需降级。
- [ ] node-audit 有结构化反查证据（`scanned` 非空、`unregistered`/`misclassified` 为空），从节点反查未登记自建及重复本地组件，不能仅检查登记表或只写 pass。
- [ ] 有状态转换和实际任务记录；设计层验证未冒充真实走查。
- [ ] 对所有交付物运行 deliver 门禁，报告说明覆盖、版本与证据边界。


## 表单校验时机

命中信息收集场景时按 [form-validation-timing](interaction-patterns.md#form-validation-timing) 检查截图与状态转换：初始、部分填写、失焦空值和清空状态没有提前报错，主操作置灰禁用；提交条件满足后按钮可用；真实错误统一走 Toast。确认组件下方没有行内错误文案或空的错误占位，错误提示没有把下方元素顶开、没有改变间距，默认稿与错误稿的几何一致。检查复用组件是否残留 Error 变体/示例文案，Demo 禁用按钮是否仍能经回车提交、错误是否只通过 Toast 出现。提前红字、行内错误顶开布局、混入默认稿的错误态或仅视觉禁用按 P2（阻断主任务时 P1）修复复验；不可用日志中“通过”代替截图/交互证据。
