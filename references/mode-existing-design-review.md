# 已有稿评审模式（`review-existing`）

## 触发

审核现有设计或原型，默认只读。

## 允许写入

默认不写设计。明确授权评审并修复时转 iterate，并继承授权范围。

## 禁止

不新建业务页、不读取无关历史评价、不把缺原始 PRD 的推测当业务事实。只读报告不能使用设计交付门禁宣称完整设计完成。

## 流程

锁定目标和范围；先截图/任务走查评 UX/UI，再查节点与实时库。没有 Slot Evidence 时以 `requirementsBasis=review-observed` 重建可观察职责，此过程不写入、不判 gap。无论是否已有 Slot Evidence，都重新调用 `get_libraries`，核对全部区域根资产及递归 slotBindings。

无原 PRD 或附件时单列业务需求 coverage 未知；可报告可观察的视觉、系统问题，但不能宣称全量 P0～P2 清零。只在明确授权抽样时抽查并报告 coverage。使用 [评审清单](review-checklist.md) 与 [独立复评](mode-independent-review.md) 的材料隔离办法。

## 确认点

评审不等于修复；缺授权保持只读。修复需要业务解释时转 `iterate` 重新审定，不把截图推断自动升级成可写需求。用户明确授权修复但没有原 PRD 时走 [模式-迭代](mode-iteration.md) 的无 PRD 授权路径：把授权原文登记为 required source，requirements 以 `origin=derived` 回指授权位置与观察事实，plan 门禁通过后按 `reviewed-plan` 进入 build；`review-observed` 仍只用于只读评审。

## 停止

只读时输出问题、证据、覆盖与限制后停止，记录 `stage=report` 并用 `--gate report` 校验；报告可以 `verdict=issues`，但每条 P0～P2 必须回指问题台账。获授权修复时按完整修复/复验门禁执行。
