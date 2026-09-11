# 生成模式（`generate`）

## 触发

从 PRD、附件或自然语言需求创建方案、设计稿或原型。先问用户要 Figma 设计稿、网页交互 Demo 还是两者都要；用户已在请求或 PRD 中明确时直接采用。用户不回复、跳过问题或无法询问时默认 `web-demo`。

先按 [输入分流](input-routing.md) 判定输入与交付物：文字需求先产出不预设页面方案的 Requirement Spec/PRD；上传 PRD 默认原文直读。随后先按 [自适应执行分级](adaptive-execution-profiles.md) 写 `executionProfile`，再执行 [体验决策契约](experience/experience-decision-contract.md)。Fast 优先验证既有 task model 上的 delta；Standard/Full 按风险展开完整体验决策。任何档位都在 Experience Review 通过后再进入 UX/UI Freeze 和组件解析。

## 允许写入

端到端生成授权覆盖目标业务文件内的实现、临时能力探测、独立评审后的范围内修复；不包含规范源修改或发布新库。

## 禁止

- 未通过 Experience Decision 与 plan 门禁就生成业务稿；未搜到并选定正式件就批量手绘；
- 跳过 `formal-instance → compose → gap` 阶梯直接手绘；把只做布局的宿主写成 gap 本地件；首次生成不主动复用正式件，等用户指出才改；
- 把搜索未命中、未发布资产或能力不足记成 gap；
- 用组件库缺口静默改业务需求；在 Experience Decision 之前读取组件目录并用组件可用性反推主流程；
- 文字需求跳过 PRD 产出直接进入 plan 或 build；
- 未确定交付物就默认按 Figma 生成，或用户已明确 Figma/both 却私自降成 Demo；
- UX 冻结后跳过原输入文件现有页面扫描、Template 子流程匹配或用户参考读取；也不能因为来源较旧就无条件重做，或把已登记来源当成未知文件再次索要链接；
- 未经用户明确要求就改写、精简、总结、扩写上传的 PRD 原文，或把它重排成“优化版”；
- 输出交接包或 run.json 填满后直接宣布完成，截图和组件调用尚未成立；
- 复用现网已有屏幕/模式却不给 `liveBaseline`，或凭印象新造 Screen Spec 尺寸；
- 独立终评尚未返回就预写 pass，或用建造脚本覆盖评审者原文。

## 流程

执行 [自动编排与完成门禁](orchestration-and-completion-gates.md)：输入分流 + 交付物分流 → 自适应 profile → Requirement Spec/原 PRD → Experience Decision / delta → 按档位独立评审 → UX/UI Freeze → 扫描现有页面并复核 Template/用户参考 → 页面级 `direct-reuse / adapt-reuse / reference-only / new` 决策 → 现网基线 → 现场组件解析（每个槽位走 `formal-instance → compose → gap` 阶梯，同类槽位默认批量搜索、通过 description gate 后早停）→ 批量生成 → 一次 read-back → [布局几何门禁](layout-quality-gate.md) + 截图复评 → 必要修复 / 自动升级 → 交付。已有页面可以直接成为新流程的一步；新增页面优先沿用最接近复用页面的壳层、导航、状态和内容连续性提示。业务稿仍写回原输入文件。Fast 只减少推理与 reviewer 轮次，不减少页面复用复核、组件身份、layout-geometry、overflow、content、node-audit 和截图。

方案、选型和最终验收均核对 [典型交互模式](interaction-patterns.md) 命中项。generate 的搜索依据是已发布库索引，源草稿变化须与发布证据区分。实际能力探测可在 plan 后的临时区执行，不以探测绕过业务生成门禁。

## 确认点

交付物问题是进入 plan 前唯一必须主动问的例行问题；用户不回复就按 `web-demo` 继续，不反复追问。参考 fileKey/nodeId/URL 已存在时不要索取链接。除此之外不例行等待冻结包确认；影响业务结果的歧义、超范围选择或用户明确要求逐步确认时才暂停相关工作。现场搜不到刚改过的 description 时说明发布依赖，不自行发布规范源。

## 停止

全部门禁通过且截图视觉、正式组件调用成立后停止。记录不完整时补记录，不要改坏已正确的可见稿。任一验收必需槽位或必需能力 blocked/degraded，或缺独立评审能力时进入 `paused-blocked`；次要 probe degraded 记录恢复入口后继续。可选项不能由 AI 擅自删减来通过。
