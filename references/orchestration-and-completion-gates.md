# 自动编排与完成门禁

## 执行状态

在 `artifacts/<run-id>/` 保存 [运行契约](run-record-format.md)。使用 `python3 scripts/validate-run.py --init <run-dir>` 创建未完成记录；不要复用历史报告。

阶段仍使用：`intake → experience-plan → experience-review → plan → plan-review → resolve → capability → build → blind-review → system-audit → fix → verify → deliver`，但 `executionProfile` 决定哪些独立评审阶段需要真实执行；不要求为了填阶段名而做无价值调用。Fast/Standard/Full 规则见 [自适应执行分级](adaptive-execution-profiles.md)。Experience 阶段先完成任务模型或 delta 与任务模拟，不解析组件；发现新风险就升级 profile，并只重做受影响阶段。只读评审走 intake → blind-review → system-audit → report（`--gate report`），不执行 build/fix/deliver 门禁。

每个阶段转换前保存 run.json、证据、未解决问题、下一步。命令从 Skill 根执行：

```text
python3 scripts/validate-run.py artifacts/<run-id>/run.json --gate plan
python3 scripts/validate-run.py artifacts/<run-id>/run.json --gate build
python3 scripts/validate-run.py artifacts/<run-id>/run.json --gate deliver
python3 scripts/validate-run.py artifacts/<run-id>/run.json --gate report
```

## 授权与审定

- `authorization` 记录原始授权证据、可写目标和 fix 权限；用户授权决定范围，方案评审决定能否实现，二者不能互相代替。
- generate 默认范围内实现和修复；review-existing 单独触发时默认只读。独立评审者默认不直接写稿，由主执行者统一串行修复。
- `reviewed-plan` 表示通过内部方案门禁；`user-confirmed` 适用于用户明确要求审定的方案；旧稿只读推导用 `review-observed`。废弃旧字段 confirmed-freeze，不能将历史确认自动迁移成当前评审通过。
- 完整需求无需例行等待确认。可逆的设计选择、必要状态补齐和范围内修复自主执行；记录设计假设。
- 业务规则冲突、会改变业务结果的缺失选择、扩大授权范围时需要用户输入。时间经过不是答案；不受影响工作可继续。
- 结构性修复若改变主任务模型、上下文保持、风险/恢复策略，回 experience-plan；只影响已冻结结构则回 plan-review。仍在原授权和业务规则内则内部重新审定，不一律要求人工确认。

## 门禁

门禁服务视觉结果和组件调用，不把记录填满当完成。intake 没有单独的命令，由 plan 门禁一并校验。脚本核对登记证据的覆盖与可计算一致性；原始来源仍需采集链及独立审计验证；稿好不好看以截图和独立评审为准。首次生成就必须走完阶梯，不能等用户指出才改用组件库。

| 门禁 | 必须成立 | 不得用来否掉正确稿 |
|---|---|---|
| intake（plan 门禁一并校验） | 已判定 `inputMode` 和 `deliverableDecision`：先问 Figma/Demo/both，未回复或无法询问时默认 `web-demo` 并登记原因；文字输入已产出不预设页面解法的 Requirement Spec/PRD 并登记 `source` 证据；上传 PRD 默认 `verbatim` 且未改写，用户明确要求改写时记 `rewrite-authorized` 并附授权证据 | 文字需求补充说明较多、上传文档格式特殊、用户暂时没回交付物问题 |
| reference | UX/UI Freeze 后、组件解析前，`referenceReview.status=reviewed`；原输入文件页面已扫描，组件库 Template 子流程和用户参考均有当次 `kind=reference` 证据、结论与理由；命中页面给出 `direct-reuse / adapt-reuse / reference-only`，直接或改造复用现有业务页面时对应 unit 有匹配 `liveBaseline`；来源只读且输出仍写回原输入文件 | 来源身份已存在于 Skill 或原请求，不要求再次提供；来源较旧本身不是重做理由 |
| plan | 原文已读；`executionProfile` 不低于风险最低档；`experienceDecision.status=reviewed` 且有任务级 chosen model/rationale/evidence；独立评审维度按 profile 成立（Fast requirements+experience；Standard 再加 ux；Full 再加 ui）；需求→unit；每个可见 unit 已给出 liveBaseline 决策；方案可执行；当前方案 P0～P2 清零；无关键业务未决 | packet 多了备注、评审报告多了字段 |
| build | 写入授权（`write=true` 且 `scope` 为非空字符串数组）；顶层 `liveLibrary` 记录当次发布库身份与观察到的 `ids`，且 `libraryCatalog.complete=true` 时 `ids` 必须是目录子集；必需槽位按 `formal-instance → compose → gap` 阶梯解析并记 `reuseLadder`；选中正式件有 pass 证据且属于 `liveLibrary.ids`；gap 另有 `composeTrials` 组合失败证明和 `libraryCatalog` 锚定的完整盘点 | 次要能力 probe degraded/未登记、白名单路径不完整 |
| deliver | 选中组件已在目标页实例化；visual 引用当次截图，`layout-geometry`、content、overflow、node-audit 均通过，interaction 按交付物核对等级，现网复用按 `(unitId, deliverable)` 各有 baseline 对照，both 有 parity；独立 final 评审维度按 profile 成立（Fast ui；Standard ux+ui；Full ux+ui+system），P0～P2 finding 回指问题台账；身份未破坏（未换字体、未解绑、未 detach）；P0～P2 已关 | 快照多了原始工具字段、缺 writeWhitelist 路径、expectedFacts 为空 |

没执行评审不等于零问题。建议项只适用于有理由证明不违反要求的偏好；不得把成立的 P2 降级、隐藏、忽略、标豁免来通过。只有用户明确变更范围，才能调整 requirements/units，并刷新计划与验收；保留变更证据和历史问题。

## 版本与恢复

分别记录 requirements / plan / design / library revision。libraryKey 是身份而非内容版本；版本不可获取时保存相关 description、属性、结构、变量/样式指纹和读取时间，不声称原子快照。

改需求使方案、选型及评审失效；改方案重做 plan 门禁和受影响选型；改节点重跑受影响截图/节点/交互检查。最终评审与 checks 必须明确对当前 revision 成立；可复用未变化的原始证据，但必须重新核对差异后生成当前检查记录，不能批量改版本号。

Figma 修复记录（`implementations[]`）若报告 `requiresPlanReview=true`、`structureChange=true`、`businessResultChanged=true`，或 `changeImpact` 命中 `information-architecture-change` / `main-action-change` / `business-result-change`，不得直接进入最终交付；最终门禁必须拒绝并返回 `nextAction=resume-plan`，回到方案评审后再继续。触发条件写在这条修复的 implementation 上，不要只写在评审正文里。布尔标志必须是真布尔，`changeImpact` 只能取上述三个登记值；非布尔或未知字符串会被拒绝，不能借此绕过触发器。

恢复先读运行记录，再核对目标节点存在、实际结构和库指纹。用保存的 nodeId 继续，不因重试重新建页。无 nodeId 的不确定写入先搜索本轮已创建目标并核实，防止重复。评审期间暂停待审范围写入；发生变化则重新取证。

## 阻断与收敛

任务状态仅 `running / paused-blocked / complete`。`paused-blocked` 是合法保存态，但所有交付门禁都会拒绝；恢复后回到产生问题的阶段再继续。只读评审交付的是报告而非设计，记录 `stage=report` 并用 `--gate report` 校验，不冒充设计 complete；报告允许 `verdict=issues`，但必须带回指台账的 findings，不能只写结论。

- 必需槽位或能力受限：记录缺口、恢复操作、责任依赖，进入 paused-blocked；其他独立工作可完成，但整体不完成。
- 同一问题连续三次修复无证据进展：停止相同操作，重新定位原因；仍无可行新路径时 `paused-blocked`。此时**交出当前稿、截图、未关闭的 P0～P2 和恢复入口**，停止空转，不再消耗轮次。不得设置“达到轮数自动通过”，也不得把未修好的问题降级成建议项来 complete。用户缩小范围、改需求或明确接受剩余项后，再从保存点继续。
- 关闭修复问题必须由不同于修复者的复验者给出证据；主执行者处理冲突时回查原文与适用规范，不按票数或主观喜好决定。
- 正常会话内自动推进；跨进程自动唤醒依赖宿主调度，本 Skill 只定义持久化与恢复，不声称后台调度已实现。

评审发现 P0～P2、记录格式校验失败、单个代理缺工具，都是优先恢复的执行事件，不自动构成整体暂停理由。缺独立评审上下文、缺现网基线、缺当次截图或内容三方证据属于必需能力/证据缺口，按 paused-blocked 处理，不能用自审或旧证据补位。先修复问题、规范化记录，或把有界操作交给确有能力的执行者；存在可行恢复路径时保持 running。主执行者负责跨角色整合与最终交付，不能用“已交给代理”或一份未完成报告代替端到端结果。多份报告的重叠发现可以有证据地合并追踪，但原始发现仍须保留。

## 历史材料意外暴露

用户要求不参考历史时，搜索和读取默认采用白名单路径，并显式排除旧 artifacts、旧业务稿、同题 Demo 和历史评审。意外返回旧材料时不得继续展开读取，但也不得机械终止整个任务：

1. 记录暴露材料、可见范围、发生阶段及是否已进入当前判断；
2. 未被采用且影响范围可定位时，隔离该材料，复核受影响决策并继续；
3. 已被采用时，只使相关方案、选型、实现或评审证据失效，由未接触材料的执行者重做该范围；
4. 独立评审者看到设计辩护、历史发现或结论时，仅该评审失效，换隔离评审者；设计稿和其它独立证据不自动失效；
5. 只有无法界定影响范围、确认大量复制旧方案，或无法满足用户明确要求的绝对隔离时，才进入 paused-blocked。

暴露记录不能作为当前方案依据，也不能放进盲审材料。恢复后沿用仍然有效的原始 PRD、工具证据和未受影响产物，不从 intake 全量重启。

## 交付报告

给目标链接、完成范围/版本、评审覆盖、P0～P2 关闭记录、门禁报告与建议项。未完成时列出阻断及恢复入口。区分静态契约测试、隔离行为评测和真实 Figma 端到端验证，不能互相替代。
