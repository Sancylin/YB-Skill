# 任务能力预检

## 两阶段

intake 只读检查目标、规范源、发布库、工具可用性及独立子代理能力。plan 门禁后选型，再在已授权目标临时区最小验证本次真正用到的操作；探测前要有槽位证据。探测不属于业务成功稿，记录 nodeId 并清理。不能用探测代替看截图和核对组件身份。

## 必要能力

先保证能搜库、能实例化、能截图。脚本硬查：

- 所有任务：`read-library`、`independent-review`、`screenshot`（Figma 与 Demo 都要截图取证）
- Figma：`import-instance`
- Demo：`demo-mapping`、`demo-render`
- 有真实 gap：`compose-check`（所有交付物）验证正式件组合确实无法覆盖；Figma/both 另需 `create-component`

`write-text`、`layout`、`slot-write`、`bind-foundations`、`demo-interaction`、`read-target` 在真正执行该操作前探测。次要 probe 可以 degraded/blocked 并记录恢复入口，不因此否掉已经实例化且截图成立的交付；只有必需能力 blocked/degraded 才整体 paused-blocked。

`independent-review` 的证据要记录隔离机制（如无历史继承的独立子代理）和评审者身份，评审者不得等于 designerId；没有隔离能力就是 paused-blocked，不能用同上下文换角色补位。复用现网屏幕/模式时，plan 阶段先取 `liveBaseline`（现网截图或几何）；Figma 用节点 bbox 对父级 clip 检查 overflow，Demo 用 DOM 断言检查 `overflow:hidden` 祖先与视口；both 还要能导出两端截图做 parity。

具体 probe 覆盖所选字体 family/style、TEXT Property、实际 Slot 类型、实例迁入 auto-layout、变量/样式绑定、截图导出。只需覆盖不同操作类型。原始工具返回要保存；available 字样或本机可显示不算写入验证。

## MCP 工具与降级

| 能力 | 工具 | 降级 |
|---|---|---|
| 发布库身份与目录 | `get_libraries`；完整发布根目录用 `list_file_components_for_code_connect` 按当前接口列出 | 拿不到发布状态或分页不完整：不写 `libraryCatalog.complete=true`，记 `blocked` |
| 语义检索 | `search_design_system` | 遵守当前工具批量与重试限制；缺失意图不记已执行，必要时转允许的只读目录盘点 |
| 节点与 description | `get_design_context` / 节点读取 | 读不到 description、属性或 libraryKey 归属：`blocked-insufficient-evidence`，不判 gap |
| 截图取证 | `get_screenshot`（Figma）与浏览器/DOM 截图（Demo） | 截不到图或缺当次截图：必需能力 blocked，整体 paused-blocked |
| 写入 | 实例化、公开属性、Slot、外层布局 | 写入失败最多重试两次；必需写入受限记 `blocked`，不能用自绘或页面层绕过 |

`get_screenshot` 是 visual/parity 的主证据；`list_file_components_for_code_connect` 是 `libraryCatalog` 的唯一合法来源，`demo/data/figma-components.json` 只是本地封装快照，不能冒充当次发布目录。任何降级都要写恢复入口、受影响 unit 和重试条件，不写“工具不支持”就继续。

## 故障处理

临时调用失败最多重试两次，间隔与错误提示相符。无新证据不重复撞同一字体/权限限制。本机显示正常不能替代 MCP 加载与写入验证。

字体失败的自动恢复入口见 [团队字体配置](team-font-configuration.md)，统一处理团队/账号上传、电脑操作能力缺失时的用户交接和恢复，不要求用户逐条改字。

原字体/规范不可替换；Slot 非法不能外挂伪造。必需能力 blocked/degraded 使整体 paused-blocked，保存缺失能力、受影响 unit、恢复入口。其他合法操作可继续，但不能交付完成。

恢复后重跑对应 probe，再写真实内容，重验换行、尺寸、布局、视觉和关联交互。Figma 与 Demo 能力分别判定，不能一端成功抵消另一端失败。
