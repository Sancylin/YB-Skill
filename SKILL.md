---
name: yb-mobile-design
description: 先问要 Figma 设计稿、网页交互 Demo 还是两者（未回复或无法询问默认网页 Demo），把需求拆成 Requirement Spec → Experience Decision → UX/UI Freeze，并按风险自适应选择 fast / standard / full 执行强度；组件事实实时来自元宝移动端 Figma 组件库，所有档位保留布局几何、截图和组件身份硬门禁，独立评审并修复 P0～P2。
---

# 元宝移动端设计工作流

先读 [元宝移动端配置](references/yuanbao-mobile-configuration.md)，选择模式，再按 [索引](references/index.md) 加载当前阶段需要的文件；不一次性通读全部附件。组件事实来自当前 Figma MCP；Skill 不保存组件配方。

## 输入分流

进入 generate 前先判定输入来源并写入运行记录 `intake`，规则见 [输入分流](references/input-routing.md)：

- **文字需求**：先产出不预设页面解法的 Requirement Spec/PRD（交付路径 + 登记 `source` 证据），再进入 Experience Decision；不得跳过体验决策直接选型或出稿。
- **上传 PRD 文档**：默认原文直读，`rewritePolicy=verbatim`；不总结、不精简、不改写、不扩写。用户明确要求改写 / 精简 / 总结 / 优化时按用户要求执行，记 `rewrite-authorized` 并登记授权证据。
- 混合输入保留原附件，用户明确增补、替换或取消通过变更单生效；最新明确变更优先，含糊冲突才询问。

## 交付物分流

进入 generate 前还必须确定交付物：**先问用户要 Figma 设计稿、网页交互 Demo，还是两者都要**；用户已在请求或 PRD 中明确时直接采用。用户不回复、跳过问题或无法询问时，默认 `web-demo`（网页交互 Demo）。判定规则与 `deliverableDecision` 字段见 [输入分流](references/input-routing.md) 第 1.1 节。

## 页面复用与参考分流

UX/UI Freeze 后、组件解析前必须先检查：原输入文件里的既有页面、组件库精确页面 `【AI参考案例】Template` 内可匹配的子流程，以及用户给出的 Figma 参考。候选页面按 `direct-reuse → adapt-reuse → reference-only → new` 作页面级判断，并把决策写入 `referenceReview`。旧页面和旧资产有效时可以直接接入新流程或作为后续新页面的连续性提示；需要改内容、状态或布局时按范围改造，不能因为“旧”就整体废弃，也不能因为能复制就跳过身份校验。组件库来源始终只读，业务输出仍写回原输入文件。

页面级复用后，每个正式组件仍走现场 `formal-instance → compose → gap` 阶梯；二者是两层决策，不能互相代替。

## 模式与授权

| 模式 | 入口 | 默认行为 |
|---|---|---|
| `generate` | [生成](references/mode-generation.md) | [输入分流](references/input-routing.md) → [自适应执行分级](references/adaptive-execution-profiles.md) → Requirement Spec → Experience Decision → UX/UI Freeze → 现有页面/Template/用户参考复核 → 页面级复用决策 → 组件解析 → 生成 → 按档位独立复评/自动升级 → 最终门禁 |
| `iterate` | [迭代](references/mode-iteration.md) | 修改指定目标，验证影响范围 |
| `review-existing` | [已有稿评审](references/mode-existing-design-review.md) | 只评不改，缺原 PRD 时声明业务覆盖限制；用 `--gate report` 校验只读报告，报告可 `verdict=issues` 但 P0～P2 必须回指台账 |
| `independent-review` | [独立复评](references/mode-independent-review.md) | 独立上下文评审；端到端任务继承范围内修复授权 |

用户明确交付物时直接采用；否则先问要 Figma 设计稿、网页交互 Demo 还是两者都要，未回复或无法询问时默认 `web-demo`。仅 PRD 有影响交付的冲突才额外询问。单独的评审请求不授权修改；已授权端到端生成不在每次内部审定后重复等确认。

## 完成标准

先看画板：**视觉效果**和**正式组件有没有用对**。运行记录用来恢复和抽查，不能代替截图，也不能因为缺某条 JSON 路径就否掉已经正确的稿。门禁只拦没读原文、该用的库组件没用上、没走复用阶梯就手绘、截图/视觉检查缺失、现网基线/裁切/双交付/内容三方证据缺失、换字体或解绑变量、P0～P2 仍开着。

## 表单状态约束

填写、选择、上传、授权勾选等信息收集场景必须应用 [表单校验时机](references/interaction-patterns.md#form-validation-timing)：未完成仅置灰禁用提交，不自动报错。初始态、填写中及清空后，不因空值、未选或未达最少字数显示红字、错误边框、警告图标或 Toast；说明需要时用中性辅助文案。真正错误统一用 Toast 说明原因和下一步，组件下方不生成行内错误文案、不预留错误占位，也不出现任何会顶开布局的提示；错误态需要单独呈现时另开画板或用浮层。此为用户明确的产品约束，适用于 Figma 和 Demo，不受交互模式中 heuristic 的默认分类降级。

## 核心协议

1. **视觉**：按 [设计规范](references/design-guidelines.md) 看层级、间距、对比和示意填充；截图是主证据。description 要求去掉的示意色必须从交付可见态拿掉。
2. **组件**：按 [现场组件解析](references/live-component-resolution.md) 先搜正式件，再试正式件组合，最后才自建。搜索未命中不等于缺口。按 [组件实例安全](references/component-instance-safety.md) 实例化、设变体和内容；禁止 detach、换字体、解绑变量、手绘冒充。
3. **体验与方案**：先按 [自适应执行分级](references/adaptive-execution-profiles.md) 选择最低安全档并允许运行时升级；再按 [PRD设计契约](references/prd-design-contract.md) 先把 Requirement 与 Solution 分开；进入页面地图前必须走 [体验决策契约](references/experience/experience-decision-contract.md)，基于 [产品体验模型](references/experience/product-experience-model.md)、[任务体验模式](references/experience/task-experience-patterns.md) 与经过验证的 [体验案例](references/experience/experience-case-contract.md) 做任务级判断。再冻结任务流、状态和职责；独立评审按 [任务模拟评审](references/experience/task-simulation-review.md) 与 [评审清单](references/review-checklist.md) 关闭 P0～P2。UI 状态只应用 [典型交互模式](references/interaction-patterns.md) 的 `when` 命中项。每个可见 unit 先定交互等级：单端用 `interactionLevel`，`both` 用 `interactionLevels`（Figma `design`、Demo `executed`）。
4. **实现**：plan 后再解析组件；同类槽位默认批量搜索、完整候选通过 description gate 后早停，build 后批量上屏并一次 read-back。记录跟上即可；按 [证据契约](references/evidence-contract.md) 能追溯用了哪些件、改了什么。脚本不代替设计判断，也不拦截 MCP。
5. **复评与交付**：独立评审先看截图。所有可见 unit 无论档位都必须过 [布局几何门禁](references/layout-quality-gate.md)、overflow、content、node-audit；修复后复验。`validate-run.py` 只核对覆盖和身份，不给视觉打分。blocked、必需 degraded 或问题未关不能 complete。

## 硬性不变量

以下任一不成立即不得 complete，也不能降级成建议项绕过：

1. **复用阶梯**：每个槽位先走 `formal-instance → compose → gap`。没有单个正式件就先用正式件组合（纯布局宿主 + 正式子件），并记录 `layoutOnly` 理由；只有前两级都耗尽、有结构化 `composeTrials` 和完整现场目录 `libraryCatalog` 证明，才可记 `gap`。顶层 `liveLibrary` 记录当次发布库身份与观察到的 `ids`，选中正式资产必须属于它；`libraryCatalog` 只用于证明缺口，不能替代 `liveLibrary`。搜不到、第一次语义搜索为空、没有一模一样的组件、外观相似都不构成 gap，更不构成手绘理由。
2. **现网基线**：复用现网已有屏幕或模式时，plan 必须给出 `liveBaseline`（现网节点/截图 + 关键几何、文案、状态）；build 后逐元素对照 `live/ours/delta`，超差要么修，要么写 `authorized` 理由。自建 compose/local 布局必须被基线覆盖。
3. **裁切与溢出**：每个可见 unit 都要有 overflow 检查，记录检查过的滚动/浮层/文本承载面，`escapes` 为空；中间容器不得误裁后代效果。
4. **内容三方**：内容脚本 → Figma 文案 → Demo 渲染逐项对齐；both 时三者必须在同一内容证据里，`mismatches` 为空。
5. **双交付对齐**：`deliverable=both` 时每个 unit 另有 parity 检查，引用 Figma 与 Demo 当次截图，元素/文案差异为零。
6. **视觉证据**：visual 检查必须引用当次截图；写入日志、导出 URL、人工摘要都不算视觉证据。
7. **独立评审**：必须由无历史继承的独立上下文完成；所需维度按 [自适应执行分级](references/adaptive-execution-profiles.md) 决定：Fast plan=`requirements+experience`、final=`ui`；Standard plan=`requirements+experience+ux`、final=`ux+ui`；Full 保持 plan=`requirements+experience+ux+ui`、final=`ux+ui+system`。reviewerId 不得等于 designerId；同一阶段同时存在 UX 与 UI 时必须不同评审者。`independent-review` 能力探测记录隔离机制与评审者身份；主执行者不得代写结论。P0～P2 finding 必须回指问题台账。
8. **输入分流、执行分级与体验冻结**：generate 必须先判定 `intake` 和 `executionProfile` 并通过 plan 门禁校验；文字输入先产出不含预设页面方案的 Requirement Spec/PRD 并登记 `source` 证据；上传 PRD 默认原文直读，用户明确要求改写时才可改写并登记授权证据。任何页面地图、Modal/Drawer/Page 选择、Screen Spec 或组件解析前，必须存在通过独立 Experience Review 的体验决策记录。任一不成立即不得 complete。
9. **页面复用复核**：generate（以及重跑 UX Freeze 的结构性 iterate）在 UX/UI Freeze 后、组件解析前必须建立 `referenceReview.status=reviewed`，并扫描原输入文件现有页面。参考范围至少覆盖现有页面、组件库精确页面 `【AI参考案例】Template` 内可匹配的子流程和用户本轮提供的 Figma 参考；每项登记 `kind=reference` 证据与 `matched / no-match / not-applicable`。命中时必须给出 `reuseAction`：同任务同状态且只需接入流程的记 `direct-reuse`，复用壳层/流程但改内容或状态的记 `adapt-reuse`，只借鉴局部的记 `reference-only`。直接或改造复用现有业务页面时，对应 unit 必须有 `liveBaseline`，输出仍落回原输入文件。页面复用不能替代组件身份校验，未复核不得进入组件解析或 complete。

历史材料意外暴露按“最小失效范围”处理：记录看到了什么、是否被采用及影响哪些决策，隔离后继续；不因普通执行者误见无关片段自动废弃整次任务。只有受污染的独立评审必须更换评审者，或无法排除旧方案已进入当前结果时，才重做相应阶段。

## 条件分支

- Figma：所有布局宿主先判断方向、双轴对齐、分布与尺寸；自建纯布局层无填充/描边/效果，各层表面按 [设计规范](references/design-guidelines.md) 判定视觉层级；锁定目标页；壳层 → 内容 → 操作区 → 浮层，完成后 [整理画布](references/canvas-organization.md)。
- MCP 缺字体：按 [云端字体配置](references/team-font-configuration.md) 先检查团队字体，缺失时从随包 `assets/fonts/` 定位匹配字体，走当前账号上传；无电脑操作能力则给用户具体上传步骤，验证后继续。
- 对话/生成式回答：读 [对话内容域](references/conversation-content-domain.md)。
- 自建缺口：读 [缺口组件创建](references/missing-component-creation.md) 和 [基础规范](references/foundations/index.md)。
- 网页原型（未指定交付物时的默认值）：读 [网页Demo交付](references/web-demo-delivery.md)。组件库预览以 `demo/README.md` 为准；独立业务 Demo 用 `node scripts/scaffold-demo.mjs <slug> --run-dir <task-run-dir>` 生成到任务工作区的 `standalone-web/<slug>/`（复用安装包 `demo/src` 封装与 `demo/public`），不写进 Skill 包，也不注册 `registry.ts`。
- 实际体验：读 [交互验证](references/interaction-validation.md)。Figma 仍画交互后的静态状态屏；可点走查在 Demo。

## 停止与维护

用户暂停或缩小范围时保存进度。无法继续的业务决定、能力限制或连续无进展修复按完成门禁暂停，明确未完成；不靠降低分级结束。

仓库稿是编辑源。修改后运行结构校验、运行门禁测试、[工作流场景](evals/workflow-scenarios.md) 与 [体验质量场景](evals/experience-quality-scenarios.md)；前者防流程回归，后者验证任务级设计判断是否真的变好。安装副本必须与仓库一致，先用 `scripts/validate-skill.py --check-install` 比较并备份；命令见 [使用说明](docs/usage-guide.md)。任务产物写入当前任务工作区，不放进安装包。
