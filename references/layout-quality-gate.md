# 布局几何门禁

本门禁专门防止“组件用对了，但简单对齐、padding、gap、Auto Layout 仍然不对”。它适用于 Fast / Standard / Full，不能因任务简单跳过。

## 1. 原则

布局质量使用两类证据同时成立：

- **结构读回**：方向、主/交叉轴对齐、Fill/Hug/Fixed、padding、itemSpacing、绝对定位、最终 bbox；
- **最终截图**：正常阅读尺度下的视觉层级、光学对齐与异常空隙。

结构参数正确不代表最终视觉一定正确；截图恰好对齐也不能替代结构读回。

## 2. 一次批量检查

build 完成后，优先一次 read-back 获取本次新建/修改布局宿主与关键子节点，不逐节点截图。对每个 visible unit 生成一份 `layout-geometry` evidence：

```json
{
  "unitId": "u1",
  "deliverable": "figma",
  "verdict": "pass",
  "checked": [
    {
      "nodeId": "frame-1",
      "role": "content-column",
      "layoutMode": "VERTICAL",
      "primaryAxisAlignItems": "MIN",
      "counterAxisAlignItems": "MIN",
      "padding": {"top": 16, "right": 16, "bottom": 16, "left": 16},
      "itemSpacing": 12
    }
  ],
  "measurements": [
    {
      "kind": "edge-alignment",
      "values": [16, 16, 16],
      "tolerance": 1,
      "status": "within"
    },
    {
      "kind": "spacing-consistency",
      "values": [12, 12, 12],
      "tolerance": 1,
      "status": "within"
    }
  ],
  "violations": []
}
```

Demo 使用浏览器几何读回，字段含义一致；不要求完全相同的工具属性名，但 measurements 必须来自实际节点/DOM 几何。

## 3. 必查项

对本次新建或修改的布局宿主，至少检查：

- 业务屏/模块根不是 Group；结构关系优先 Auto Layout；absolute 仅用于有理由的 overlay；
- 方向、主轴/交叉轴对齐、分布不是未思考的工具默认；
- 父级 padding 与子组件 description 声明距没有重复叠加；
- 重复同类 sibling 的 gap 没有无理由漂移；
- 应同边对齐的元素 bbox 边缘在容差内；需要基线对齐的同行文字单独检查；
- Hug / Fill / Fixed 与剩余空间关系不会让 CENTER / MAX / SPACE_BETWEEN 失效；
- 贴边壳层没有误吃页面 inset；内容内收没有贴边；
- 最终 bbox 与 overflow 检查一致。

## 4. measurement 规则

`measurements[]` 支持：

- `edge-alignment`：同一对齐组的 x/y/右边缘/下边缘值；
- `spacing-consistency`：同类重复 sibling 的实际间距；
- `padding-pair`：场景要求对称时比较成对 padding；
- `baseline-alignment`：同排文本需要基线对齐时比较 baseline；
- `custom`：其它可测几何，必须有 `reason`。

每项：

- `values` 至少 2 个有限数值；
- `tolerance >= 0`；
- `status=within` 时 `max(values)-min(values) <= tolerance`；
- `status=authorized` 时必须写 `reason`，说明为什么不应一致；
- 不能用 `authorized` 遮盖无依据的随机偏差。

没有天然需要一致的对象不要为了过门禁硬造 measurement。至少应存在一个真实可比组；若本屏确无重复/同边/基线关系，可用 `custom` 记录关键容器 padding/gap 与 Screen Spec 的 measured comparison，并说明理由。

## 5. Fast 修复策略

Fast 的 UI Reviewer 先看截图，再结合 `layout-geometry`：

1. 第一次发现局部对齐/间距问题：主执行者局部修复；
2. 修复后重新 read-back + screenshot；
3. 同类问题再次出现，或修复需要改变 Screen Spec / task model：记录升级到 Standard；
4. 不允许靠增加 reviewer 轮次在 Fast 内无限打磨。

布局问题仍按 [评审清单](review-checklist.md) 分 P1/P2；“个人更喜欢另一种间距”不算 P2，必须有现场规范、同类一致性、Screen Spec 或可测几何依据。
