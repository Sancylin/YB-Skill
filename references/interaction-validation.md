# 状态转换与体验验证

## 转换契约

每项关键任务记录前置条件、当前状态、用户动作/系统事件、预期下一状态、应保留内容、反馈与恢复/退出。状态矩阵有图不代表转换成立。对每个相关 unit 预先选 interactionLevel：design、executed 或 not-applicable；不能在验证失败后降低等级。`both` 用 `interactionLevels` 按交付物分别记录（通常 `{figma: design, demo: executed}`），每端 interaction 检查的 `level` 必须与对应值一致。

## 走查

按需求选择入口→完成→退出、错误→重试、返回状态、重复操作、加载禁用、内容增长、滚动末尾、键盘与浮层遮挡、设备和主题。记录步骤、预期、实测、截图/工具证据、pass/fail/unknown。关键转换全部覆盖；组合边界按风险覆盖并说明理由，不生成无意义排列矩阵。

静态 Figma **仍要画交互后的页面**：点击、提交、空、错、弱网、浮层、成功等，每一态一张静态屏。所谓 `design` 只表示 Figma 不用做成可点热区/原型连线；不是省略这些屏。可点走查记在 Demo 的 `executed`。`both` 时两套屏结构、层级、元素和文案应对齐，不能把 Figma 的等级改成 `executed` 来省 Demo 走查。外部服务未实现时不得声称生产行为已验证。若任务要求实际操作而当前工具不能执行，保持 required check unknown，不能自动改成 design。

## 视觉与节点

必要截图覆盖首屏、关键滚动位置、末尾操作、浮层、异常及内容边界。正常滚动越界和合法 overlay 不当成碰撞；结合 viewport、clip 和节点角色判断。文本内容与内容脚本核验，不以默认说明、字体规格或占位文案冒充。

裁切不能只靠肉眼看截图：Demo 断言后代 `getBoundingClientRect` 不越出最近的 `overflow:hidden` 祖先或视口，并检查 `scrollWidth/scrollHeight`；Figma 读回节点 bbox 与父级 clip 比较。发现逃逸先修，再写 overflow 证据。

对比、触达、阅读顺序、焦点及读屏等按团队采用的适用规范验证；静态无法证明的行为如需验收则进入对应原型或实现走查。结果写 checks，保持设计层与实测等级。
