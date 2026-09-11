# example-page 独立业务 Demo

由 `scripts/scaffold-demo.mjs` 从 `assets/standalone-web-template/` 生成，复用安装包 `demo/src` 正式封装和 `demo/public` 资源，不复制组件实现，也不写入 `demo/src/screens/registry.ts`。

这是模板，不是可直接打开的页面：它依赖 `@demo` / `@app` 别名和安装包 `demo/` 的依赖，直接双击 `index.html` 只会空白。必须先生成到任务工作区再运行。

## 运行

```bash
npm install
npm run dev
```

dev/preview 固定端口 5181（`strictPort`）。按槽位证据实现 `src/screens/example-page.tsx`：只组合 `@demo/generated/components` 的正式封装和现场验证过的合法 props；页面层只做业务组合与交互状态。

## 页面壳契约

- `src/App.tsx` 已经提供 `RenderPolicyProvider` + `DemoShell` + `HostCanvas`，并且 `HostCanvas` 挂着 `screen-demo-canvas`；业务 screen 只写画布内容，**不要再套一层 `DemoShell` 或 `HostCanvas`**，否则外层舞台会裁掉内层内容。
- 舞台按 `--demo-phone-w/h`（默认 402×874）定尺寸并 `overflow: hidden`，缩放与居中由 `@demo/screens/screens.css` 的 `.screen-demo-stage > [data-canvas]` 接管，业务页不要自己写 `position: absolute` / `transform: scale(...)`。
- 页面根节点换成自建类名时仍会被缩放，但只有 `screen-demo-canvas` 带机模尺寸和表面底色；内容超出机模的部分需要画布内自己滚动。

## 验收

```bash
npm run typecheck
npm run build
```

组件外观和 token 由安装包 `demo/` 维护；不一致时记录为组件库实现问题，不改本 Skill 的组件实现。
