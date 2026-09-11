# 网页交互原型交付接口

以下布局/视觉模式仅在现场团队规范可追溯且场景命中时作为 team-rule；无依据时为可解释调整的 heuristic，不以本文措辞独立阻断。工具限制、实例身份保护和需求覆盖仍为硬性不变量。规则分类见 [采集与验证契约](capture-and-validation.md)。
本文件只规定工作流与 Demo 工程的接口，不规定任何 React 组件的视觉、CSS、token 或内部实现。

## 输入

网页交互原型必须复用：

- 已确认的 PRD 冻结包；
- 抽象槽位与现场组件解析证据；
- 状态矩阵；
- 内容脚本；
- 设备、画布与适配要求。

不得在 Demo 分支重新选组件或让代码结构反向决定 Figma。只出 Demo、不出 Figma 时，仍按同一套槽位证据和内容脚本实现，不能另起一套页面结构。已有 Figma 再补 Demo，或已有 Demo 再补 Figma：直接复用槽位证据、内容脚本和 `chosenLiveKey → generatedExport` 映射，按已有稿的屏、层级、元素和文案铺另一端，不要重新发明信息架构。

## 目录选择

用户未明确交付物、或无法询问时，默认 `deliverable=web-demo`，按本文件交付可交互网页原型；用户明确要 Figma 或 both 时不要用 Demo 顶替。

| 用户要求 | 产物位置 | 禁止 |
|---|---|---|
| 组件库预览（人工查看） | `demo/`，按 `demo/README.md` 注册 `?screen=` | 无 |
| **独立业务 Demo**（`web-demo` 交付的默认产物） | 任务工作区的 `standalone-web/<slug>/` 独立 Vite 应用 | **禁止**写入 Skill 包的 `demo/src/screens/registry.ts`，也不把业务 Demo 留在 Skill 包里 |

独立应用通过 alias 复用 `demo/src` 正式封装和 `demo/public` 图标，不复制组件实现。机外 chrome 放场景/主题切换，机内只放业务页。用 `node scripts/scaffold-demo.mjs <slug> --run-dir <task-run-dir>` 生成骨架（slug 必须以小写字母开头，只能含小写字母、数字和连字符，避免生成非法组件名）：脚本复制 `assets/standalone-web-template/`，把模板里的中文占位名（页面名、组件名、Demo 路径）替换成实际项目名和安装包 `demo/` 的绝对路径，并生成 `standalone-web/<slug>/src/screens/<slug>.tsx` 占位页；生成后按槽位证据填页面，不要改模板去重画正式组件。模板本身依赖 `@demo`/`@app` 别名和安装包依赖，直接打开 `assets/standalone-web-template/index.html` 会是空白；必须先 scaffold 到任务工作区再运行。

## 实现边界

- 每个已解析正式槽位映射到对应的正式生成封装及现场验证过的合法 props。
- 先验证 Demo 当前 manifest 的设计库身份与 Session live library 一致，再按 `chosenLiveKey → manifestAssetKey → generatedExport` 映射；禁止只按名称猜。
- 名称相同但 live key 与 `demo/src/generated/assets.ts` 的 `assetKey` 不一致时，记组件库同步问题：`mapping.manifestAssetKey` 必须等于本地 `assetKey`，`chosenLiveKey` 保留当次 live key，并另记 syncMismatch（type=identity-migration、reason、evidenceRefs）；证据含 fromKey/toKey 及 schema/dependencies/visual 的 before/after 非空相等指纹；Demo 仍用正式封装，不要手绘绕过，也不要把错误 key 写进 Skill。
- 映射后的 props schema 必须覆盖槽位证据中的合法公开属性。
- **内容对齐（与 Figma 同一套改法）**：Figma 里改嵌套文字、占位、trailing 图标、空态插画、按钮文案的地方，Demo 用同一正式件的内容 props 改，不在页面层重画。至少对齐：`children`（标题/主文案）、`placeholder` / `value`、`subtitle` / `trailing` / `trailingKind`、`illus` / `descText` / `buttonLabel`、`bodyText` / `primaryLabel` / `secondaryLabel` / `primaryType`。generated `*Props` 若只有 Variant/布尔，把这些内容字段作为 extra values 传进 renderer；缺字段记为组件库实现缺口，在已授权维护范围内补 renderer 与 `CommonAssetProps`；否则在任务隔离副本修复并交付补丁，不改安装包，不要在页面手绘。
- 页面层只做业务组合与交互状态，不重画已有正式组件。
- `gap` 只实现已登记的真实缺口，且必须先走完 `formal-instance → compose → gap`：纯布局宿主 + 正式子件记 `compose`，不因“没有单个正式件”就在页面手绘本地件；Web Demo 与 Figma 共用同一份槽位证据、`reuseLadder` 和 `libraryCatalog`，不能一端省步骤。
- manifest 版本不一致、缺正式封装或 schema 漂移时为 `blocked`，scope 记为 `demo`；它不是 Figma gap，也不能用页面自绘绕过。
- 组件外观和 token 由 Demo 组件库维护；不一致时记录为组件库实现问题，不把修复配方写回本 Skill。
- 组件库目录 Demo 的命令仍以 `demo/README.md` 为准；独立 Demo 以该目录 `package.json` 的 `npm run dev` 为准。

## 页面壳

网页 Demo 的页面组合必须是 auto-layout：viewport 内设备画布、内容柱、模块列和浮层内容槽用 flex 关系排列，不用绝对坐标拼装主结构。按 [设计规范](design-guidelines.md) 保持与 Figma 相同的容器职责、表面区分、双轴对齐和分布意图；flex 主轴随方向变化，不能把所有行列套同一套默认对齐。

- 设备画布在视口中居中，并缩放到当前一屏可见；预览控件（场景、主题、返回）放在机模外的空位，不占用机模内部高度。机外 chrome 应能切到与 Figma 交付屏一一对应的状态（默认、搜索命中、无结果、空、弱网、浮层、轻提示）。
- 缩放与居中由 `screens.css` 的 `.screen-demo-stage > [data-canvas]`（含 `:only-child` 兜底）统一接管，页面不要自己写舞台定位。业务页根节点必须是 `HostCanvas`（自带 `data-canvas`），并挂 `screen-demo-canvas` 取得 402×874 机模尺寸；`App` 拥有 `DemoShell` + `HostCanvas`，业务 screen 只写画布内容，不要再套一层 `DemoShell` / `HostCanvas`。漏挂框架类的表现是内容按内容高度收缩、超出舞台的部分被 `overflow: hidden` 裁掉。
- 页面边距落在**内容层**（卡片、文本框、列表），不改正式组件内部间距；内容柱随内容增长，需要滚动的区域保持滚动能力。
- 贴边壳层（顶栏、长按条、锁定操作条、系统键盘、Tab）铺满设备画布，父级左右 padding 为 0。禁止把内容柱的左右 padding 套到同时包含着这些条的容器上，否则底栏会比画布窄一圈。内容内收用独立包装，不要让输入卡片为了迁就底栏而贴边。命中时按 [设计规范](design-guidelines.md) §5.1 与 `edge-chrome-vs-content-inset`。系统键盘另命中 `system-ime-keyboard`：映射已发布的系统输入法键盘正式封装，禁止页面手绘键帽。
- Figma 没有系统滚动条的区域，Demo 也不显示系统滚动条；只有设计稿里的滚动轨道才保留为可见轨道。
- 仅现场 description 允许填充的正式组件按父级填充；固定、hug、居中等按 Screen Spec 和正式约束，禁止为了通栏强制 stretch 或撑破容器。
- 受控输入：`value=""` 是合法空值，不能回落到组件库示意文案（如搜索默认「元宝」）。空值不显示清除。占位文本只出现在现场空态公开属性组合里；不要把已填编辑态套到空占位上。
- 落地页空/弱网缺省与 Figma 相同：相对整机画板垂直居中，不要在顶栏下方剩余列里居中。
- 截图前读机模主题属性确认 Light 主交付。机外主题按钮写的是「下一主题」，不能凭按钮文案判断当前是浅色还是深色。

## 验收

- 槽位证据与 Demo 映射一一对应；
- Demo Mapping Evidence 已记录 manifest 身份、live key、正式导出和 schema 校验；
- compose 槽位中每个 chosen asset 都有且仅有一条 mapping，slotBindings 已验证；
- 主要状态和恢复路径可在浏览器走通；
- 关键组件与当次 Figma 现场截图/description 一致；示意填充同样不得留在交付可见态；
- 内容脚本、Figma 文案和 Demo 渲染三方逐项一致，差异证据 `mismatches` 为空；
- 页面滚动、浮层和文本承载面做过溢出/裁切断言，`escapes` 为空；
- `both` 时每个 unit 有 Figma 与 Demo 当次截图的 parity 对照，元素和文案无差异；
- 已解析正式槽位没有用截图、占位或自绘外观冒充完成；
- 设备画布一屏居中可见，预览控件在机外；内容卡片不贴边、不撑破，贴边壳层铺满画布；
- 无设计滚动条处无系统滚动条，需要滚动的区域仍可滚动；
- blocked/degraded 单列；
- Demo 工程自身验收通过。
- 独立 Demo 未写入组件库 `registry.ts`。

`both` 时，Figma 与 Demo 是同一套屏：结构、层级、元素、文案对齐。unit 记 `interactionLevels={figma: design, demo: executed}`；Figma 交静态状态屏（含点击后的页面），能点的走查记在 Demo。不要因为 both 就把 Figma 伪造成 `executed`，也不要因为 `design` 就少画交互后的屏。

## 严格渲染与移交

独立模板使用 RenderPolicyProvider 的 deliverable-strict。组件工作台 catalog-preview 可截图兜底，业务交付禁止；严格模式缺 renderer、非正式资产、身份歧义和非法公开属性值会失败。renderer-bindings.json 将稳定 assetKey 映射到本地实现，名称仅用于展示及唯一解析。本地检查不等于 live 视觉验证。

导出：`node scripts/export-demo.mjs <应用目录> <新的移交目录> --verify`，复制本地库为相对 vendor 快照并在输出目录生成锁文件、npm ci 与构建。原始应用不改。delivery-manifest.json 记录快照哈希和构建状态，视觉/真实 MCP 单独验证。保留字体和资源授权边界。
