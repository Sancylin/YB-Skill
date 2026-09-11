# 使用说明：yb-mobile-design

## 直接使用

**文字需求**（没有 PRD 文件）：

> 使用 $yb-mobile-design，把「做一个任务列表页，三条任务带标题、描述、状态和进度，健身任务带图」做成设计稿或网页 Demo。

期望：先问清要 Figma 设计稿、网页交互 Demo 还是两者都要；没有回复或无法询问时默认网页交互 Demo。然后产出一份只冻结问题与约束的 Requirement Spec/PRD（不由 AI 预设页面地图或 Modal/Drawer/Page），再进入 Experience Decision 做任务模型、候选取舍和任务模拟；体验冻结后才解析组件并出稿。要“先看 PRD 再出稿”就明确说，否则 PRD 产出后连续执行。

**已有 PRD**（上传或给出 PRD 文件）：

> 使用 $yb-mobile-design，按这份 PRD 直接出 Figma 设计稿，不需要总结和优化。

期望：原文直读，不总结、不精简、不改写、不扩写、不重排结构；需求逐条回指原文位置。需要精简 / 改写 / 总结这份 PRD 时直接说，按其要求执行并登记授权证据；两者同时提供时保留文件原件，最新明确用户变更通过变更单优先生效。链路见 [输入分流](../references/input-routing.md)。

交付物必须先问：用户明确 Figma / web-demo / both 时直接采用；不回复或无法询问时默认 `web-demo`（网页交互 Demo）。已授权端到端任务不会停在方案冻结或盲审交接包。业务规则冲突、缺必要材料或工具能力时，AI 给出具体恢复入口，不能冒充完成。单独说“评审已有稿”仍然只评不改。

## 链路与文件

- [主入口](../SKILL.md)：模式选择与核心协议。
- [输入分流](../references/input-routing.md)：先问交付物（未回复/无法询问默认 web-demo）；文字需求先产出 Requirement Spec/PRD，上传 PRD 原文直读；随后执行 Experience Decision；`intake/plan` 门禁。
- [自适应执行分级](../references/adaptive-execution-profiles.md)：自动选择 Fast / Standard / Full，允许运行中升级；Fast 减少推理/评审轮次但不降低布局、截图和组件身份门禁。
- [布局几何门禁](../references/layout-quality-gate.md)：所有可见 unit 检查 Auto Layout、padding/gap、对齐与实际几何，防止简单需求的版式细节错误。
- [自动编排](../references/orchestration-and-completion-gates.md)：阶段、授权、恢复、三道门禁。
- [需求契约](../references/prd-design-contract.md)：原文追溯、职责树、UX/UI 方案与专家职责。
- [现场组件解析](../references/live-component-resolution.md)：实时 description、完整候选、组合和最小缺口。
- [运行记录](../references/run-record-format.md)：证据文件、实际命令、盲审包和版本关系。
- [评审清单](../references/review-checklist.md)：分级、内容、视觉、系统与修复复验。

Skill 不保存组件 key、色值、字号和变体配方。基础规范、属性和组合关系仍从现场获取；libraryKey 只表示身份，内容更新需核对版本/指纹。默认 `web-demo` 时，独立业务 Demo 用 `node scripts/scaffold-demo.mjs <slug> --run-dir <task-run-dir>` 生成到任务工作区，不写进安装包。

## 运行门禁

从源码目录执行示例命令；安装使用时，把脚本替换为 Skill 内绝对路径，将运行记录放在当前任务工作区。

```text
python3 scripts/validate-run.py --init artifacts/my-design-run
python3 scripts/validate-run.py artifacts/my-design-run/run.json --gate plan
python3 scripts/validate-run.py artifacts/my-design-run/run.json --gate build
python3 scripts/validate-run.py artifacts/my-design-run/run.json --gate deliver
```

init 创建未完成骨架，AI 需要随实际工作填写并取证；骨架检查失败是预期行为。证据必须保存在本次运行目录，使用 --add-evidence 计算哈希登记；具体格式看运行记录。

完成以视觉效果和正式组件调用为准。plan 先校验 `executionProfile` 不低于最低安全档，再按 profile 检查所需独立评审；build 检查原输入文件页面是否已扫描、组件库 `【AI参考案例】Template` 和用户参考是否已复核、命中页面是否按直接复用/改造复用/仅参考作页面级决策、直接或改造复用现有页面时是否有匹配 `liveBaseline`，再检查是否搜过并选对组件、选中件是否属于当次 liveLibrary；Fast 遇到真实 gap/复杂 compose 会要求升级；deliver 对所有 profile 都检查实例是否在稿上、visual 是否引用当次截图、`layout-geometry` 是否通过、内容是否对齐、overflow 是否无逃逸、现网复用是否有 baseline 对照、both 是否有 parity、组件身份有没有被破坏、P0～P2 是否关闭。有效旧页面既可接入新流程，也可为后续新页面提供连续性提示；业务输出始终回到原输入文件，来源页只读。脚本不给视觉打分，也不鉴定证据真伪。缺白名单路径或快照多字段不应否掉已经正确的稿。历史误报通过 supersedes 关联新评审，原报告保留。

## 能力要求和完成边界

设计生成需要可访问的 Figma 发布库、适用写入/导出工具、实际字体和 Slot 能力；独立盲审需要无历史继承的评审上下文。缺少这些能力会明确阻断，不能用同上下文换角色冒充盲审。

脚本在本地校验记录及不变量，不会替你调用 Figma，不鉴定证据是否伪造，不判断所有 UX 语义，也不在工具层拦截绕过 Skill 的写入。当前没有后台自动唤醒服务；中断恢复依据保存记录和现场核对。

其它运行的 artifacts 必须按本次证据契约重新核验。不能把旧稿的 P1=0 转成当前完成，也不能用 Demo 成功抵消 Figma 未写入真实文案。

## 执行分级与测量

不要把所有 generate 都跑成 Full。初始路由只选择当前最低安全档，之后按证据升级：

- Fast：已有 task model 上的 1–2 个局部增量、无 IA/导航/权限/高风险/长异步/部分成功；默认 2 次 reviewer 调用（plan requirements+experience 合并一次，final ui 一次）。
- Standard：新任务/新模式但无高风险系统变化；默认 3 次 reviewer 调用。
- Full：结构性或高风险变化，保留完整审计。

组件检索仍以 Figma 为唯一真相源，但同类槽位默认批量搜索、完整候选通过 description gate 后早停，同一 live library 指纹下复用本轮已读证据；只有证明 gap 才进入全量 Inventory。build 后优先一次批量 read-back + 一次截图评审，不逐节点往返。建议在 run 中记录 `timeToFirstUsableDraftMs / figmaSearchCalls / figmaReadCalls / reviewCalls / fixAttempts / profileEscalations`，先优化第一版可用稿时间。

## 维护和测试

```text
python3 scripts/validate-skill.py
python3 scripts/validate-skill.py --demo-check
python3 -m unittest discover -s tests -v
python3 scripts/validate-skill.py --check-install
```

结构校验只检查入口、引用、文件与包规则；`--demo-check` 额外验证 `npm run generate` 可重复，`demo` 的 typecheck/build 与 `test:strict-render` 通过，需要先在 `demo/` 执行 `npm ci`。测试使用显式 fixture 验证门禁反例，不能替代真实 MCP 端到端回归。人工/独立行为场景见 [工作流场景](../evals/workflow-scenarios.md)。

维护工具：`scripts/audit-library.py <local> <live> <output>` 按 `nodeId` 比较本地快照与现场目录，把同 nodeId 换 `assetKey` 记为 `rekeyed`（身份迁移，不是删除），schema 一致不等于视觉一致；`scripts/compare-evidence.py` 做内容/集合比较；`scripts/migrate-run.py` 只转换 schemaVersion=2 的运行记录结构并标 `needs-recapture`；`scripts/export-demo.mjs <app> <new-output> [--verify]` 把独立 Demo 导出为自带 `vendor/yb-library` 的干净目录，`--verify` 只证明可构建，不证明视觉或 live 一致。

只读已有稿评审或单独独立复评使用 `python3 scripts/validate-run.py artifacts/<run-id>/run.json --gate report`；只读模式不执行 build/deliver，缺原 PRD 时在报告中单列业务需求 coverage 未知。报告允许 `verdict=issues`，但每个 P0～P2 finding 必须回指问题台账，并附每个可见 unit 的当次截图。

## 真实 MCP 回归清单

脚本测试用 fixture，不能替代真实 Figma 端到端。每次改动工作流后，在有权限的账号上按下列清单人工/独立代理走查并记录状态，未执行的项目单列，不能用模拟替代：

1. `get_libraries` 能精确定位当次发布库，`liveLibrary.libraryKey/version/fingerprint/observedAt` 与现场一致；
2. `list_file_components_for_code_connect` 能按当前接口列出到结束，发布的根 Component/Component Set 数与 `libraryCatalog.ids` 一致，且能证明 `chosenAssets ⊆ liveLibrary.ids ⊆ libraryCatalog.ids`；
3. `search_design_system` 语义检索命中/未命中都能被描述门禁复核，两次无果后能走 `published-name` 兜底；
4. `get_design_context` 能读到 description、公开属性、Slot 与库归属，读不到时按 `blocked-insufficient-evidence` 处理而不是判 gap；
5. `get_screenshot` 能导出当次截图，visual 与 both parity 都能引用；
6. 授权范围内能新建正式实例、设公开属性、写 Slot 和外层布局，且 pre/post 快照身份未被破坏；
7. 字体、变量/样式、Slot 与实例迁入 auto-layout 的真实写入通过；
8. 独立评审使用无历史继承的上下文，隔离证据 `isolated=true` 且评审者不同于 designerId；
9. 无 PRD 的授权修复能按 [模式-迭代](../references/mode-iteration.md) 的路径登记授权 source 并派生 requirements；
10. `paused-blocked` 恢复后能从保存点继续，未关 P0～P2 不会因轮次或时间自动通过。

把每项写成通过/受阻/未执行 + 证据位置；只有全部通过且截图视觉、正式组件调用成立，才把真实端到端回归标为通过。

仓库是编辑源。同步已有安装副本前比较差异并备份，按 `scripts/validate-skill.py` 的 managed_files 白名单同步（含 SKILL.md、references、agents、scripts、tests、evals、docs、assets、demo 源码与资源；排除 node_modules、dist 和历史产物）。默认安装对比目录为 ~/.codex/skills/yb-mobile-design，可用 --install-root 指定其他安装位置。没有正式验证的线上能力要在评审报告中单列。

## 团队字体与文案写入

优先使用团队共享字体；团队未配置或没有上传权限时，改走当前 Figma 账号上传。有电脑操作能力的 AI 可在授权范围内完成官方上传；没有该能力时给用户缺失字体、文件路径和 Settings → Account → Your uploaded fonts → Upload fonts 步骤，保存进度，待用户上传后验证并继续。账号必须与 MCP 一致，个人上传不等于团队共享。上传成功不能替代 MCP 实测。见 [团队字体配置](../references/team-font-configuration.md)。

## 目录与分发

运行核心为 SKILL.md、agents、references 和 scripts/validate-run.py。scripts/validate-skill.py、tests、evals 和本说明用于维护回归，保留但日常任务无需通读。只加载索引命中的模式/阶段资料，运行证据写在任务工作区。

Demo 源码、资源和锁文件支持网页原型，不能作为无用附件删除；node_modules、构建产物和系统缓存可重建，首次使用 Demo 先按其 README 安装依赖。历史运行截图、备份和评审报告不属于分发包。随包体积主要由 `assets/fonts/`（约 38MB）和 `demo/`（约 31MB）构成：它们分别支撑缺字体恢复和默认 `web-demo` 交付，只有部署环境能保证等价能力时才可裁剪，并在评审报告单列。

`scripts/package-skill.py` 按 validate-skill.py 的 managed_files 白名单打包，包含执行规则、校验脚本、测试、使用说明、assets/fonts 随包字体以及 `demo/` 工程（含 195 个正式资产的本地 React 封装）。`web-demo` 是默认交付物，Demo 工程不能从分发包删除；`demo/node_modules`、构建产物和历史运行记录不进包。

分发时保留 Skill 根目录及 assets/fonts 相对结构，可打包为 ZIP；同结构 ZIP 另存为 .skill 供支持该格式的客户端导入，不代表所有客户端都支持。解包后先运行 scripts/validate-skill.py 核对字体完整性；字体仅按需上传 Figma 云端，不需要将二进制读入模型上下文。


## 体验能力回归

评测包含 `evals/workflow-scenarios.md` 和 `evals/experience-quality-scenarios.md`。工作流回归检查“有没有漏/有没有违规”，体验质量评测优先使用 pairwise human preference 检查“两个都能完成的方案里哪个体验更好”。修改 Experience Planner、案例库或任务模式后两套都要跑。
