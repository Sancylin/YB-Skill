# 参考文件索引

所有模式先读 [yuanbao-mobile-configuration.md](yuanbao-mobile-configuration.md)。再按“模式（`mode`）+ 交付物（`deliverable`）+ 识别到的业务域（`detected domain`）”只加载必要文件。

## 所有端到端任务

- [输入分流](input-routing.md)：先问交付物（未回复/无法询问默认 `web-demo`）；文字需求先产出 Requirement Spec/PRD（不预设页面解法），上传 PRD 原文直读；plan 门禁校验 `intake`。
- [自适应执行分级](adaptive-execution-profiles.md)：在 Experience Decision 前选择最低安全档 `fast / standard / full`，运行中按证据自动升级；档位只减少推理/评审轮次，不降低布局与截图质量门禁。
- [布局几何门禁](layout-quality-gate.md)：所有可见 unit 都检查 Auto Layout、padding/gap、对齐与实际几何，专门防简单需求的版式细节漂移。
- [自动编排与完成门禁](orchestration-and-completion-gates.md)：完成以视觉和组件调用为准；门禁拦漏项、现网基线/裁切/双交付/内容三方证据缺失和身份破坏。
- [运行记录格式](run-record-format.md) 与 [证据契约](evidence-contract.md)：创建 run.json，取证、盲审包及运行校验。
- [能力预检](capability-preflight.md)：访问与选型后的具体操作验证。
- [交互验证](interaction-validation.md)：有状态转换、原型或任务走查时。
## 按模式

- `generate`：[input-routing.md](input-routing.md) + [自适应执行分级](adaptive-execution-profiles.md) + [mode-generation.md](mode-generation.md) + [prd-design-contract.md](prd-design-contract.md) + [体验决策契约](experience/experience-decision-contract.md) + [产品体验模型](experience/product-experience-model.md) + [任务体验模式](experience/task-experience-patterns.md) + [体验案例契约](experience/experience-case-contract.md) + [任务模拟评审](experience/task-simulation-review.md) + [review-checklist.md](review-checklist.md) + [interaction-patterns.md](interaction-patterns.md)
- `iterate`：[mode-iteration.md](mode-iteration.md) + [interaction-patterns.md](interaction-patterns.md)
- `review-existing`：[mode-existing-design-review.md](mode-existing-design-review.md) + [review-checklist.md](review-checklist.md) + [interaction-patterns.md](interaction-patterns.md)
- `independent-review`：[mode-independent-review.md](mode-independent-review.md) + [review-checklist.md](review-checklist.md) + [interaction-patterns.md](interaction-patterns.md)


## 体验决策层

- [体验决策契约](experience/experience-decision-contract.md)：Requirement 与 UX Freeze 之间的强制 Planner。
- [产品体验模型](experience/product-experience-model.md)：产品实体、角色、规则和任务连续性的事实模型。
- [任务体验模式](experience/task-experience-patterns.md)：按频率、风险、数据量、可逆性等形成候选，不是 UI 模板。
- [体验案例契约](experience/experience-case-contract.md)：verified case 的结构、检索和防复制边界。
- [任务模拟评审](experience/task-simulation-review.md)：从用户视角逐步走任务，并支持 pairwise preference。

## 条件加载

- 首次调用 MCP、接口变化或故障：[工具适配契约](tool-adaptation-contract.md)。
- 证据采集、格式转换和比较：[采集与验证契约](capture-and-validation.md)。

- 解析或替换组件：[live-component-resolution.md](live-component-resolution.md)
- Figma 写入：[component-instance-safety.md](component-instance-safety.md)、[design-guidelines.md](design-guidelines.md)、[evidence-contract.md](evidence-contract.md)
- 自建真实缺口：[missing-component-creation.md](missing-component-creation.md)；基础规范见下一项。
- 自建层颜色、文字、圆角、投影、蒙层、分割、间距，或 Screen Spec 需要设备/画布/间距而组件 description 不足：[foundations/index.md](foundations/index.md)
- 对话或生成式回答：[conversation-content-domain.md](conversation-content-domain.md)
- 网页交互原型（未指定交付物时的默认值）：[web-demo-delivery.md](web-demo-delivery.md)；独立业务 Demo 用 `scripts/scaffold-demo.mjs` 生成到任务工作区
- 参考管理：[ai-canvas-and-references.md](ai-canvas-and-references.md)
- 画布整理：[canvas-organization.md](canvas-organization.md)
- 设备或画布不确定：[device-and-canvas-scan.md](device-and-canvas-scan.md)；iPad 与间距正式资产按 [foundations/index.md](foundations/index.md) 指向的现场页读取
- MCP 缺字体：[team-font-configuration.md](team-font-configuration.md)，团队共享 → 当前账号上传 → 必要时用户上传后恢复。
- 复用现网屏幕/模式：先按 [run-record-format.md](run-record-format.md) 记录 `liveBaseline`，几何与裁切判断见 [design-guidelines.md](design-guidelines.md)
- 评审分级与证据检查：[review-checklist.md](review-checklist.md)
- 状态含义：[state-and-fallback.md](state-and-fallback.md)

## 维护与评测

- [工作流回归场景](../evals/workflow-scenarios.md)：防执行、证据、组件与交付流程回归。
- [体验质量场景](../evals/experience-quality-scenarios.md)：专门评估 Experience Planner / Reviewer 的任务设计质量，优先使用 pairwise human preference。

## 非规范内容

- `demo/`：React 实现真相源，不反向决定 Figma 选型。
- `evals/`：回归与体验质量评测，不是组件规范，也不能反向成为页面模板。
- `docs/`：人类说明，不是 Agent 执行规则。
- 任务工作区的 `artifacts/`、`standalone-web/`：本次任务的运行记录与业务产物，写在任务工作区而不是 Skill 安装目录；不得升级为团队规范。
