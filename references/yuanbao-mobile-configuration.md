# 元宝移动端配置

本文件只保存稳定的团队环境与治理政策，不保存组件 key、Variant、token 值、组件配方或视觉参数。

## 设计系统

- 规范源（只读）：`iUyH8VSdURxlGrhp646zYJ`
- 发布库名称：`📱 元宝移动端组件库-2026`
- 每次任务对目标文件调用 `get_libraries`，按名称精确匹配并记录当次 libraryKey。
- `search_design_system` 走的是已发布库索引。规范源里改过的 description 必须由设计师发布后，其它文件和 generate 才能搜到。
- 其它移动端、PC、社区或草稿库不参与自动选型，除非用户明确授权。

## 默认目标

- 默认业务写入文件：`TU15hLT7Oz5RaTtSpGMqa6`
- 用户指定文件时以用户目标为准。
- 新建 Figma 业务页使用 `【AI禁止参考】[业务名]`。
- `Cover`、其它 `【AI禁止参考】*` 和历史 AI 稿不作为参考。
- 组件库 Template 只在 UX 冻结后用于同类页面复用，不能覆盖 PRD，也不改变业务写入目标。

## 组件库 Template 页面复用

- 组件库源文件（只读）：`iUyH8VSdURxlGrhp646zYJ`
- 发布库名称：`📱 元宝移动端组件库-2026`
- Template 参考页面名称：`【AI参考案例】Template`
- Template 页面由组件库维护；pageId/nodeId 以组件库现场为准，Skill 不写死节点。必须按精确页名 `【AI参考案例】Template` 定位，不能拿其它名称相似的页面替代。页面内部可包含多个流程/Frame；实际匹配对象可以是其中一个子流程节点，`pageName` 仍记录精确页面名，`nodeName/nodeId` 记录命中子流程。
- 读取时机：Experience Review 通过且 UX/UI Freeze 后、组件解析前。先用当次 `get_libraries` 枚举组件库页面，再读取 `【AI参考案例】Template` 及其相关子流程。
- 匹配依据：同时看任务模型、页面壳层、步骤关系、状态结构和信息密度，不能只凭名称相似。名称相同也要检查实际内容。
- 复用边界：组件库源页只读，禁止修改、移动或直接在源页上写业务稿。复用结果只落到原业务输入文件；业务组件仍须从当次发布库现场解析并正式实例化，不能把 Template 中的旧实例当成正式资产身份。
- 未命中：记录 `no-match` 和理由后按正常流程生成。页面尚未创建或工具无法读取页面时，记录 `not-applicable` 或阻断原因；不得要求用户重复提供已登记的组件库链接。
- 记录：写入 `referenceReview.sources`，保留当次 `kind=reference` 工具证据、实际页面/子流程身份和匹配结论。
- 用户提供的 Figma URL 默认是参考文件，不等于业务写入目标；只有用户明确说“在该文件里出稿”时才改变写入目标。
- 用户提供参考文件时解析 `fileKey` 和 `nodeId` 后直接读取；Skill 已登记或本轮用户已给出的链接不得再次索要。
- 组件库 Template 属于设计/结构复用来源，不是 `verified-only` 的 Experience Case；只能在 UX 冻结后用于实现方案复用。

## 页面级复用阶梯

页面和组件分两层判断。页面先决定“用哪个已有页面/流程”，组件再决定“用什么正式组件实现”。页面级顺序固定：

1. **原输入文件现有页面**：扫描顶层页面名称、ID 和可见结构，找与当前任务步骤同类的页面。现有页面可以直接成为新流程的一步，也可以作为后续新增页面的壳层、导航、状态和内容连续性提示。
2. **组件库 `【AI参考案例】Template` 子流程**：在精确页面内查找任务或名称相近的流程，判断能否直接使用、改造后使用或只借鉴局部。
3. **用户参考页**：仅作为用户已明确提供的补充来源。
4. **新页面**：前三层都不成立时才新建。

每个命中页面必须给出：

- `direct-reuse`：任务、步骤和状态基本一致，只调整它在流程中的位置或连线；`changeScope` 只能含 `flow-order`。
- `adapt-reuse`：页面壳层、主流程或状态结构可复用，但内容、状态、外层布局、导航或适配需要修改；`changeScope` 必须列出实际改动。
- `reference-only`：只借鉴局部结构、连续性或提示，不把来源页面当实现主体。
- `no-match`：同类性不足，不硬套。

直接复用或改造复用原输入文件里的现有页面时，对应 unit 必须使用该页面作为 `liveBaseline`，交付时对照来源与结果。作为复用来源读取时页面只读；如果来源节点本身已在授权输出范围内且本轮任务就是修改它，可以原位修改，但必须登记同一 source/target 身份并保留 pre/post 证据。需要独立版本时，在授权目标内复制/重建，不修改来源页。

## 交付物

- `figma`：设计稿。
- `web-demo`：可交互网页原型（不是静态截图或组件库预览）。
- `both`：共用同一 PRD 冻结、槽位证据和内容脚本。
- 生成前必须先问用户要哪一种；用户已在请求或 PRD 中明确时直接采用。用户不回复、跳过问题或无法询问时默认 `web-demo`，并登记 `intake.deliverableDecision`，规则见 [输入分流](input-routing.md) 第 1.1 节。
- 设备类别、画布尺寸、适配范围来自 PRD、目标文件和现场正式模板；不要用旧项目常量代替现场证据。

## 写入与字体

- 规范源、发布库主组件和默认内容只读。
- 正式实例保持原字体、变量、样式和内部结构。
- MCP 字体不可用时按 [云端字体配置](team-font-configuration.md) 先团队后账号恢复，恢复前阻断受影响写入；禁止替换字体规避缺失；已授权随包字体按云端字体配置定位、校验和上传。


## 体验决策配置

- `experiencePlanning.required=true`：generate/结构性 iterate 在页面地图前必须形成 Experience Decision Record。
- `experienceCases.policy=verified-only`：只有人工认证的结构化体验案例可在体验决策阶段引用；未经认证的 AI 稿与探索稿禁止作为先例。
- `experienceCases.visualAccess=after-ux-freeze`：默认只读案例中的任务、约束、备选、理由和结果，不在体验冻结前读取最终视觉/组件树。
- `experienceReview.pairwise=preferred`：存在两个实质可行方案时优先做 A/B 任务级比较，不用绝对分数代替判断。
- `experienceReview.simulationRequired=true`：至少覆盖 happy path、first-use、error、interrupt、post-success。
