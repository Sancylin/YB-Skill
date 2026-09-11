# 任务模拟评审

任务模拟评审补充现有 checklist：不只检查“有没有状态”，而是从用户角度逐步执行任务，判断信息、反馈、连续性和恢复成本是否合理。

## 1. Reviewer 输入

盲审材料只包含：

- Requirement Spec / 原 PRD 证据；
- Product Experience Model 中本任务相关事实；
- Experience Decision Record；
- UX Freeze 产物（评 plan 时）；
- 可点击 Demo 或状态截图（评 final 时）。

不包含 Designer 的辩护、评分、自评结论和历史 reviewer 结论。

## 2. 必跑场景

每个主任务至少跑：

1. **Primary happy path**：正常用户从入口完成目标。
2. **First-use / low-context**：用户不了解功能时是否知道下一步。
3. **Error or invalid input**：错误是否在可行动的位置出现，是否保留已完成工作。
4. **Cancel / back / interrupt**：退出、返回、中断后是否丢上下文或产生不确定状态。
5. **Post-success continuation**：完成后用户是否知道结果，下一步是否自然。

按任务再选：

- 高频专家用户；
- 大数据量；
- 弱网/长任务；
- 权限不足；
- 部分成功；
- 多设备/内容增长；
- 高风险不可逆操作。

## 3. 逐步记录

```yaml
simulation:
  scenarioId: "..."
  category: happy-path | first-use | error | interrupt | post-success | other
  userIntent: "..."
  steps:
    - step: 1
      sees: "..."
      decides: "..."
      ambiguity: "..."
      friction: none | low | medium | high
      systemFeedback: "..."
  failurePoint: null | "..."
  recoveryCost: low | medium | high
  contextLoss: none | partial | severe
  verdict: pass | issue
  findings: []
```

Reviewer 每一步都回答：

- 用户现在看到了什么关键信息？
- 下一步是否可预测，还是必须猜？
- 系统是否让用户知道“发生了什么 / 现在是什么状态 / 接下来怎么办”？
- 前一步输入和选择是否被保留？
- 是否出现不必要的往返、记忆负担、重复输入或确认？

## 4. 体验问题分级

沿用 P0～P2，但补充体验判断：

- **P0**：核心任务无法完成、严重误导、危险操作不可控、无恢复出口。
- **P1**：主路径明显多余/绕、重要上下文丢失、关键状态反馈不清、常见异常无法行动。
- **P2**：局部认知/操作成本可复现地偏高，虽能完成但影响效率或理解。

“我更喜欢另一种布局”不是 issue。必须指出具体场景、用户成本和验证方法。

## 5. Pairwise 评审

有两个可行候选时优先做 pairwise：同一 Reviewer 在相同 Requirement Spec 下比较 A/B，只判断任务结果和体验取舍，不看视觉完成度。

输出：

```yaml
preference:
  winner: A | B | tie
  decisiveReasons: []
  losingCosts: []
  conditionsThatCouldFlipDecision: []
```

如果两者在任务结果上等价，允许 `tie`；不要为了产出结论强行制造差异。

## 6. 机器门禁

plan 的 `experience` review 和 final 的 `ux` review 都要把上述五类必跑场景写入结构化报告 `simulationScenarios`。门禁只检查这些场景确实被记录并有结论，不替代 reviewer 的体验判断；场景命中专项风险时仍需按第 2 节补跑对应专项。
