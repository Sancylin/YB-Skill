# 状态与降级

三个状态不能混用。

## `blocked`：选型硬停

触发：

- description 及合法继承规则无法证明用途或禁用边界；
- 无法证明 owning parent、合法变体或属性组合；
- 只找到内部组件、旧库或禁用资产；
- 用户缺少会改变方案的必要选择。

行为：记录 `scope`（选型、Figma 写入、Demo 映射等）、缺失证据和恢复入口；不实例化、不手绘替代、不宣称完成。换候选、请求补 description 或向用户询问。一个交付物 blocked 不自动等于另一个交付物存在 gap。

## `degraded`：实现软降级

触发：

- 当前 `family + style` 不在 `listAvailableFontsAsync()`；
- 允许的 TEXT Property 或目标页 `characters` 写入失败；
- 无法把节点放进 auto-layout 父级（例如字体未加载导致 `appendChild` 失败）；
- 平台权限或工具能力阻止某项内容，但结构与组件选型仍可正确完成。

文本写入按 [component-instance-safety.md](component-instance-safety.md)；缺字体先执行 [云端字体配置](team-font-configuration.md) 的团队/账号上传与用户交接路径。

行为：

- 保留正式实例默认内容；继续合法的 Variant、Boolean、Slot 和外层布局；
- 不 remap 字体、不放本地字体文件、不改正式库主组件、不外挂手绘文字遮盖；
- 不得把 Group 当交付页面或模块根来规避布局失败；
- 记录 `nodeId / 目标值 / 缺失能力或字体 / 恢复动作与等待依赖`；
- 可以保存未完成结构，但不能宣称内容已完成。任何必需项 degraded 都阻断整个交付门禁，不能以 P0～P2 清零掩盖。恢复后写入真实内容并重验布局、截图与交互。

## `illegal-mutation`：事务失败

触发：

- 改了规范源或正式库主组件；授权业务文件内已登记 gap 主组件的合法修复不属此项，须记录本地快照并回归全部实例；
- detach、克隆业务实例；
- 字体 remap、变量解绑、非法后代视觉或布局 override；现场 description 要求的示意填充处理不是非法后代视觉；
- 写入后快照字段意外漂移。

行为：删除**本轮创建**的错误实例，从发布库重建。用户已有节点仅按 preSnapshot 精确恢复本次变化；不能证明可恢复时立即停止相关写入并报告损坏和恢复入口。不得对用户已有实例 `resetOverrides()`，不得把它降级成 degraded。

## 交付格式

```text
状态：degraded
位置 / nodeId：
目标值：
当前保留值：
缺失字体或能力：
恢复动作 / 待用户完成的步骤：
```
