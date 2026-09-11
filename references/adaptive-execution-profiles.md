# 自适应执行分级

本文件只决定**执行强度**，不降低交付质量。核心原则是：**低成本起步、证据驱动升级、质量门禁不分档**。不要把 PRD 一次性永久判成 Fast / Standard / Full；先选当前最低安全档，运行中发现新风险就升级。升级只重做受影响阶段，不从 intake 全量重启。

## 1. 三档职责

| 档位 | 适用 | 主要节省 | 不允许省 |
|---|---|---|---|
| `fast` | 已有任务模型上的局部增量、1–2 个可见 unit、无新 IA/导航/权限/长异步/部分成功/高风险不可逆 | 不做完整候选体验发散；plan 只需 requirements + experience 独立审查；final 只需独立 UI 审查；任务模拟按风险触发 | 现场组件解析、正式实例身份、layout-geometry、overflow、content、node-audit、当次截图与修复复验 |
| `standard` | 新任务或新体验模式，但没有高风险系统性变化 | plan 不做 UI 维度独立审查；final 不做额外 system LLM 审查；其余保持 | Experience Decision、UX 审查、UI 审查、布局/截图/组件门禁 |
| `full` | IA/导航/权限变化、高风险不可逆、长异步、部分成功、跨上下文多步、主任务模型重大变化或高歧义 | 不节省 | 当前完整审计链 |

`fast` 不是“质量低”，而是“推理和评审轮次少”。任何 visible unit 的几何与视觉门禁完全相同。

## 2. 初始路由记录

`generate` / `iterate` 在 Experience Decision 前写 `executionProfile`：

```json
{
  "executionProfile": {
    "level": "fast",
    "source": "auto",
    "assessment": {
      "taskModelChanged": false,
      "navigationChanged": false,
      "informationArchitectureChanged": false,
      "permissionChanged": false,
      "highRiskDestructive": false,
      "longAsync": false,
      "partialSuccess": false,
      "crossContextMultiStep": false,
      "newExperiencePattern": false,
      "visibleUnitCount": 1,
      "componentCoverageExpectation": "known-existing",
      "ambiguity": "low"
    },
    "requiredSimulations": ["happy-path"],
    "reasons": ["existing task model; one local unit; no structural risk"],
    "escalationHistory": []
  }
}
```

`source` 为 `auto | user`；用户可以要求更高档，但不能要求跳过硬门禁。`componentCoverageExpectation` 只能是 `known-existing | likely-existing | unknown`，只基于已知上下文判断；**Experience Decision 前仍禁止读取组件目录来反推体验。**

## 3. 最低档计算

先按以下规则得出 minimum profile；允许主动选更高档，不允许低于 minimum。

### 必须 `full`

任一为 true：

- `navigationChanged`
- `informationArchitectureChanged`
- `permissionChanged`
- `highRiskDestructive`
- `longAsync`
- `partialSuccess`
- `crossContextMultiStep`
- `ambiguity=high`

### 至少 `standard`

未命中 Full 且任一成立：

- `taskModelChanged`
- `newExperiencePattern`
- `visibleUnitCount > 2`
- `componentCoverageExpectation=unknown`
- `ambiguity=medium`

### 可 `fast`

以上均未命中，且：

- `visibleUnitCount` 为 1–2；
- `componentCoverageExpectation` 为 `known-existing` 或 `likely-existing`；
- 主任务模型、导航、IA、权限与关键恢复策略不变。

不要用 PRD 字数、页面看起来简单或“人工半小时能做完”单独判断档位。

## 4. Fast 的 Experience Decision

Fast 不从零重建完整体验模型。优先写 `delta`：

- 原主任务是否保持不变；
- 新增/修改了什么动作或状态；
- 是否改变进入、退出、恢复或完成后的连续性；
- 是否出现新的错误、高风险或权限条件；
- 为什么仍可沿用已有 task model。

独立 Experience Reviewer 重点检查两件事：

1. 当前 profile 是否过低；
2. 增量是否真的不改变 task model / IA / recovery。

review 报告必须给 `profileVerdict=keep | escalate-standard | escalate-full`。不是为了多打一份分数，而是让路由判断本身接受独立挑战。

## 4.1 独立评审调用合并

维度数量不等于 LLM 调用次数。只要仍满足盲审材料隔离：

- 同一个隔离 reviewer 可以在**一次调用**里输出多个独立维度报告；每个维度仍保存为自己的 review record / report evidence；
- Fast 的 plan `requirements + experience` 默认同一次 reviewer 调用完成，final `ui` 再一次，目标是 **2 次 reviewer 调用**；
- Standard 的 plan `requirements + experience + ux` 默认一次完成，final 的 `ux` 与 `ui` 因必须不同 reviewer 而分两次，目标是 **3 次 reviewer 调用**；
- Full 的 plan 可由 reviewer A 输出 requirements/experience/ux、reviewer B 输出 ui；final 可由两个 reviewer 覆盖 ux/ui/system，仍保证同阶段 UX 与 UI 不同人；
- 不为了“维度看起来独立”机械启动 7 个 agent；真正独立的是结论与材料隔离，不是调用次数。

## 5. 风险触发的任务模拟

`happy-path` 永远必跑。其余按需求事实触发，并写进 `requiredSimulations`：

- 有首次引导/首次状态变化 → `first-use`
- 有失败、校验、弱网、权限或不可达结果 → `error`
- 有等待、长输入、可取消、切后台/切页面继续 → `interrupt`
- 完成后有重要下一步、返回上下文或连续任务 → `post-success`
- 批量且可能部分成功 → `partial-success`
- 不可逆/高风险 → `destructive-recovery`

Fast 通常只需 `happy-path` 加实际命中的专项场景；Full 仍跑基础五项并补专项。

## 6. 运行时自动升级

模式不是承诺。以下发现必须升级并记录到 `escalationHistory`：

### `fast → standard`

- 解析后出现真实 `gap`；
- `compose` 需要有视觉职责的正式宿主或复杂多层组合，而不是简单 `layoutOnly`；
- 实际可见 unit 超过 2；
- 发现新体验模式、task model 改变或 `experienceDecision.confidence != high`；
- 当前页面/模式的关键 baseline 无法获得；
- 独立 Experience Reviewer 返回 `escalate-standard`；
- 同一个 layout-geometry P2/P1 修复后再次复现。

### `standard → full`

- 运行中发现 IA/导航/权限、高风险不可逆、长异步、部分成功或跨上下文多步；
- Experience Reviewer 返回 `escalate-full`；
- 修复要求改变主任务模型、主操作或业务结果。

升级后保留仍有效的 Requirement、现场组件证据和未受影响实现；只刷新被新风险影响的 Experience / Plan / Review。

## 7. 所有档位共享的质量底线

任何档位都必须：

- 组件走 `formal-instance → compose → gap`，Fast 只是在确认完整 formal 候选后更早停止搜索；
- build 后一次批量 read-back；
- 每个 visible unit 有 `layout-geometry`、`overflow`、`content`、`node-audit`；
- visual 引用当次截图；
- layout-geometry 检查 Auto Layout、padding/gap、边缘/基线或重复间距的一致性，不以“看起来差不多”替代；
- Fast 允许一次局部修复回路；同类几何问题再次出现就升级，不无限在 Fast 内重试。

详见 [布局几何门禁](layout-quality-gate.md)。

## 8. 组件解析的效率策略

不改变 Figma 作为唯一组件事实源：

1. 先把当前方案所有槽位语义一次列齐，按职责/状态/内容类型分组；
2. 默认批量提交可合并的语义搜索；
3. 完整覆盖候选一旦通过 description gate，立即早停；
4. 同一 library 指纹、同一会话内复用已读 description/属性证据；
5. 只有证明 `gap` 才做完整 Inventory；
6. Fast 如果进入 gap，先升级再继续，不在低档里做昂贵全库证明与新组件创建。

这减少的是 MCP round trip，不建立人工维护的组件缓存；组件 description 仍只在 Figma 维护。

## 9. 性能指标

运行记录可选保存 `metrics`：每阶段 `durationMs / llmCalls / toolCalls / reviewCalls / fixAttempts`。优先看：

- `timeToFirstUsableDraftMs`
- `totalDurationMs`
- `figmaSearchCalls`
- `figmaReadCalls`
- `reviewCalls`
- `fixAttempts`
- `profileEscalations`

优化目标优先是缩短“第一版可用稿”，不是让 Agent 在无人参与时把最后 5% 无限打磨。
