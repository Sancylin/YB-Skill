# 运行记录格式与命令

这是 validate-run.py 接受的版本 3 契约；本次扩展在不改变 schemaVersion 的前提下增加体验决策门禁。不使用只检查关键词的结构校验代替运行验证。以下命令以源码目录为例。安装后使用脚本的绝对路径，run-dir 放在任务工作区，不能把业务证据写进已安装 Skill 目录。所有路径相对 run.json 所在目录；证据必须实际存在于该目录内，不能用外链、路径穿越或指向目录外的软链接。

## 开始与取证

```text
python3 scripts/validate-run.py --init artifacts/<run-id>
python3 scripts/validate-run.py artifacts/<run-id>/run.json --add-evidence raw/prd.md --id prd-1 --kind source --provenance captured
python3 scripts/validate-run.py artifacts/<run-id>/run.json --gate plan
python3 scripts/validate-run.py artifacts/<run-id>/run.json --gate report
```

init 只创建未完成骨架，已有 run.json 不覆盖。先保存真实材料再 add-evidence；它计算 sha256 并登记，不能证明材料来自哪个工具。source/authorization 来自用户输入；tool/screenshot 来自本次工具；plan/review/verification 是有来源和判断的报告，可标 authored。fixture 只用于离线测试，生产门禁不接受。

门禁返回 JSON 和退出码：0 表示记录通过，1 表示失败。完整输出保存为本次门禁报告，不用截取 passed 一行。模拟测试必须显式 --allow-fixture，不能作为真实设计交付报告。

## 根字段

| 字段 | 类型与意义 |
|---|---|
| schemaVersion / runId / designerId | 3 / 非空 ID / 实现者身份 |
| mode | generate、iterate、review-existing、independent-review |
| intake | 输入分流：`inputMode`（text / prd-file）、`deliverableDecision`（交付物确认）、`prdArtifact`（文字输入产出的 PRD 证据）、`sourceDocs`（上传 PRD 的 source id）、`rewritePolicy`（authored / verbatim / rewrite-authorized）、`rewriteAuthorization`（用户明确要求改写的授权证据）、`clarifications`；generate 必填，由 plan 门禁校验，规则见 [输入分流](input-routing.md) |
| referenceReview | 页面复用与参考复核：`status=reviewed`、`existingPageScan`（原输入文件页面扫描）、`sources`（现有页面、组件库 Template 与用户 Figma 参考，每项含 id、origin、sourceKind、fileKey、nodeId、pageName、nodeName、url、decision、reason、evidenceRefs；命中项另含 reuseAction、unitIds、changeScope）；generate 与重跑 UX Freeze 的结构性 iterate 在组件解析前必填，规则见 [输入分流](input-routing.md) 第 1.3 节 |
| deliverable | figma、web-demo、both |
| environment | live；测试用 fixture |
| status | running、paused-blocked、complete |
| stage | 当前执行阶段：intake、experience-plan、experience-review、plan、plan-review、resolve、capability、build、blind-review、system-audit、fix、verify、deliver、report |
| revision | requirements、plan、design、library 四个非空版本标识；未到达阶段可暂为 pending，但对应门禁不通过 |
| authorization | write、fix、requirePlanConfirmation 布尔；scope 为允许的 targetId 字符串数组，进入 build 时 write=true 且 scope 至少一个非空字符串（不接受单字符串）；evidenceRefs 指授权原文 |
| executionProfile | generate/iterate 的自适应执行强度：`level=fast|standard|full`、`source=auto|user`、`assessment`、`requiredSimulations`、`reasons`、`escalationHistory`；规则见 [自适应执行分级](adaptive-execution-profiles.md) |
| experienceDecision | generate/iterate 的任务级体验决策摘要：status=reviewed、taskIds、chosenModels（taskId/model/rationale）、confidence、evidenceRefs(kind=plan)；先于页面/组件方案成立 |
| planEvidenceRefs / taskEvidenceRefs | UX/UI 方案正文 / 中性任务脚本证据 ID 数组 |
| nextAction / blockers | 下一步及阻断/恢复条件；blockers 必须是数组，交付时为空数组 |
| liveLibrary | 有槽位时必填：`libraryKey`、`version` 或 `fingerprint`、`observedAt`、当次会话观察到的发布库 `ids`、`evidenceRefs`（kind=tool）；每个 `chosenAssets` 必须是 `ids` 成员。`libraryCatalog.complete=true` 时 `ids` 必须是目录 `ids` 的子集，不能凭空多出未发布组件。发布库确为空时 `ids=[]` 且另记 `emptyProof=true` 并附工具证据 |
| libraryCatalog | 有 `gap` 时必填：`libraryKey`（须与 `liveLibrary.libraryKey` 一致）、`complete=true`、当次发布库完整 `ids`、`evidenceRefs`；槽位 inventory 必须分类完整目录（扫描或有依据排除） |

下列集合全部为数组，即使当前为空也保留。带 id 的集合内 ID 唯一，引用使用字符串 ID；captures 以 unitId、deliverable 和 revision 定位。

## 交付物确认

`intake.deliverableDecision` 记录本次为什么选 `figma` / `web-demo` / `both`：

| 字段 | 含义 |
|---|---|
| source | `user-specified`（用户已明确）、`asked`（本次问过）、`fallback`（无法询问） |
| userChoice | 用户选择；没得到回复时为 null |
| fallbackReason | `no-reply` 或 `cannot-ask`；用户已选择时为 null |
| evidenceRefs | 用户原话/回复的 source 或 authorization 证据；仅在用户选择非空时必填 |

`userChoice` 非空时必须等于根字段 `deliverable`；`userChoice=null` 时 `deliverable` 必须是 `web-demo`。用户不回复或无法询问都默认网页交互 Demo，不得默认 Figma。

## 输入与方案集合

| 集合 | 每项字段 |
|---|---|
| evidence | id、path、sha256、kind、provenance；kind 为 source/authorization/plan/task/constraint/screenshot/baseline/reference/tool/review/verification/packet；reference 是当次参考页工具证据，baseline 是现网截图或几何 JSON |
| sources | id、required 布尔、readStatus、evidenceRefs；必要材料 readStatus=read |
| requirements | id、statement、acceptance、sourceLocation、origin（explicit/derived/team）、sourceIds、targets |
| units | id、kind（screen/state/non-ui）、required=true、requirementIds、deliverables（figma/demo）、interactionLevel 或 interactionLevels、liveBaseline |
| assumptions | id、impact（business/design）、status、evidenceRefs；business 必须 resolved |

units 是当前已审定交付范围，全部 required；建议项放问题建议区，不能把失败 unit 改 required=false 来绕过。明确的范围变更保留授权与历史，更新 requirements/plan revision。非 UI 项 deliverables 可为空，验收以 non-ui 分支检查。双交付的每个可见 unit 默认同时覆盖 figma/demo；用户限定不同范围时分别作为独立运行记录，不能静默删一端。

交互等级有两种写法：单交付物或 non-ui 用 `interactionLevel`（design/executed/not-applicable）；`both` 用 `interactionLevels`，键必须与 `deliverables` 一致，例如 `{figma: design, demo: executed}`。Figma 交静态状态屏记 `design`，能点走查记在 Demo 的 `executed`，不能把 Figma 伪造成 `executed`，也不能因为 `design` 就少画交互后的屏。deliver 门禁按交付物逐端核对 interaction 检查的 `level`。

## 自适应执行分级

`executionProfile` 在 Experience Decision 前建立。plan 门禁按 assessment 计算最低安全档；允许选更高档，不允许低于最低档。Fast/Standard/Full 只改变独立评审和任务模拟强度，不改变组件、截图与布局几何质量门禁。运行中发现 gap、复杂 compose、新 IA/权限/高风险/长异步/部分成功等信号时升级并记录 `escalationHistory`。字段与路由表见 [自适应执行分级](adaptive-execution-profiles.md)。

## 体验决策摘要

`experienceDecision` 是 plan 门禁的硬字段，用来防止 Agent 直接从需求跳到页面和组件。它不是完整 EDR 的替代；完整内容放在 kind=`plan` 的证据里，并由 `evidenceRefs` 指向。

```json
{
  "experienceDecision": {
    "status": "reviewed",
    "taskIds": ["task-main"],
    "chosenModels": [
      {
        "taskId": "task-main",
        "model": "contextual-quick-edit",
        "rationale": ["高频低风险且需要保留当前上下文"]
      }
    ],
    "confidence": "high",
    "evidenceRefs": ["experience-plan"]
  }
}
```

`confidence=low` 可以保存，但如果低置信事项会改变主流程，按 [体验决策契约](experience/experience-decision-contract.md) 不得进入 reviewed。

## 组件与能力集合

| 集合 | 每项字段 |
|---|---|
| slots | id、unitIds、requirementsBasis、revision、resolution、reuseLadder、searchAttempts、candidates、chosenAssets、childSlotIds、slotBindings、evidenceRefs |
| candidates（内嵌） | key、gateDecision、reason、evidenceRefs；key 对应现场资产；decision 为 pass/reject-proven-mismatch/blocked-insufficient-evidence |
| reuseLadder（内嵌） | 顺序固定 `formal-instance → compose → gap`，不可跳级；每步 step、outcome（matched/exhausted）、reason、evidenceRefs；只有最后一步 matched 且等于 resolution |
| searchAttempts（内嵌） | source（semantic/published-name/page-routed/inventory）、query 或 pageId、evidenceRefs |
| slotBindings（内嵌） | childSlotId、parentAssetKey、host、evidenceRefs |
| compose 槽字段 | `layoutOnly` 布尔；true 时 `layoutReason` 必填且宿主是纯布局层；false 时 chosenAssets 必须指向正式宿主 |
| composeTrials（gap 槽内） | host（layout 或目录内资产）、parts（目录内资产数组）、outcome=reject-proven-mismatch、reason、evidenceRefs；至少一条 |
| inventory（gap 槽内） | complete、eligibleIds（= libraryCatalog.ids）、scannedIds、exclusions、evidenceRefs；目录非空而 eligible 为空时另需 scopeReason |
| compositionEvidenceRefs（gap 槽内） | 职责分解、正式子件复用和合法组合仍缺能力的验证证据 |
| capabilities | id（见能力预检）、status、revision、evidenceRefs；必需能力必须 passed，次要能力可为 passed/degraded/blocked；`independent-review` 的证据还要含 isolated=true、mechanism、reviewerIds；有 gap 时必须有 `compose-check` |

resolution 为 formal-instance/compose/gap/blocked；进入 build 不允许 blocked。chosenAssets 为选中的正式资产 key 数组，必须有 pass 候选，且每个 key 必须是顶层 `liveLibrary.ids` 的成员。gap 本身的候选证明不匹配，复用的正式子件放独立 child slots（它们有自己的 pass）。所有 childSlotIds 都有实际 slotBindings。空库亦需原始空目录证明，不用伪造候选；详见脚本的空 inventory 支持。只做布局的宿主记 `compose`，不记 `gap`。

slot 和 capability 校验 requirements/plan/library；变体与不同状态需要不同资产时按状态拆槽，避免把互斥资产都要求放在同一 unit 中。

## 实现集合

| 集合 | 每项字段 |
|---|---|
| implementations | id、unitId、slotId、deliverable、targetId、nodeId、origin（formal/local/layout/content）、revision、outcome=ok、preEvidenceRef、postEvidenceRef；writeWhitelist 与 expectedFacts 可选；现网复用的 unit 里 formal/local/layout 实现还要 baselineElementId |
| formal 附加 | assetKey；Figma 快照 sourceAssetKey 对齐选中资产；变体看 post.mainComponentKey；description 要求处理示意填充时另有 descriptionFillAdjustments |
| local 附加 | localComponentId；快照 mainComponentId 必须指向登记主组件 |
| demo formal 附加 mapping | chosenLiveKey、manifestAssetKey（必须等于本地 assetKey）、generatedExport、propertySchemaMatch、evidenceRefs；chosenLiveKey 与 assetKey 不一致时另需 syncMismatch（type=identity-migration、reason、evidenceRefs）；证据含 fromKey/toKey 及 schema/dependencies/visual 的 before/after 非空相等指纹 |
| localComponents | id、slotId、nodeId、dependencyKeys、instanceNodeIds、evidenceRefs、mainEvidenceRef |

pre/post 必须能核对身份：ancestorIds、targetId、type、nodeId、sourceAssetKey、mainComponentKey、mainComponentId、properties、content、layout、name、parentId、overrides、protected。可以多带原始工具字段。protected 含 font、textStyle、variables、fills、effects、internalLayout。正式基线含 sourceAssetKey、mainComponentKey、protected、legalPropertyNames，示意填充例外时还要有 description。overrides 的 kind 为 public-property/allowed-text/outer-layout/description-fill。writeWhitelist 可选，用于抽查；禁止 `/`。名称、外层布局、公开属性、内容、祖先链和 description 示意填充是合法可见变化，脚本不因缺白名单路径失败。font、textStyle、variables、effects、internalLayout 必须与基线一致，不能靠白名单换字体或解绑变量。fills 仅当 description 要求处理间距示意填充时可与基线不同，须有 descriptionFillAdjustments（nodeId、paintIndex、property、before、after、action=hide-fill、descriptionQuote；layerName 仅作说明），protected.fills 为节点 ID 到 paint 数组的映射，变化必须逐项匹配，且 fills 确实变了。expectedFacts 可选，有则必须与快照一致。正式 Figma 实例的 post 快照须有 mainComponentKey。chosenAssets 必须实际出现在对应交付物上。本地 mainEvidenceRef 指向含 nodeId、type（COMPONENT/COMPONENT_SET；Demo 用 CODE_COMPONENT）、dependencyKeys、boundFoundations、description 的工具证据。非组件化 layout/content 不能替代 gap 主组件。

## 评审、截图与检查

| 集合 | 每项字段 |
|---|---|
| reviews | id、stage（plan/final）、dimension（requirements/experience/ux/ui/system）、reviewerId、independent=true、revision、coverage（unitIds）、evidenceRefs、issueIds、verdict（生成/迭代门禁必须 pass；只读报告可 issues，且每个 P0～P2 发现回指台账）、packetRef（必须指向 kind=packet 证据） |
| captures | unitId、deliverable、revision、evidenceRef（kind=screenshot） |
| checks | id、unitId、deliverable、kind、revision、result（pass/fail/unknown）、evidenceRefs；kind 为 visual/content/node-audit/layout-geometry/interaction/requirement/library-refresh，可见 unit 另有 overflow，现网复用加 baseline，both 加 parity；interaction 另有 level，按交付物对应 `interactionLevel`/`interactionLevels` |
| issues | id、stage、severity、originalSeverity（P0/P1/P2/suggestion）、unitIds、evidenceRefs、state、fixAuthor、reason、resolution；duplicate 另有 duplicateOf |
| resolution（内嵌） | reviewerId、revision、reason、evidenceRefs（kind=verification） |

### 检查证据

- `layout-geometry`：`{unitId, deliverable, verdict, checked:[...], measurements:[{kind,values,tolerance,status,reason?}], violations:[]}`；每个 visible unit 必填。`status=within` 时数值离散必须在 tolerance 内，`authorized` 必须给 reason。结构见 [布局几何门禁](layout-quality-gate.md)。
- `liveBaseline`：`applicability=replicated` 时给 `screenRef` 和 kind=`baseline` 的 evidenceRefs；`applicability=new` 时给 reason。plan 门禁要求所有可见 unit 做出选择。
- `referenceReview.existingPageScan`：`status=scanned` 时给出原输入文件 `fileKey`、顶层 `pageIds` 和 kind=`reference` 证据；页面为空时另给 reason。没有可用输入文件时可为 `not-applicable` 并给 reason。
- `referenceReview.sources`：每项给出 `id`、`origin`（built-in/target-file/user）、`sourceKind`（component-library-template/target-existing-page/user-reference）、实际 `fileKey`、`nodeId`、`pageName`、`nodeName`、`url`、`decision`（matched/no-match/not-applicable）、`reason` 和至少一条 kind=`reference` 证据。组件库 Template 项必须使用 `id=yuanbao-component-template`、`origin=built-in`、`sourceKind=component-library-template`、fileKey=`iUyH8VSdURxlGrhp646zYJ`、pageName=`【AI参考案例】Template`；`nodeName/nodeId` 记录内部实际命中子流程。命中时必须有 `extractedPatterns`、`reuseAction`、`unitIds` 和 `changeScope`：`direct-reuse` 只允许 `flow-order`，`adapt-reuse` 必须列出内容/状态/布局等实际改动，`reference-only` 表示仅借鉴局部。`origin=target-file` 的页面被直接或改造复用时，对应 unit 的 `liveBaseline.applicability=replicated` 且 `screenRef` 等于该页面 nodeId；未完成不得进入组件解析。
- baseline 对照：`{unitId, deliverable, verdict, elements:[{id, live, ours, deltas:[{field, live, ours, delta, tolerance, status, reason?}]}]}`；status 只能 within/authorized，within 要求 |delta|≤tolerance，authorized 要求 reason。baseline 按 `(unitId, deliverable)` 定位，Figma 与 Demo 各自一份，不能互相顶替。
- overflow：`{unitId, deliverable, checked:[...], escapes:[], verdict}`；escapes 必须为空。
- content：`{unitId, source, figma, demo?, mismatches:[], verdict}`；both 时三个来源都要有，mismatches 必须为空。
- parity：`{unitId, figma, demo, mismatches:[], verdict}`；both 的每个 unit 用 Figma 与 Demo 当次截图加这份对照。


plan 需要 requirements/experience/ux/ui 四个维度，final 需要 ux/ui/system；每个维度覆盖全部 unit。每个维度都使用隔离评审者，reviewerId 不得等于 designerId；UX 与 UI 另须使用不同评审者。报告原文不能只写 pass：保存具体依据、覆盖及发现；结构化报告的元数据与 reviews 一致，包含 reviewerId、stage、dimension、revision、coverage、issueIds、verdict；`findings` 必须是数组，每项含 unitId、position、summary、evidenceRefs；finding 标了 P0/P1/P2 时必须带 `issueId`，且 issue 的 severity 一致，建议项标 `suggestion`。

plan 的 `experience` 报告与 final 的 `ux` 报告还必须包含 `simulationScenarios`，至少覆盖 `happy-path / first-use / error / interrupt / post-success`。每项含 `category`、`verdict=pass|issue`、`summary`；这让“任务模拟已执行”成为机器可检查的事实，而不是只写在 checklist 里的口号。

issues 必须绑定 `unitIds` 且指向已知 unit，不能登记无范围的全局问题；无法定位到 unit 时先补观察证据或缩小到具体范围。

每个可见 unit/交付物需 visual、content、node-audit、overflow；有交互再要 interaction，现网复用再加 baseline，both 再加 parity。visual 检查必须引用当次截图，写入日志不算。node-audit 引用结构化反查证据：`scanned` 非空、`unregistered` 与 `misclassified` 为空；只写 pass 不算。内容要覆盖 source/figma/demo 三方，双交付要有两端截图和元素文案对照。缺少截图或任一检查失败则不能交付。library-refresh 仍要，用于确认用的还是当次库。non-ui 的 `requirement` 检查 `deliverable` 固定写 `non-ui`。

`nextAction` 非空时必须是已知恢复/停止动作：resume-plan、resume-resolve、resume-build、resume-review、resume-verify、deliver、report、wait-user。`taskEvidenceRefs` 可省略（按空数组处理）；一旦填写，每一项都必须是 kind=task 的中性任务脚本证据。

## 盲审包

```text
python3 scripts/validate-run.py artifacts/<run-id>/run.json --packet plan --reviewer ux-plan > artifacts/<run-id>/ux-plan-packet.json
python3 scripts/validate-run.py artifacts/<run-id>/run.json --add-evidence ux-plan-packet.json --id ux-plan-packet --kind packet --provenance authored
```

随后只把包及其引用材料提供给无历史继承的评审者；不要提供 run.json。包必须含 schemaVersion、stage、reviewerId、revision、unitIds、evidenceRefs；可以多备注字段，不得夹带结论字段。plan 包允许 source/task/constraint/plan/reference；final 包允许 source/task/constraint/screenshot。所有必要原始附件必须在包内，组件库 Template 页面证据也随 reference 进入 plan 包。工具检查材料类别；隔离是否成立仍需执行者确认。

## 只读报告门禁

`review-existing` 与单独的 `independent-review` 不执行 build/deliver，使用 `--gate report`：

```text
python3 scripts/validate-run.py artifacts/<run-id>/run.json --gate report
```

只读 run 允许 `sources`/`requirements` 为空，但必须有观察得到的 `units`、每个可见 unit 的当前 revision 截图、final 的 ux/ui/system 评审、问题台账和结构化发现。`mode` 必须是只读模式，`stage=report`、`status=complete`；`revision` 的 requirements/plan 记被审稿版本或 `n/a`，不能留 `pending`；缺原 PRD 时在报告中单列业务需求 coverage 未知。只读模式调用 `--gate plan|build|deliver` 会被拒绝，不能靠自审或旧证据冒充设计交付。

只读报告允许评审 `verdict=pass` 或 `verdict=issues`：`issues` 必须带结构化 findings，P0/P1/P2 必须回指问题台账；只写 issues 不写发现不成立。只读报告不要求关闭 P0～P2，但必须如实登记。

## 方案复审触发

Figma 修复记录若在 implementation 上报告 `requiresPlanReview=true`、`structureChange=true`、`businessResultChanged=true`，或 `changeImpact` 命中 `information-architecture-change` / `main-action-change` / `business-result-change`，deliver 门禁必须拒绝并返回 `nextAction=resume-plan`；回到方案评审、刷新 requirements/plan revision 后再继续，不能直接交付。三个布尔标志一旦出现必须是真布尔值；`changeImpact` 是字符串或字符串数组，且取值只能来自上述三个登记值，未知字符串或非字符串会被门禁拒绝，不能借此绕过回 plan 的触发器。

## 历史评审与复验

review 可带 supersedes 数组，指向同阶段/维度、覆盖不更小的旧评审 ID。旧报告和原问题保留；当前有效评审计算门禁，旧问题仍必须在 issues 中得到证据化关闭。禁止自引用或循环。误报独立判定 not-a-bug 后，可同设计 revision 新建复评取代旧报告，不为通过虚增设计版本。

正式实例公开属性切换可能合法改变视觉，protected 对照的是现场目标变体/合法公开配置的规范基线，而非强迫所有状态等于旧变体。基线身份与实际 mainComponentKey 必须一致；不能把组件集 key 与具体变体 key 混为一谈。工具证据归一化仍需保留原结果供审计核对，脚本不能判断一个人工伪造的基线是否真的来自工具。

## 特定用户确认与目标身份

用户明确要求先确认方案时，authorization.requirePlanConfirmation=true；planConfirmation 保存当前 requirements/plan revision 与用户确认原文 evidenceRefs。user-confirmed 槽位同样必须有此证据，不能只改标签。默认 reviewed-plan 不额外要求人工确认。

targetId 由节点现场归属确认（建议使用 fileKey/pageId 的稳定组合），pre/post、实现记录与授权 scope 必须一致；parentId 是实际直接父节点，不能代替目标页身份。规范化快照要包含保护字段，不适用值保持明确的空结构，不通过删字段规避审计。

## 组合与本地依赖的结构关联

compose 可以没有匹配的正式父组件：chosenAssets/candidates 可为空，但必须记 `layoutOnly=true` 和 `layoutReason`，并有已解析 childSlotIds、绑定证据和实际 layout 实现；宿主只能承担布局职责，有视觉表面时必须指向正式宿主。无完整父组件不等于 gap，不能为了填记录而制造候选或新组件，也不能把“懒得组合”写成 gap。

binding.host 为非空宿主名/路径，parentAssetKey 是父槽位 chosenAssets 中的正式 key；纯布局组合用 layout:<父slotId>，gap 自建容器用 local:<父slotId>。只有向正式资产的 Slot/Swap 写入才要求 slot-write 能力，普通布局组合用 layout 能力。每条绑定的子槽位覆盖父槽位所有 unit；状态不同则拆父槽位，不能留下未覆盖的隐含绑定。

本地组件 dependencyKeys 必须来自该 gap 的递归 child slots 的正式选型，并在每个本地实例的相应 unit/交付物中出现真实正式后代。ancestorIds 保存现场祖先链，用于验证这种从属关系，不能把页面别处同 key 的实例算成复用。

Figma 本地主组件仅接受 COMPONENT/COMPONENT_SET，Demo 仅 CODE_COMPONENT；both 的本地主组件分别登记，不能共用一条不同平台的主组件记录。

所有历史评审及其原始结构化报告的 issueIds 都必须存在于 issues。版本变化使结论过期，不免除问题登记与关闭义务；不能只检查当前评审而丢弃历史发现。

合法迁入布局容器时，writeWhitelist 中允许 /parentId，ancestorIds 随真实父级变化是派生变化，可同时更新；显式列 /ancestorIds 也只在该条件下允许。节点身份与 targetId 不得变化，祖先链首项必须等于直接 parentId，正式依赖仍须满足最终从属关系。不得只改变祖先链来伪造包含关系。

## 运行记录格式

运行记录使用 `schemaVersion=3`。`scripts/migrate-run.py` 可转换 `schemaVersion=2` 的输入；原件保留，缺失证据必须补采并重验，已有 pass 不自动视为有效。详见 [采集与验证契约](capture-and-validation.md)。
