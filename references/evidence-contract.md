# 设计证据契约

## 事实、判断与记录

运行使用 [运行记录格式](run-record-format.md) 与 `scripts/validate-run.py`。原始工具结果、规范正文、截图和独立报告作为独立文件登记路径、sha256、kind、provenance；结论引用 evidenceRefs。不要把人工摘要或历史产物标成当次 captured。

脚本校验登记覆盖、内容/几何/集合运算及身份差异；它不能仅靠记录证明远端行为发生。它不给视觉打分，也不能鉴定伪造证据。完成以截图和组件调用为准；记录跟不上时先补记录，不要为了过脚本改坏可见稿。字段名不是证据。此仓库拦不住直接 MCP 写入，门禁是流程约定，不是权限系统。

## Session 与方案

记录 runId、mode、deliverable、designerId、授权原文、目标白名单、当前 requirements/plan/design/library revision、来源与附件、需求追溯、units、内容/任务脚本、未决假设及恢复入口。方案审定不等于用户授权。review-observed 可执行只读解析，但不能写入或判 gap。

## 页面复用与参考复核

UX/UI Freeze 后、组件解析前，`referenceReview` 必须记录原输入文件页面扫描、组件库 Template 子流程和用户 Figma 参考。每项以现场页面/节点身份、`kind=reference` 工具证据登记，并给出 `matched / no-match / not-applicable` 与理由。页面命中时登记 `direct-reuse / adapt-reuse / reference-only`、对应 unit 和实际 changeScope。现有页面直接/改造复用必须成为对应 unit 的 `liveBaseline`；来源页只读，需要独立版本时只在授权目标内复制/重建。页面复用不能替代需求、不能改变写入目标，也不能替代现场组件解析；用户已经提供或 Skill 已登记的链接不得再次索要。

## Slot Evidence

每个实际使用槽位必须有 unitIds、requirementsBasis、`reuseLadder`、searchAttempts、逐候选 gateDecision/理由、description 与公开属性原始 evidenceRefs、chosenAssets、childSlotIds、slotBindings 以及版本。chosenAssets 用当次正式资产身份；实际变体主组件 key 在节点快照与 expectedFacts 中核验，不混同组件集 key。

候选先查用途、宿主、合法状态/属性、内容增长、实际子槽位和来源；文本标题可继承，关键证据不能缺。`reuseLadder` 固定 `formal-instance → compose → gap`，只有最后一步 matched 且等于 resolution；跳到 gap 的记录不成立。compose 记 `layoutOnly`（true 时附 `layoutReason`，false 时 chosenAssets 指向正式宿主）。formal-instance 修改了子槽位也要记录绑定，不仅 compose。gap 另有结构化 `composeTrials`、顶层 `libraryCatalog` 锚定的 inventory 与 compositionEvidenceRefs；未盘点或组合未试不能填 complete。formal-instance/compose 的 inventory 可为 not-required。

`libraryCatalog` 是当次发布库的完整目录证据（`libraryKey`、`complete=true`、`ids`）；gap 的 eligibleIds 必须覆盖完整目录，不能自造范围，`complete=true` 时 `liveLibrary.ids` 也必须是它的子集。`composeTrials` 每条至少给出 host、parts（目录内资产）、失败理由和证据；没有任何组合尝试就直接 gap 视为未取证。

## 现网基线与几何继承

复用现网已有屏幕或模式时，plan 的每个可见 unit 记录 `liveBaseline`：

- `applicability=replicated`：`screenRef` 指向现网节点/屏，`evidenceRefs` 为 kind=`baseline` 的现网截图或几何 JSON；build 后必须产出 baseline 对照证据，逐元素给出 `live / ours / delta / tolerance / status`。baseline 对照按 `(unitId, deliverable)` 定位并带 `deliverable` 字段，`both` 的 Figma 与 Demo 各一份，不能互相顶替。
- `applicability=new`：写明为什么没有现网对应，不能把“没找”写成“没有”。

baseline 对照里每个 delta 只能是 `within`（|delta| ≤ tolerance）或 `authorized`（附理由）；任何 open、超差未授权都不能交付。现网复用的 unit 里 formal/local/layout 实现都要用 `baselineElementId` 指向对照元素，逐元素核对现网尺寸与状态；纯文本 content 可省。Screen Spec 的数字只能来自现网基线或用户原文，不能凭印象新造。

## Implementation Log

每个实现记录 targetId、nodeId、unitId、slotId、交付物、origin、preEvidenceRef、postEvidenceRef 和 outcome。writeWhitelist、expectedFacts 用于抽查，允许为空。快照必须能核对组件身份（sourceAssetKey、mainComponentKey、type、nodeId）；可以附带原始工具字段。名称、外层布局、公开属性、内容和 description 示意填充是合法可见变化，不必为每个 JSON 路径补白名单。不允许根路径 `/` 放行一切。font/变量/效果/内部布局仍须对齐基线；description 要求的示意填充按 fills 例外登记，不能把未授权改色写成保护豁免。

布局/表面审计在现有布局快照及 UI/node 检查证据内附每个受影响宿主的角色依据、双轴对齐与分布意图、实际方向/对齐/尺寸/padding/gap、视觉属性、可见承载面和差异；换行/基线按适用项记录。正式实例内部只读核验，不能以标签代替职责判断。审计覆盖本次新建/修改节点及受影响祖先/兄弟/实例，记录覆盖范围；不新增一套与运行记录平行的门禁。

写入后从 Figma 重新读取，不从写入命令推测成功。正式实例 sourceAssetKey 通过主组件/owning set 的现场关系追溯；不能自行声称属于该 key。已有节点修复保留原快照；新节点才允许删除重建。

## Demo Mapping Evidence

每个正式 chosen asset 都有 mapping：chosenLiveKey → manifestAssetKey → generatedExport，propertySchemaMatch 和 evidenceRefs。`manifestAssetKey` 必须等于本地 `assetKey`；当次 live key 漂移时保留 `chosenLiveKey` 并另记 syncMismatch（type=identity-migration、reason、evidenceRefs）；证据含 fromKey/toKey 及 schema/dependencies/visual 的 before/after 非空相等指纹。库身份、版本/指纹、封装 props 和 slotBindings 一起验证。每个 `chosenAssets` 必须恰好有一条 mapping（按实例/使用状态记录可重复引用同一映射证据）。没有映射是 demo 能力阻断，不是 Figma gap。

## 裁切、溢出与双交付对齐

每个可见 unit/交付物有 overflow 检查证据：记录检查过的滚动容器、浮层和文本承载面，`escapes` 为空（后代 bbox 不得越出最近 `overflow:hidden` 祖先或视口；Figma 节点不得被中间容器意外裁掉效果；正常滚动/图片裁剪需分类证明）。

内容检查使用一份三方对照证据：`source`（内容脚本/原文）、`figma`、`demo` 与 `mismatches`。both 时三者必须在同一证据里且 mismatches 为空；只有一端时另一键可省略。

`deliverable=both` 的每个 unit 另有 parity 检查，引用 Figma 与 Demo 当次截图和一份 `figma`/`demo` 元素与文案对照，mismatches 为空。两端不互相抵消。

## 评审与问题

review 记录 stage、dimension、独立 reviewerId、packetRef、revision、coverage、报告 evidenceRefs、issueIds、verdict。原始评审报告用结构化 JSON 和具体发现正文保存；独立上下文只接收白名单材料。复验报告可以读取历史问题，不与盲审混用。

评审报告 `findings` 必须是结构化数组，每项含 `unitId`、`position`、`summary`、`evidenceRefs`；只写“已检查”或整段结论不算发现。`independent-review` 是必需能力：能力证据记录隔离机制（如独立子代理）和评审者身份，评审者不得是 designerId；主执行者代写或同上下文换角色不成立。

问题保留 originalSeverity、来源、位置、evidenceRefs、修复者、状态和 resolution。P0～P2 只有 verified-closed、证据充分的 not-a-bug 或指向已解决问题的 duplicate 可关闭；任何豁免、降级、pending、open、fix-applied 都不通过。修复不能删除原问题；关闭引用当前版本、不同于修复者的复验者和 verification 证据。

## 实际覆盖

截图、内容、节点、交互 checks 对应每个 required unit 和交付物；non-ui 约束同样需要 requirement check。captures 标 unit、交付物和版本；当前检查不得引用过期结论。最终 library-refresh 重新核对已用资产与基础规范。node-audit 必须引用结构化反查证据：`scanned` 列出扫过的目标节点，`unregistered` 和 `misclassified` 为空；它从目标反查未登记自建，不只检查登记表，不能用一个 pass 标签代替。

原始证据可在本次运行目录中留存并验证后复用，不能写回 Skill 当组件常量，也不能把别的任务证据冒充 live。库身份相同但发布内容变化时，受影响证据重新获取。
