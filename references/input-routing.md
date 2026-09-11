# 输入分流（intake）

generate 的第一步是判定输入来源，写入运行记录 `intake`，再进入 plan。判定完成前不做选型、不建页、不写业务稿。字段定义见 [运行记录格式](run-record-format.md)，门禁位置见 [自动编排与完成门禁](orchestration-and-completion-gates.md)。

## 1. 判定表

| 用户输入 | `inputMode` | 行为 |
|---|---|---|
| 只有文字 / 口述需求，没有 PRD 文件 | `text` | 先产出 Requirement Spec/PRD（只冻结问题与约束，不预设页面解法），再进入 Experience Decision |
| 给出或上传 PRD 文件（md、docx、pdf、图片、在线文档） | `prd-file` | 默认原文直读；用户要求改写时按其要求执行 |
| 既有 PRD 文件又有补充文字 | `prd-file` | 保留文件原件；明确补充或变更优先生效并追溯 |

上传 PRD 默认原文直读；用户明确要求改写 / 精简 / 总结 / 优化时按其要求执行，见第 4 节——用户意图优先。

用户明确说“先给 PRD，确认后再出稿”时，PRD 产出后暂停等确认；否则产出 PRD 后连续执行，不例行等确认。

## 1.1 交付物分流（必须先确定）

`generate` 在进入 plan 前必须确定 `deliverable`：`figma`、`web-demo` 或 `both`。

1. 用户在本轮请求或 PRD 中已明确交付物时，直接采用：`source=user-specified`，`userChoice` 等于该选择，`evidenceRefs` 指向用户原话或 PRD 位置。
2. 未明确时必须先问一句：**“这次要 Figma 设计稿、网页交互 Demo，还是两者都要？”**
   - 用户回复后：`source=asked`，`userChoice` 等于回复，`evidenceRefs` 指向回复。
   - 用户不回复、跳过问题或继续其它指令时：给予合理回复机会后，`source=asked`、`userChoice=null`、`fallbackReason=no-reply`，默认 `deliverable=web-demo`。
3. 无法提问时（批量、自动化、无交互通道等）：`source=fallback`、`userChoice=null`、`fallbackReason=cannot-ask`，默认 `deliverable=web-demo`。

`both` 同时承担 Figma 与 Demo 两条交付链，不能为省事降成单端；用户明确“先只出 Figma”时按用户要求记 `userChoice=figma`。`web-demo` 指可交互网页原型，不是静态截图或组件库预览。

运行记录：

```json
"deliverableDecision": {
  "source": "user-specified | asked | fallback",
  "userChoice": "figma | web-demo | both | null",
  "fallbackReason": "no-reply | cannot-ask | null",
  "evidenceRefs": ["..."]
}
```

`source=user-specified`，或 `source=asked` 且 `userChoice` 非空时，`evidenceRefs` 必填；`userChoice=null` 时 `fallbackReason` 必填，且 `deliverable` 必须是 `web-demo`。

## 1.2 澄清记录

向用户追问影响交付的冲突或缺失信息时，把每次追问登记到 `intake.clarifications`：每项是对象，含 `question`（追问原文）和 `answer`（用户回复原文；未回复写 `null`）。澄清只补事实，不改写 PRD 原文；回答涉及需求变更时仍要回写 requirements 并刷新 revision。

## 1.3 页面复用与参考识别

generate 以及重跑 UX Freeze 的结构性 iterate 除了需求来源，还要识别可复用页面。来源优先级和判断规则见 [元宝移动端配置](yuanbao-mobile-configuration.md)，用户请求或 PRD 中的 Figma URL/附件也必须纳入。

1. 在 Experience Review 通过且 UX/UI Freeze 后，先扫描原输入文件顶层页面名称、ID 和可见结构，写入 `referenceReview.existingPageScan`；不能用旧项目常量代替现场页面列表。
2. 对每个已冻结 unit，先找原输入文件中的同类现有页面。命中时登记 `origin=target-file`、`sourceKind=target-existing-page`，实际页面身份从当次工具结果读取。确定直接复用或改造复用后，对应 unit 的 `liveBaseline` 必须指向该页面。
3. 再读取配置登记的组件库源文件 `iUyH8VSdURxlGrhp646zYJ`，按精确页名 `【AI参考案例】Template` 定位页面并检查内部可匹配子流程。命中项登记 `origin=built-in`、`sourceKind=component-library-template`；`pageName` 记录精确页面名，`nodeName/nodeId` 记录实际命中子流程。
4. 页面命中时记 `decision=matched` 并给出 `reuseAction`：`direct-reuse` 只允许调整流程位置，`adapt-reuse` 必须列出内容/状态/布局等 `changeScope`，局部参考记 `reference-only`。没有同类页面记 `no-match`，工具无法读取页面记 `not-applicable` 或阻断。来源不能覆盖 PRD，也不能改变业务目标。
5. 扫描用户原文、PRD 和附件中的 Figma URL，解析 `fileKey`、`nodeId` 与原始 URL，作为 `origin=user`、`sourceKind=user-reference` 项合并进 `referenceReview.sources`；同一 fileKey+nodeId 去重。
6. 所有页面来源和写入目标分开。用户给参考 URL 时默认不改写目标；只有用户明确说在该文件内创建/修改业务稿，才更新授权 scope 和目标。既有页面可以成为新流程的一步，或给后续新页面提供连续性提示；需要独立版本时只在授权目标内复制/重建。
7. 每项必须有当次 `kind=reference` 证据和 `matched / no-match / not-applicable` 结论。组件库或用户已经提供完整身份时直接读取；不得回复“请把文件链接给我”，只有字段缺失且无法从上下文恢复时才询问一次。

`referenceReview` 的具体字段见 [运行记录格式](run-record-format.md)。plan 门禁要求它已 `reviewed`；未复核不能进入组件解析。

## 2. 文字输入：先产出 Requirement Spec/PRD

1. 按 [PRD设计契约](prd-design-contract.md) 第 1 节做需求解析：业务目标、目标用户、使用场景、用户任务、成功标准、范围、设备、数据、权限、异常和依赖。
2. 写出 Requirement Spec/PRD，至少覆盖：
   - 业务目标 / 目标用户 / 用户任务 / 成功标准
   - 范围与约束（范围内 / 范围外）
   - 业务规则 / 数据 / 权限 / 依赖
   - 用户进入任务前的上下文与预期结果
   - 异常事实与验收标准
   - 明确假设与未决问题
3. **此文档禁止由 AI 预先写入页面地图、Modal/Drawer/Page 选择、具体布局、组件方案。** 用户原话明确指定时保留为 explicit constraint，不得删除。
4. 文档保存到当前任务工作区，并复制进 run 目录登记为 `kind=source`、`provenance=authored` 证据，写入 `intake.prdArtifact.evidenceRef` 与 `intake.rewritePolicy=authored`。
5. 把 PRD 文档路径交付给用户，然后进入 [体验决策契约](experience/experience-decision-contract.md)。原始文字仍登记为 required source；派生 PRD 不替代原始输入。

建议骨架：

```text
# <功能名> Requirement Spec / PRD
## 1. 业务目标 / 目标用户 / 用户任务 / 成功标准
## 2. 范围与约束
## 3. 业务规则 / 数据 / 权限 / 依赖
## 4. 用户上下文与预期结果
## 5. 异常事实与验收标准
## 6. 假设与未决问题
```

任务流、页面地图、状态矩阵、内容脚本、抽象槽位与 Screen Spec 均在 Experience Decision 通过后再产生。机器检查 PRD 非空及原始输入追溯；完整性由独立需求评审判断，不设最小字数。

## 3. PRD 文件输入：默认原文直读

默认 `intake.inputMode=prd-file`、`intake.rewritePolicy=verbatim`、`intake.prdArtifact` 为空、`intake.sourceDocs` 指向已登记的必需 source。

- **禁止**（未经用户要求时）：总结、精简、改写、扩写、重排结构、替换术语、合并或删减需求，以及任何形式的“优化版 PRD”。用户说“不需要做任何总结和优化”时按字面执行。
- **允许**：读原文、编号、建立 `requirementId` 映射、记录 `sourceId / 位置 / 版本 / readStatus / evidenceRefs`、只对影响主流程或交付物的冲突提问。
- 每条 requirement 的 `statement` 必须能回指原文位置，`origin=explicit`；原文没有、由设计推导的决定记 `derived` 并写依据，不得冒充原文。
- 上传的 PRD 本身登记为 `kind=source`、`provenance=captured` 证据；verbatim 模式下不得新增任何 authored 的 source 证据。
- 缺失必要且影响任务决策的材料时按缺必要材料处理，进入 `paused-blocked` 并给出恢复入口，不替用户补写 PRD。

## 4. 用户明确要求改写

用户意图优先于默认原文直读。用户说“帮我精简一下”“按这份 PRD 改写成……”“总结成摘要”等，就按其要求执行：

1. 把用户原话登记为 `kind=authorization`、`provenance=captured` 证据；
2. 先读原文（`sourceDocs` 全部 `readStatus=read`），再产出改写稿；
3. `rewritePolicy=rewrite-authorized`，`rewriteAuthorization.evidenceRefs` 指向该授权证据；改写稿登记为 `kind=source`、`provenance=authored`，需要时写入 `prdArtifact`；
4. 记录改写范围（改写 / 精简 / 总结 / 扩写 / 重排）和未覆盖的原文 requirement，验收时对照原 PRD 说明差异。

没有可指认的用户原话时不得自行判定“用户想改写”；不确定就问一句，不默认改写也不默认拒绝。

## 5. 混合输入

原件保留不改；最新、明确适用于当前任务的用户增补/替换/取消优先生效。使用根 changeSet 数组登记 operation（add/replace/remove）、evidenceRefs、reason；replace/remove 保存 previousRequirement（完整旧项快照），旧 ID 不再出现在当前 requirements；add/replace 指向新的 requirementId。模糊意见不是自动变更，影响业务结果的歧义才询问。

AI 生成 PRD 标 provenance=authored，原始文字与附件持续作为 required source，独立评审必须同时读取。AI 推导不能成为唯一需求原文。

## 6. 迭代模式

`iterate` 的文字变更请求不重写整份 PRD：在既有 PRD 上追加变更单（来源、影响范围、受影响 requirement / unit），按 [模式-迭代](mode-iteration.md) 验证影响范围。只有变更改变任务流或信息架构时，才回到 [PRD设计契约](prd-design-contract.md) 重新冻结。

## 7. 门禁

plan 门禁校验 `intake`：

- `inputMode` 必须是 `text` 或 `prd-file`；
- `deliverableDecision` 按第 1.1 节：`userChoice` 非空时必须等于 `deliverable` 并附用户证据；`userChoice=null` 时 `fallbackReason` 必须是 `no-reply` 或 `cannot-ask`，且 `deliverable=web-demo`；
- `text`：`rewritePolicy=authored`，`prdArtifact.evidenceRef` 指向存在且哈希一致的 `source` 证据，原始输入由 originalSourceIds 指向 required captured source，语义完整性由需求评审检查；
- `prd-file`：`sourceDocs` 全部 `readStatus=read`；`rewritePolicy=verbatim` 时 `prdArtifact` 为空且本次运行没有 authored 的 source 证据；`rewritePolicy=rewrite-authorized` 时 `rewriteAuthorization.evidenceRefs` 指向用户的 `authorization` 证据，改写稿可登记为 authored source；
- `referenceReview.status=reviewed`，且现有页面扫描、组件库 Template 项与用户参考项均有当次 `reference` 证据和结论；页面命中项必须给出 `reuseAction`，直接/改造复用现有页面时对应 unit 必须有匹配的 `liveBaseline`；未复核不得进入组件解析；
- `review-existing` 与 `independent-review` 不适用本门禁，按各自模式读原文。
