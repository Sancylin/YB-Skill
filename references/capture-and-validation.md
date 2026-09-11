# 采集、计算与恢复

新运行 schemaVersion=3。原始工具返回、归一化结果、确定性计算与评审判断分开保存。哈希只证明内容未变化，不证明来源真实。

## 来源

文字输入 intake.originalSourceIds 指向 required captured source；派生 PRD 不替代它。changeSet 记录用户明确变更及旧 requirement 快照，规则见 [输入分流](input-routing.md)。原始来源始终进入独立评审包。

证据由宿主保存原始 MCP/浏览器结果；本地脚本不冒充 MCP 客户端。记录 producer、capturedAt、target 和原始证据引用；toolCallId 仅宿主真实提供时写入。无法观察的字段写 unknown，不用空数组伪装不存在。postSnapshot 必须重新读取真实目标。

## 精确填充

protected.fills 采用 `{descendantNodeId:[paint对象,...]}`。每个 descriptionFillAdjustments 必须含 nodeId、paintIndex、property（visible/opacity）、before、after、action=hide-fill、descriptionQuote。layerName 仅说明用途。引用必须属于 canonical description。只允许原 visible=true 改 false，或正 opacity 改 0；节点、paint 数量、颜色、变量及其它属性不变。每条实际差异恰好对应一条例外。基线对应最终合法公开属性组合。

## 自动比较

content.source/figma/demo 是以稳定 contentId（可嵌套状态）为键的非空对象。可见内容从实际文本/DOM 获取，输入字段读 value；隐藏示意与当前业务内容分开。只归一化换行及 Unicode NFC，数字、标点及有意义空白不忽略。双方字段和值均比较，both 三方比较。

baseline 元素的 live/ours 存数值，deltas 中同字段数值必须与元素一致，delta 自动等于 ours-live。所有数值有限，tolerance 非负。容差依据来自明确规范或评审，不能人为调大过门禁。业务授权偏差引用用户证据；设计取舍由独立评审确认。

命令（output 必须新文件，不能覆盖证据）：

```text
python3 scripts/compare-evidence.py content input.json output.json
python3 scripts/compare-evidence.py baseline input.json output.json
```

content 输入另含 media=[figma]、[demo] 或 [figma,demo]；baseline 输入每个元素有 fields、live、ours、tolerances。生成结果再登记 evidence；deliver 重新计算，不相信空 mismatches 或手填 delta。

## 裁切与截图

区分 intentional-scroll、intentional-crop、overlay、unexpected-overflow。正常滚动子节点超出视口不是缺陷；检查可达性、承载容器和预期裁剪。Figma 读取 clipsContent 和实际可获得边界；DOM 读取 computed overflow、client/scroll 尺寸及滚动状态。阴影、旋转或蒙版无法仅凭 bbox 判断时独立看图，不伪造自动通过。

双端对齐固定 unit、state、theme、device、内容版本。语义结构与文案严格一致，几何依容差，不要求 DOM 与 Figma 节点树相同或字体抗锯齿像素完全一致。

## 评审成本和失效

方案前允许只读可行性探查（目录、关键组件约束、基础规范）；不写业务页、不静默改需求。正式 resolve 仍在 plan 后。

requirements 可由独立 UX 评审者同次调用输出独立维度；UX/UI 仍须不同且无历史继承。首轮发现封存后才开放系统审计材料。无问题 findings 可为空，但 pass 必须有 checksPerformed（unitId、summary、evidenceRefs）；issues 不能空 findings。

依 requirement→unit→slot→implementation→check 追踪影响。修复只重采受影响证据；未变项复用需核对依赖指纹并形成当前覆盖记录，不能批量改版本号。最终仍覆盖全部当前 unit。全局 token/父级变化扩大范围；业务路径变化回 plan。复验可以看原问题，不冒充全新盲审。

## 运行记录格式转换

```text
python3 scripts/migrate-run.py /old/run.json /new/run-dir
```

将 schemaVersion=2 的输入复制到独立目录，原件保存为 run.v2.json，标 paused-blocked 和 needs-recapture。补齐原始输入、精确填充、完整目录分类、重新计算及当前独立评审后，migration.status 才可记 revalidated，并运行所有门禁。输入记录中的 pass 不自动视为有效；不重建仍可用目标节点。

## 规则来源

工具限制以当前声明为准；team-rule 需现场出处与适用条件；workflow-invariant 包括身份保护、真实来源及权限边界；heuristic 为可解释调整的设计建议。整机居中、浮层 Hug、布局选择等只有现场团队依据才是硬规则，未确认时标启发式并独立评审，不自动升级成规范。组件内部规范不因此放宽。
