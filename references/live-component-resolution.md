# 现场组件解析

本文件规定 AI 如何通过 Figma MCP 实时选择组件。组件用途、属性、组合和视觉规范只能来自当次现场 description 与真实节点。

## 1. 输入门禁

开始前必须有：

- `requirementsBasis`：`reviewed-plan`、`user-confirmed` 或 `review-observed`；
- 已分解的职责树、状态、关系与 unitIds；没有匹配父组件仍要查子职责；
- `referenceReview.status=reviewed`；原输入文件页面已扫描，页面级 `direct-reuse / adapt-reuse / reference-only / new` 决策已登记；直接或改造复用现有业务页面时对应 `liveBaseline` 已建立；
- 目标文件、写入范围和元宝移动端配置；
- 当次 `get_libraries` 精确匹配出的发布库；run 顶层 `liveLibrary` 记录 `libraryKey`、版本或指纹、观察时间和本次观察到的 `ids`，每个 `chosenAssets` 必须是该 `ids` 成员。

`reviewed-plan` 来自通过 plan 门禁的 PRD/UX/UI 方案；用户明确确认也不能替代门禁。可用于选型，写入另需授权和 build 门禁。`user-confirmed` 另需当前方案用户确认的原文证据，仍需 plan 门禁。`review-observed` 用于缺少历史选型证据的旧稿只读评审（有 PRD 时另做原文需求覆盖检查）：槽位职责只能来自截图和节点可见事实，不允许实例化、判定 gap 或推测业务意图；无法证明时为 blocked。

## 2. 每个槽位的解析协议

### 语义定义（`Semantic`）

把槽位职责改写为一个自然语言搜索意图。禁止先写组件名、Variant、key 或 token。

### 设计系统搜索（`Discover`）

调用 `search_design_system`，限制到当次 libraryKey。一个 query 只表达一个意图。结果只是候选：语义不相关时必须被描述门禁淘汰。

调用与分页以 [工具适配契约](tool-adaptation-contract.md) 为准。一个 query 表达一个已识别意图；使用当前工具允许的批量方式，不能机械换同义词重试或违反工具规则并行单 query。截断/失败意图不记为已执行。

若 `referenceReview` 命中现有页面或组件库 Template，先把页面结构和槽位映射到当前 unit，作为组合蓝图。直接复用的页面只调整流程位置或连线；改造复用的页面按已登记 changeScope 修改内容、状态、外层布局、导航或适配。来源页中出现的组件只提供候选线索，仍需逐个核对当次 `liveLibrary` 身份并通过描述门禁。页面复用不得跳过 `formal-instance → compose → gap` 阶梯，也不得把源页面实例直接当作成品复制。

旧页面中的实例不因“旧”自动废弃：key、description、公开属性和保护字段仍有效且属于当次 `liveLibrary` 时可以直接复用；身份失效、资产未发布或状态不满足时才替换/升级。反向也不成立：来自旧页面不自动通过身份门禁。

搜索结果只是候选。空结果不证明缺口；可读取允许的当次发布目录及对应页面，定位后仍检查 description、父级、属性和状态。未发布资产不能当作 gap。删除固定搜索次数门槛，gap 由目录覆盖和合法组合能力证明。

简单槽位发现完整覆盖候选后可停止；复杂槽位先比较已发现的高相关候选的用途直接性、完整状态、合法组合与最小自建，再记录选择理由。无需为已有完整方案的槽位做全量盘点。

### 全库盘点兜底（`Inventory Fallback`）

搜索无法确认匹配且工具允许目录读取时，执行只读现场盘点：

1. 枚举规范源全部顶层页面名称和 ID，并标出可证明属于当前发布库的 eligible pages；
2. 先扫描相关页面；完整覆盖且完成必要候选比较后可停止；
3. 若仍无通过候选，且当前目标是证明 `gap`，才继续扫描其余 eligible pages 中所有正式根 Component Set/Component；
4. 对每个根读取 description、公开属性、owning parent、内部件状态、Slot 关系、资产状态和 libraryKey 归属，再执行描述门禁；
5. 记录槽位 `inventory` 的 `eligibleIds / scannedIds / exclusions / complete`；`pagesEligible / pagesScanned / rootsScanned` 可作进度备注，但不是门禁字段。

盘点结果只属于本次会话，不写入 Skill 或手工缓存。

槽位 `inventory` 是门禁读取的字段；`inventoryCoverage` 只是文档里的口径标签：

- 结论为 `formal-instance` 或 `compose`：记 `inventoryCoverage=not-required`，不写 `inventory`，不要求 `complete`；
- 结论为 `gap`：只有要证明 gap 时才必须完成全量 Inventory，且 `inventory.complete=true`、`eligibleIds = libraryCatalog.ids`、`eligibleIds = scannedIds ∪ exclusions`，没有 `blocked-insufficient-evidence` 候选，全部未选候选均为 `reject-proven-mismatch`；
- 要证明 gap 但无法完成全量盘点时只能 `blocked`，不能假装 gap。

`libraryCatalog` 从当前 `list_file_components_for_code_connect` 原始结果建立。当前接口只接受 fileKey，声明仅返回已发布组件；没有 cursor 参数，不要求 published 字段重复表达接口保证。仅实际接口支持时分页。输出截断或无法确认完整性时 complete=false 并恢复，禁止把缓存冒充现场目录。详见 [工具适配契约](tool-adaptation-contract.md)。空库同样保留原始空结果。

只有通过 plan 门禁的 reviewed-plan 或 user-confirmed 才可判定 gap。

### 现场读取（`Live Read`）

对候选读取：

- Component/Component Set description；
- 相关 Variant description；
- `componentPropertyDefinitions`；
- owning parent、是否内部件；
- Slot / Instance Swap / 子组件关系；
- 当前 key 和资产状态。

### 描述门禁（`Description Gate`）

顺序固定：

1. 若【用途】或【禁用方式】标明这是规范说明、禁止实例化或文档画板，而不是可放入产品界面的 UI，记 `reject-proven-mismatch`，禁止 `createInstance`；
2. 【用途】是否匹配槽位职责；
3. 宿主：槽位的 `scene` / `layoutRelationship` / `surfaceLevel` 必须被候选【适用场景】和【禁用方式】覆盖。用途匹配但禁用了当前宿主（落地页、浮层、内容流）→ `reject-proven-mismatch`。「不要用 A 代替本组件」不是允许把本组件嵌进 A；
4. 【禁用方式】是否排除当前场景；
5. 【使用规则】要求怎样组合、排序或选择属性；实例化后必须执行的示意填充处理写在这里时，属于交付写入，不是可选项；
6. 【属性/状态】是否存在目标组合；
7. 目标状态、适配和内容边界是否完整。

description 不足、父级不明、资产非正式或组合无法证明时为 `blocked`，不得用名称、截图相似度、本地 key 表或 Code Connect 猜测。

每个候选的 `gateDecision` 只有三种：

- `pass`：证据足以覆盖槽位；
- `reject-proven-mismatch`：用途、禁用边界或已完整验证的必要状态、属性组合、内容/适配能力不匹配；
- `blocked-insufficient-evidence`：description、父级、属性、状态或组合证据不足。

证据不足不能记作“淘汰”，也不能帮助证明 gap。

### 递归组合（`Recursive Composition`）

先按需求职责树主动解析；父组件 description 要求 Slot、子组件或复合结构时，再把每个未解析子职责变成新槽位，递归执行语义定义 → 搜索 → 现场读取 → 门禁。禁止把整颗复杂 UI 直接做成一个自建组件来跳过子槽位解析。

组合是缺口的必经前置：没有单个正式件覆盖时，必须先尝试用**正式子件 + 纯布局宿主**组合，记录 `composeTrials`（host、parts、为什么仍缺能力）；只有组合也证明不成立，才允许 `gap`。纯布局宿主只负责方向、对齐、分布和尺寸，自身不得有填充/描边/效果；有视觉表面的宿主不能靠“组合”绕过正式件。

### 解析结论（`Resolve`）

每个槽位必须按固定阶梯记录 `reuseLadder`，顺序不可跳级：

- `formal-instance`：一个正式组件完整覆盖，记 `matched`；不成立记 `exhausted` 并写理由；
- `compose`：多个已解析正式实例组合。必须记 `layoutOnly`：`true` 时写 `layoutReason`，宿主是纯布局层；`false` 时 `chosenAssets` 必须指向正式宿主。`formal-instance` 未耗尽不能进入 `compose`；
- `gap`：现场证明库不覆盖**且**无法组合。必须同时满足：前两级均 `exhausted`、`composeTrials` 至少一条 `reject-proven-mismatch`、`libraryCatalog` 完整、`inventory` 由该目录锚定；缺一即 `blocked`；
- `blocked`：证据不足，停止该槽位。

`reuseLadder` 只有最后一步 `matched`，且 `matched.step` 必须等于 `resolution`。只写了 `gap` 没写前两级尝试，或只写一次搜索就判 `gap`，记录不成立。

## 3. 执行策略

- 先解析主任务路径和高风险槽位，再解析次要状态。
- 职责、状态和内容类型相同的槽位**默认批量搜索**；只有候选冲突、状态边界不同或工具明确不支持批量时拆开。先列齐本轮语义 intents 再发请求，避免逐槽位往返。
- 完成必要候选比较后立即停止 Discover；完整候选通过 description gate 后不再为“证明最优”搜索同义词。Inventory 仅在证明 gap 时进入。
- 全量 Inventory 只在要证明 gap 时分批执行并持续记录 pages/roots 进度；不能因会话成本把未完成盘点写成 gap；同一发布指纹下复用原始目录，逐槽位保留适用性分类。
- 同一会话、同一 live libraryKey 下，key 与 description/属性指纹一致的候选证据必须优先复用，避免重复 Live Read；独立复评仍刷新。
- 父子槽位形成依赖图；检测到循环或无法证明终点时为 blocked。
- 不能为了降低工作量跳过子槽位证据。Fast 若解析出真实 gap 或复杂非 layout-only compose，先按 [自适应执行分级](adaptive-execution-profiles.md) 升级，再继续昂贵盘点/创建。

## 4. 实例化

保存 [evidence-contract.md](evidence-contract.md) 的槽位证据（`Slot Evidence`）后，按交付物分别实例化：

```text
Figma：import by live key → createInstance → setProperties(现场验证的公开属性)
      → resolve child Slots → apply allowed outer layout
Demo：chosenLiveKey → manifestAssetKey → generatedExport
      → 用合法公开 props 渲染 → 页面层只做业务组合与交互状态
both：两端共用同一份槽位证据、reuseLadder、libraryCatalog 和内容脚本，
      先各自验证映射/实例，再做 parity 对照
```

Figma 不得 clone 业务实例、detach、改正式库主组件或从缓存 key 直接实例化。Demo 不得只按名称猜组件、不得在页面层重画已有正式封装；manifest 身份或 props schema 不一致时记组件库同步问题（`syncMismatch`）或 `blocked`，不能用自绘绕过。两端都不能跳过复用阶梯：一端省步骤不等于另一端可以省。

只有通过 plan/build 门禁且获写入授权的 reviewed-plan 或 user-confirmed 才允许进入本节；`review-observed` 到此停止。规范说明、禁止实例化或文档画板资产不得进入本节。

## 5. 缺口

`gap` 先记录缺失能力、`composeTrials` 组合失败证据、完整 `libraryCatalog` 和已复用的正式子槽位，再按 [missing-component-creation.md](missing-component-creation.md) 创建。自建部分只能覆盖真正缺失的内容或行为；宿主若只是布局职责，改记 `compose`，不建本地组件。

## 6. 输出

每个进入实现的槽位必须有：

- requirementsBasis；
- searchAttempts（`source: semantic | published-name | page-routed | inventory`）；
- 所有被读取候选的三值 gateDecision/理由和 description 摘录；
- `reuseLadder`（`formal-instance → compose → gap`，只有最后一步 matched）；
- `compose` 的 `layoutOnly` / `layoutReason` 或正式宿主 `chosenAssets`；
- `gap` 的 `composeTrials`、`libraryCatalog` 锚定与 `inventory`；
- 结论与允许/禁止写入。

`inventory` 仅 `gap` 必填，字段为 `complete / eligibleIds / scannedIds / exclusions / evidenceRefs`；`pagesEligible / pagesScanned / rootsScanned` 只作进度备注。未完成证据的槽位不得进入实现。

## 7. 覆盖、继承与发布一致性

get_libraries 若返回组织库分页，遍历到定位目标或证明列表结束；同名身份歧义不能任选。search_design_system 的分页/截断/检索覆盖不能凭名称推断，按当前工具实际能力记录。

根 Component Set、相关 Variant、内部件及父级描述共同判定。父级明确适用于子级的规则可继承，记录来源；子级合法的更窄限制必须遵守。关键语义缺失/冲突才 blocked，不以是否重复出现固定中文标题判定。不得因继承就假定实际不存在的属性组合可用。

Inventory 分全局目录及候选详情两层。run 顶层 `liveLibrary` 保存本次会话观察到的发布库身份与资产 `ids`；证明 `gap` 时另用 `libraryCatalog` 保存当次发布库的 `libraryKey`（须与 `liveLibrary` 一致）、`complete=true` 和完整 `ids`；槽位 `inventory` 的 eligibleIds 必须覆盖该目录全集，不能自造范围。对允许发布库的完整资产范围记录 eligibleIds / scannedIds / exclusions 和原始目录证据；排除要有可靠的职责/类型事实，不仅页名。用途未知且可能相关的资产继续补证据。所有 eligible 资产都必须被检查或有证据排除，scannedIds 每一项都要有候选判定或排除记录；相关候选全部可证明不覆盖；另有 `composeTrials` 证明合法组合仍缺何能力。无法获得完整范围时不能写 complete=true；无法完成全量盘点时只能 `blocked`，不以成本或工具缺分页假装 gap。

libraryKey 只证明身份；记录当前发布版本或相关资产指纹与时间。源文件未发布草稿不能替代已发布描述/属性；无法对齐则 blocked。独立复评必须刷新，并检查所用资产和基础规范是否变化；变化时使受影响解析、实现和评审失效。

布局 Frame、一次性内容不是可复用交互缺口。formal-instance 的内部子槽位只要本次实际修改，也必须有 childSlots / slotBindings；不能仅 compose 才记录。依赖循环阻断；登记到 [运行契约](run-record-format.md)。

## 8. 完整性

gap 的 eligibleIds 必须等于 libraryCatalog.ids，且 scannedIds 与 exclusions.id 不相交，其并集等于完整目录。全量分类不要求深读所有无关资产；可靠的类型/职责事实可批量排除但必须展开 ID。未知用途不能排除。组合证据证明在已核对公开接口和职责范围内缺失哪项能力，不宣称穷举所有排列。
