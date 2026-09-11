# 元宝移动端组件 React Demo

设计团队本地 Demo，对应 Figma 文件 `iUyH8VSdURxlGrhp646zYJ`。

这些 React 实现用于设计验证和 AI 生成 Demo，不是公司生产前端代码，也不发布到 Figma Dev Mode。Figma 选型以现场 description 为准，本目录不能覆盖现场描述。

Markdown 回答流组合见 `../references/conversation-content-domain.md`（Figma 对话页与 Demo 都可读；变体以现场 description 为准）。

## 本地运行

```bash
npm ci
npm run dev
```

依赖目录不随包分发；按锁文件执行 `npm ci` 后再运行。`node_modules`、`dist` 和 `code-connect-docs.json` 不进仓库，需要时再装、再编。

组件目录支持搜索、Light/Dark、属性切换、交互预览和 JSX 复制。

## 组件工作台

组件目录使用三栏布局，保留原有组件渲染器及属性约束：

- 按组件、图标筛选，支持组件名、导出名和 Node ID 搜索。
- 属性按变体、开关、插槽分组，支持重置和代码同步。
- 收藏保存在当前浏览器中；组件直达链接使用 `?asset=<nodeId>`。
- 预览默认不放大普通组件，图标适应模式最大为 400%；可手动缩放。
- React 示例区可收起；窄屏使用目录、预览、属性三个视图。

浏览器回归使用已有 Playwright 安装，不修改组件库依赖：

```bash
CATALOG_URL=http://127.0.0.1:5180/ \
PLAYWRIGHT_MODULE=/absolute/path/to/playwright/index.mjs \
node scripts/test-catalog-ui.mjs
```

默认截图和结果存放在系统临时目录 `yb-mobile-design-catalog-test/`。测试需要本机 Chrome
和已启动的 Demo 服务；`PLAYWRIGHT_MODULE` 可在当前环境已安装 Playwright 时省略。
`vite.config.ts` 把 dev/preview 端口固定为 5180（`strictPort`），避免自动换端口后与 `CATALOG_URL` 不一致。

## 页面级 Demo

- 不带 `screen` 参数时显示组件目录。
- `?screen=agent`、`?screen=source-outreach`、`?screen=feedback` 打开三个内置演示页。
- 三个内置演示是组件库功能，清理历史任务时必须保留。
- 新任务生成的独立业务 Demo 放在任务工作区，不继续累积到这里。
- 独立业务 Demo 用 Skill 根目录的 `node scripts/scaffold-demo.mjs <slug> --run-dir <task-run-dir>` 生成；模板复用本目录 `src` 与 `public`，不写进 `src/screens/registry.ts`。

## 校验

```bash
npm run generate
npm run typecheck
npm run test:strict-render
npm run lint
npm run build
npm run code-connect:compile
```

`test:strict-render` 用 SSR 渲染核对身份、非法变体、正式资产 renderer 覆盖、未发布资产拒绝和 catalog-preview 兜底边界。
`code-connect:compile` 只在本地验证模板，不会发布任何映射。

## 本地资料

- `data/figma-components.json`：195 个正式资产及属性快照
- `data/extra-icon-nodes.json`：`src/generated/extra-icons.ts` 的 145 个补充图标来源清单（当前未接进生成脚本，改动补充图标时对照）
- `src/library/catalog.ts`：`publishedCatalog` 是发布库资产，`supplementalCatalog` 的补充项标 `published=false`；补充项不能替代 `liveLibrary.ids` 选型
- `src/generated/assets.ts`：本地资产注册表
- `src/generated/components.tsx`：195 个 React 导出与 Props
- `src/figma/*.figma.ts`：本地 parserless 模板
- `code-connect-docs.json`：本地编译结果
- `code-connect-mappings.json`：本地映射清单
- `src/tokens.css`：185 个本地 CSS token 和 Light/Dark 值

## 组件更新时

1. 用 `$yb-mobile-design` 重新扫描最新版 Figma 组件、属性和变体。
2. 将新的 `list_file_components_for_code_connect` JSON 更新到 `data/figma-components.json`。
3. 运行 `npm run generate`。
4. 检查生成差异；如果只改视觉或 token，通常不需要修改 Props。
5. 如果 Variant、Boolean、Slot、属性名或 node ID 改变，更新受影响的 React 行为并重新执行全部校验。

Figma 内保留中文组件与 Variant 描述，供设计同学直接维护；代码模板与 CSS token 只在本目录维护。

`.figma-token.json` 已加入 `.gitignore`，不会被生成脚本读取，也不应提交到仓库。
