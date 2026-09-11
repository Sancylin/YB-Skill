# 通用工作流回归

这些用例验证流程不变量，不定义组件规范。组件结果必须在执行时从 Figma MCP 获取。

## 1. 交付物分流

- 输入：用户给出新 PRD，但未说明要设计稿、交互原型还是两者。
- 期望：进入 generate 后先问要 Figma 设计稿、网页交互 Demo 还是两者；未回复或无法询问时默认 `web-demo` 并登记 `deliverableDecision`；方案/能力门禁前不生成业务稿。

## 2. 冻结前禁止实现

- 输入：用户要求根据完整 PRD 直接生成页面。
- 期望：先输出目标、任务流、状态、抽象槽位、Screen Spec 和验收；内部 plan 门禁通过后才正式选型，不例行等人工确认。

## 3. 现场组件解析

- 输入：冻结包中有一个职责槽位；第一次语义搜索返回噪声，改写后仍为空。
- 期望：逐候选记录 pass / proven mismatch / insufficient evidence，再进入 Inventory Fallback。简单槽位完整通过即可选定；复杂槽位先比较已发现高相关候选。只有要证明 gap 时才必须完成全量 Inventory。

## 4. 复合槽位递归

- 输入：候选正式组件要求内容、操作和图标子槽位。
- 期望：按父组件 description 将未解析职责递归成槽位；每个子槽位独立获取现场证据。

## 5. 真实缺口

- 输入：多次现场搜索和递归组合仍无法覆盖一个独特业务内容。
- 期望：只有 `complete=true`、零 `blocked-insufficient-evidence`、当前缺口槽位的未选候选均为 `reject-proven-mismatch` 且无法组合，才标记 gap；盘点能力不足时为 blocked。

## 6. 容器角色

- 输入：页面包含最终边界、透明布局包装、带视觉层级的内容和浮层。
- 期望：按角色决定尺寸、fill、clip 和 overlay；Screen Spec 含 `canvasRole`。正式实例内部视觉不重复绑定。自建层颜色、圆角、间距等到规范源基础页用 `search_design_system` 读取，不写进全局规则。同色叠底按页面与表面职责判断：主对话内卡片优先 secondary，通过自建表面绑定或正式件合法属性实现；已有边界需验证实际可见，不默认叠加装饰。

## 7. 字体能力受限

- 输入：目标文本的实际 family/style 不在插件字体列表。
- 期望：停止文字写入，保留正式实例，记录 degraded 和人工接管；禁止字体替换。

## 8. 选型阻断（`blocked`）

- 输入：候选 description 不足、父级不明或资产状态不可证明。
- 期望：blocked，不实例化、不按名称或本地缓存猜测。

## 9. 写入事务回滚

- 输入：写入后变量、样式、布局或父级关系超出白名单。
- 期望：标记 illegal-mutation，删除本轮错误实例并从当次 live key 重建。

## 10. 迭代模式结构变化

- 输入：已有稿修改会改变任务流、信息架构或主操作。
- 期望：回到 PRD/UX/UI 内部审定；范围内设计修改不重复问用户，业务规则变化才询问。

## 11. 评审与修复授权

- 输入：用户只说评审已有稿。
- 期望：先截图后读节点；没有历史冻结包时以 review-observed 只读重建槽位，不实例化、不判 gap。只输出证据化问题；结构性修复转 iterate 重冻结。

## 12. 独立盲审

- 输入：新会话收到客观交接包。
- 期望：单独请求默认 fixAuthorized=false；端到端生成继承修复授权。使用无历史继承的隔离上下文先评截图 UX/UI，再重新验证发布库并刷新范围内全部根资产/slotBindings 核对 Slot Evidence。抽样必须声明 coverage 且不能宣称全量清零。

## 13. 网页交互原型

- 输入：交付含交互原型。
- 期望：复用同一冻结包、槽位证据和内容脚本；验证工程 manifest 与 live library 一致，为 chosenAssets 中每个资产建立唯一映射并校验 slotBindings/props。缺映射时 blocked，不自绘、不改成 Figma gap。

## 14. 未知设备

- 输入：PRD 指定新设备类别，但目标尺寸和模板未知。
- 期望：扫描目标文件与规范源正式模板；iPad 搜索 `ipad 模板` 和 `iPad适配规则`；页面外层间距搜索 Spacing 变量并打开 `间距规范` 画板。必要时询问用户；不使用历史画布常量，不把断点或间距数字抄进 Skill。

## 15. 自建缺口读基础页

- 输入：冻结包证明一个真实缺口，自建层需要页面边距，且目标是 iPad 宽屏。
- 期望：不先读完整套基础规范去改正式实例。间距打开 `✅ 间距 Spacing`，绑定 Spacing 变量并阅读 `间距规范` 画板例外。画布用 `ipad 模板` 对应展示方式，断点和主区读 `iPad适配规则` 规范说明组件。数值不写进 Skill。规范说明组件和说明画板不得 `createInstance` 到业务稿。

## 16. 同色叠底

- 输入：分组表单页的 surface 填色与白色主底相同；另一页是对话流，必须保持主底。
- 期望：表单页 `canvasRole=grouped`，只把 viewport 换成现场页面次级背景，不改组件默认填色。对话页 `canvasRole=primary`，主底不变，卡片优先用 secondary 的合法实现；需保留主背景且规范支持时才考虑 divider soft 描边。已有投影或描边有效时不加第二层对比，受裁切时修正原因。

## 17. 规范说明件不实例化

- 输入：搜索适配或间距时命中规范说明组件或说明画板。
- 期望：Description Gate 记 `reject-proven-mismatch`，禁止 `createInstance`。画布仍用正式模板组件；规则只读 description 和说明正文。

## 18. 宿主错置

- 输入：冻结包把某状态标成 `in-stream`，候选 description 的【禁用方式】排除内容流，但【用途】仍匹配「空或失败」。
- 期望：Description Gate 因宿主不匹配记 `reject-proven-mismatch`，不把页面级空态放进生成式回答流。

## 19. 嵌套二次底色

- 输入：浮层或卡片 Slot 需要短文案填充，父级已经是 surface。
- 期望：填充物是 `content` 或 `layout-only`，不加第二层填色 Frame；4.1 同色叠底不用于给槽内内容再包底。

## 20. 浮层虚高

- 输入：底部或居中浮层只有几行说明加一颗按钮；另一场景手册要求重复浏览且不要顶满。
- 期望：短内容 hug；只有现场 description 和当前场景同时要求分档或最大高度时才用该高度。不从其它项目抄高度。

## 21. Group 不能当页面

- 输入：插件因字体无法把实例 `appendChild` 进 Frame，实现者打成 Group 当业务屏根。
- 期望：记 layout `degraded` 和人工接管；交付结构仍必须是 auto-layout Frame。编组只允许瞬间搬家后拆组，不能当页面或模块根。

## 22. 声明距不再外加

- 输入：内容流正式件 description 声明了内部间距示意层，外层内容柱又加了同方向 gap。
- 期望：只使用声明距；示意层按 description 处理填充且不删除；外层同方向不再加距。

## 23. 无声明距必须补

- 输入：自建缺口或未声明对外间距的正式件与内容流块拼在同一内容柱，实现者只用绝对坐标贴在一起。
- 期望：外层 auto-layout 打开间距规范和 Spacing 变量补 padding 或 itemSpacing；禁止贴死，禁止猜数字写进 Skill。

## 24. 对话生成中弱网

- 输入：冻结包包含对话正在输出时的弱网。
- 期望：命中 `in-stream-weak-network`：保持正在输出或思考中，过几秒非阻断轻提示；不得画成落地页空态或输出完成后再换整页缺省。

## 25. 未命中的模式不套用

- 输入：纯设置页，没有生成式回答，也没有整页空状态。
- 期望：不套用 `in-stream-weak-network`；落地页弱网才用 `page-weak-network`；无主内容可展示时才用 `page-empty`。

## 26. 网页 Demo 壳

- 输入：交付网页交互原型，含设备画布、内容柱、场景切换和主题切换。
- 期望：页面组合是 auto-layout；设备画布居中并缩放到一屏可见；预览控件在机模外空位；页面边距落在内容层而不是贴边壳层；正式件不撑破容器；Figma 无系统滚动条的区域不显示系统滚动条，需要滚动的区域仍可滚动。

## 27. 完整授权自动推进

- 输入：完整 PRD，明确要求生成并评审修复。
- 期望：内部审定后自动进入选型、能力检查、实现、独立复评和修复；不停止在交接包。

## 28. 关键业务冲突

- 输入：PRD 对同一操作同时要求匿名和强制实名。
- 期望：记录业务未决并阻断相关方案门禁；不以假设自动选一条。

## 29. 原始附件漏读

- 输入：一项范围内需求只在必要附件。
- 期望：缺附件或依赖来源 unread 时 plan 失败。

## 30. 父组件不存在仍复用

- 输入：库无整块业务模块，但按钮和容器存在。
- 期望：主动拆职责并验证组合；只为剩余能力证明最小 gap。

## 31. 完整空库

- 输入：可靠目录确认允许库为空，零候选。
- 期望：允许用空目录和组合证据证明 gap；不得伪造候选。

## 32. 必要能力确实缺失

- 输入：用途匹配，但完整属性证明缺必要状态且不能组合。
- 期望：reject-proven-mismatch；与证据不足区分，继续其他候选或缺口证明。

## 33. 盲审材料污染

- 输入：包里含首轮 P1=0 或完整历史 run.json。
- 期望：不计作独立盲审，生成白名单包并换隔离上下文。

## 34. 修复尚未复验

- 输入：P2 已改节点，但无独立复验。
- 期望：fix-applied 仍阻断；不同于修复者的验证证据才能关闭。

## 35. 正式实例字段绕过

- 输入：将换字体写入允许白名单，或省略保护字段。
- 期望：换字体、解绑变量即使写进白名单也失败。示意填充按 description 处理、名称和外层布局变化不是这条的反例。

## 36. 真实缺口主组件修复

- 输入：已登记业务本地组件长文案溢出。
- 期望：允许范围内修复本地主组件并回归全部实例，不误判为改正式库。

## 37. 历史误报保留

- 输入：旧评审问题经独立确认 not-a-bug，新复评通过。
- 期望：supersedes 显式取代旧报告，原报告和问题留存，同设计版本可通过。

## 38. 字体恢复后的回归

- 输入：字体不可用导致文字未写入，之后恢复。
- 期望：先验证能力，再写真实文案，再验换行、布局、截图和相关交互；恢复前整体不完成。

## 39. 交互图正确但行为错误

- 输入：各状态图正确，返回后丢失上下文。
- 期望：状态转换/走查失败；不能用截图通过抵消。

## 40. 同一缺口多处使用

- 输入：三页需要同一新组件。
- 期望：登记一个合适本地主组件，三处真实实例；反查未登记自绘和正式子件。

## 41. 库内容中途变化

- 输入：libraryKey 不变但发布属性变化。
- 期望：按内容版本/指纹使相关证据失效，重新解析与审计。

## 42. 中断恢复

- 输入：建页成功后会话中断，恢复时未确认前一调用状态。
- 期望：读取 run 和现场 nodeId，核实已有结果后继续，不重复建页。

## 43. 双交付不互相抵消

- 输入：Demo 完整，但 Figma 文案仍为默认说明。
- 期望：Figma content 检查失败，both 不能完成。

## 44. 静态测试不冒充线上

- 输入：fixture 测试全通过，但尚无实际 MCP 运行。
- 期望：报告仅证明离线契约行为；生产门禁不接受 fixture，不能声称真实稿验收完成。

## 45. 团队上传字体

- 输入：远程 MCP 缺苹方，管理员已上传团队字体。
- 期望：重新核实目标团队文件、MCP 账号字体枚举与加载，真实文案写入保持 token 后才通过；不调用本机开发插件。

## 46. 富文本与内容变量

- 输入：同一节点包含不同文字样式或绑定字符串内容变量。
- 期望：加载全部原字体，制定字符段或公开内容属性写入方案，逐段保留样式和变量，不盲目整段替换。

## 47. 上传成功但 MCP 未加载

- 输入：团队字体面板有对应字体，但 MCP 加载失败。
- 期望：记录实际缺失的 family/style、账号及文件作用域，阻断相关写入；不得换字体或宣布成功。

## 48. 团队无字体但可上传到账号

- 输入：团队没有苹方，当前用户不是团队管理员；本次需要 Regular/Medium，有已授权原件和电脑操作工具。
- 期望：核对 MCP 与界面为同一账号，在 Settings → Account → Your uploaded fonts 上传仅本次缺失字重；重新加载与测试写入，保持 token。不等待团队管理员，不安装改字插件，不声称全团队配置完成。

## 49. 无电脑操作能力

- 输入：当前账号缺字，AI 只有 MCP，不能操作上传界面。
- 期望：给出精确字体清单、已找到的文件或缺失原件、账号上传菜单步骤与回复方式；保存阶段和节点，暂停受影响写入，继续独立工作。用户上传后从保存阶段恢复，加载并写入验证通过才继续，不要求用户手改设计稿。

## 50. 上传账号与 MCP 不一致

- 输入：用户说已上传，但上传用 A 账号，MCP 连接 B 账号。
- 期望：指出作用域不一致并按正确账号恢复，不能拿上传成功截图宣称 write-text 通过；不重建已有页面、不解绑 token。

## 51. 团队列表为空但字体已可用

- 输入：团队未配置，但当前账号已经上传或 MCP 已内置所需字体。
- 期望：实际加载与原字体写入验证通过后直接继续，不重复上传，不阻断在管理员配置步骤。

## 52. 已上传但仍不能加载

- 输入：用户回复已上传，字体出现在账号列表，但实际所需字重缺失或组织策略禁止该入口。
- 期望：回查精确 family/style、账号/文件和实际限制；保留阻断与恢复入口，不以回复代替能力证据，不绕过组织策略。

## 53. 默认白底污染布局

- 输入：新建 Markdown 输出柱和卡片内文字列，创建工具默认 fills 为白色；白色页面截图暂时看不出问题。
- 期望：仅对这两个自建 layout-only 显式清空 fills / strokes / effects 并读回；不清除卡片、页面或正式按钮背景。不能仅凭截图判通过。

## 54. 主对话嵌入卡片

- 输入：主背景对话页中卡片无可见边界，自建卡片或正式卡片公开属性支持 secondary。
- 期望：页面主底与 Markdown 包装保持各自角色，只有卡片使用现场 secondary 绑定 / 合法属性；卡内文字层透明，检查真实背景和截图，不默认叠描边投影。

## 55. 分组表单与二级页面

- 输入：反馈页以主背景 Form 分组；另一二级详情页是连续正文。
- 期望：前者可选 grouped / secondary 页面底并保留 Form；后者根据正文职责判定，不能因导航深度强制 secondary。

## 56. 投影存在但被裁掉

- 输入：同色 Navbar 按钮自带投影，其中一个被自建布局祖先裁切。
- 期望：正常按钮沿用原投影；异常按钮修正有权限的错误裁切并截图复验，不因 effects 非空跳过，也不额外加描边。

## 57. 正式卡片没有合法换底能力

- 输入：主对话卡片边界消失，正式件没有公开背景属性且禁止后代覆盖。
- 期望：重新检索合法候选 / 组合；无解记录阻断，不改实例后代、不解绑 token、不伪造 gap，也不换整页底色后宣称完成。

## 58. 透明祖先与独立子表面

- 输入：卡片直接父级无 fills，祖先是同色页面；卡内有文字包装和规范支持的独立代码块。切主题后两个不同名称 token 解析成同色。
- 期望：穿过透明祖先检查实际背景，文字包装透明而代码块可保留有依据的表面；结合主题与边界截图判断，不能按父级空 fills 或不同 token 名直接判通过。

## 59. 九宫格双方向映射

- 输入：分别用横排、竖排实现九种对齐，父内容框有剩余空间，子项固定尺寸。
- 期望：18 个组合的实际几何均匹配水平/垂直目标；不能把竖排的 primary 当水平轴。保留合法左上，不为展示多样性修改目标。

## 60. 参数居中但尺寸冲突

- 输入：要求某组在有界区域正中，其直接父级却 Hug，或子级 Fill 占满目标轴。
- 期望：找出有界空间的真实宿主并修正合法尺寸关系；不只写 CENTER，也不凭空增高容器制造空白。正确 Hug 紧凑组保持原意。

## 61. 两端分布不是等宽

- 输入：一组需要首尾锚定，另一组需要固定 gap；内容从三个子项变成单个，第三组需要等宽子项。
- 期望：分别决定 SPACE_BETWEEN、紧凑间距和子项尺寸，单项状态有预期锚点；不混同分布与等宽，不用空白占位填空间。

## 62. 文字基线与多行内容

- 输入：横排不同字号文字需要共基线，外部区域居中；正文从单行增长至多行。
- 期望：容器居中、文字框内阅读对齐和 BASELINE 分别处理；竖排不设置 BASELINE；长文增长不被改成无依据的居中排版。

## 63. 换行与混合锚点

- 输入：可换行子组与两侧不同锚点区域共同装配，宽度缩小且最后一行不足。
- 期望：行内、多行分布、最后一行和子组锚点各有判断；透明嵌套表达不同关系，不统一左上或以绝对坐标修补。

## 64. 未出现过的组件也适用

- 输入：未在案例中命名的业务区包含多层包装、独立区域及并列条目；都默认白底。
- 期望：不查询组件名特例即可按职责清除纯布局视觉，找到真实承载面并判断独立表面/兄弟区分，合法应用现场背景、边界或效果；对齐逐层判断。

## 65. 同色但不需要新增表面

- 输入：连续内容由清楚留白与标题分组，另有确需独立边界的交互区；两者与承载面同色。
- 期望：前者保持透明与既有分组；后者选择足够且合规的层级线索。不能把所有同色区域涂 secondary，也不能逐层交替背景。

## 66. 变体切换后布局失效

- 输入：正式实例切换为长内容变体，外部宿主仍保持旧尺寸；旧参数截图曾通过。
- 期望：重新验证受影响宿主、祖先及兄弟的双轴几何和表面关系，通过合法外层布局修复；不改正式实例内部，不引用旧版本检查结论。

## 67. 意外看到旧同题材料

- 输入：用户要求不参考历史稿；普通设计执行者的受限搜索意外返回几行旧同题 Demo，但尚未采用，当前方案可追溯到 PRD。另一种情况是独立盲审者看到了历史问题数量。
- 期望：前者记录暴露范围、隔离旧材料、复核可能受影响的决策后继续，不废弃整个 run；后者只使该份盲审无效并更换评审者，不删除设计稿或重做未受影响阶段。只有无法界定采用范围或确认大量复制旧方案时才暂停。

## 68. 可恢复的执行失败

- 输入：方案评审返回若干重叠问题，方案 JSON 缺少追溯字段，主线程不能调用 Figma 但受委派执行者可以。
- 期望：主执行者保留全部原始发现，合并追踪重复项、修复方案和数据契约，通过具备能力的执行者继续；不把局部工具缺失推断为整体无能力，不把评审尚未通过或格式尚未修正当作结束端到端任务的理由。场景为待行为评测用例，不能仅凭静态校验声称行为已经验证。

## 69. 示意填充必须按 description 处理

- 输入：内容流正式件 description 要求实例化后处理内部间距示意层填充，库默认仍带示意色。
- 期望：交付可见态无示意填充；几何保留、层不删除。fills 变化记入 `descriptionFillAdjustments`，摘录能在规范基线 description 中找到。不得为过门禁而保留示意色。不要求 `/protected/fills` 白名单。换字体或解绑变量仍失败。

## 70. 门禁服务视觉和组件

- 输入：正式件已按 description 去掉示意填充，截图视觉成立；实现日志缺某条白名单路径，或快照多了一个原始工具字段。
- 期望：交付不因记录格式失败。换字体、解绑变量、未搜索就手绘、截图缺失仍失败。

## 71. 落地页缺省整机居中

- 输入：落地页弱网或列表空状态，机模有顶栏。
- 期望：命中 `page-weak-network` 或 `page-empty`；缺省插画+说明相对整机画板垂直居中。不得在顶栏下方剩余列里垂直居中导致内容偏下。

## 72. 终评先落原文

- 输入：独立 UX/UI 终评尚未返回，执行者准备跑交付门禁。
- 期望：不得预写 pass 或用脚本覆盖评审报告；先保存评审者 JSON。若是否决，登记问题、修复、升设计版本后再复验。

## 73. 圆角组旁说明内收

- 输入：修改昵称页有圆角单行输入，下方有左对齐辅助说明；另有对话 Markdown 正文。
- 期望：命中 `rounded-group-caption-inset`：辅助说明左对齐但对齐输入框内边内容，不贴圆角外框。Markdown 正文不套这条。

## 74. 修复空转要停

- 输入：同一 P2 已修三次，截图仍是同样缺陷，没有新路径。
- 期望：停止重复操作，`paused-blocked`，交出当前稿、截图和未关问题；不得自动标通过，也不得无限制继续烧轮次。

## 75. 贴边壳层不被内容边距内收

- 输入：对话锁定态同时有流式文本框和底部取消/麦/发送条；长按绿条已经铺满画布。
- 期望：命中 `edge-chrome-vs-content-inset`。文本框按页面边距内收；锁定操作条（及同组键盘）铺满画布，与绿条同宽。禁止把左右 padding 加在二者共用的父级上。Figma 与 Demo 同一拆分。

## 76. 系统键盘用正式件

- 输入：对话打字态或锁定编辑需要画出已拉起的系统输入法。
- 期望：命中 `system-ime-keyboard`。从规范源输入框页取已发布根组件名搜索，description 确认是系统输入法整块示意后实例化，贴底铺满。淘汰键盘图标、输入框内切键盘图标和外部系统库。未发布则 `blocked`，禁止手绘键盘当 gap。

## 77. 复用现网却跳过基线

- 输入：新需求改的是现网已有的输入条和缩略图模式，plan 直接凭印象写 Screen Spec。
- 期望：plan 门禁要求每个可见 unit 给出 `liveBaseline`。`replicated` 必须指向现网节点/截图并记录关键几何、文案和状态；没有现网对应才可 `new` 并写理由。跳过基线不能进 build。

## 78. compose 尺寸超差

- 输入：复用现网 chip，但自建 compose 把高度从 36 写成 40，行高从 20 写成 25。
- 期望：baseline 对照逐元素给 `live/ours/delta/tolerance`；超差且没有 `authorized` 理由时 deliver 失败。自建布局必须有 `baselineElementId` 指向对照元素。

## 79. 授权偏差要有理由

- 输入：确有必要偏离现网几何。
- 期望：delta 标 `authorized` 时必须写明理由；只改状态不写理由仍阻断。用户原文或业务规则才是授权来源，不能自授。

## 80. 中间容器误裁后代

- 输入：Demo 里元宝头像被流式容器裁掉一角；Figma 投影被中间层裁掉。
- 期望：overflow 检查记录检查过的滚动/浮层/文本承载面，`escapes` 为空；后代 bbox 不得越出最近 `overflow:hidden` 祖先或视口。只靠截图肉眼看不算检查。

## 81. 写入日志冒充视觉证据

- 输入：visual 检查只引用一份 Figma 写入日志。
- 期望：visual 必须引用当次截图；写入日志、导出链接和人工摘要都不通过。缺当次截图则不能交付。

## 82. 内容三方不一致

- 输入：内容脚本写「说点什么...」，Figma 用了「发消息或按住说话」，Demo 仍是组件库默认占位。
- 期望：content 证据逐项对照 `source/figma/demo`，`mismatches` 为空；both 时三者必须在同一证据里。占位文案不算对齐。

## 83. 双交付两端不一致

- 输入：Figma 顶栏有三个操作图标，Demo 硬编码隐藏右槽并弹出键盘。
- 期望：`deliverable=both` 每个 unit 有 parity 检查，引用两端当次截图和元素/文案对照，`mismatches` 为空。一端成功不能抵消另一端。

## 84. 同上下文冒充独立评审

- 输入：主执行者自己写了一份 `independent=true` 的评审报告，没有独立子代理。
- 期望：`independent-review` 是必需能力，证据要记录隔离机制和评审者身份，评审者不得等于 designerId；`findings` 是含 unitId、position、summary、evidenceRefs 的结构化数组。缺隔离能力时 paused-blocked。

## 85. 首次生成跳过复用阶梯

- 输入：一个槽位第一次语义搜索没命中，执行者直接记 `gap` 并手绘本地组件。
- 期望：build 拒绝；`reuseLadder` 必须先记 `formal-instance` 和 `compose` 两级 `exhausted`，且至少有两次 `semantic` 和一次 `published-name`/`inventory` 兜底。首次生成就执行，不靠用户提醒才复用组件库。

## 86. 纯布局宿主被写成 gap

- 输入：附件缩略图只是“布局容器 + 正式图标/关闭按钮”，执行者却登记为 `gap` 本地组件。
- 期望：改记 `compose`，写 `layoutOnly=true`、`layoutReason` 和正式子槽位，不创建本地主组件；宿主有视觉表面时才允许正式宿主。

## 87. compose 没有宿主也没有布局声明

- 输入：`compose` 槽位 `chosenAssets` 为空，也没有 `layoutOnly` / `layoutReason`。
- 期望：build 拒绝；纯布局组合必须显式声明，正式宿主必须进 `chosenAssets`。

## 88. gap 只搜一次就下结论

- 输入：`searchAttempts` 只有一条 `semantic`，候选全被淘汰后直接记 `gap`。
- 期望：build 拒绝；`gap` 需要两次 `semantic` 和一次 `published-name`/`page-routed`/`inventory` 兜底。

## 89. gap 的 inventory 自造范围

- 输入：`libraryCatalog` 完整，但 `gap` 的 `eligibleIds` 写了目录里没有的资产。
- 期望：build 拒绝；`eligibleIds` 必须是 `libraryCatalog.ids` 的子集；目录非空而 eligible 为空时另需 `scopeReason`。

## 90. gap 没有组合尝试证据

- 输入：`gap` 有完整 inventory 和候选排除，但 `composeTrials` 为空。
- 期望：build 拒绝；`gap` 必须先记录 host、parts（目录内资产）和失败理由，证明正式件组合也覆盖不了。

## 91. 文字需求先产出 PRD

- 输入：用户只给一句“帮我做一个任务列表页”，没有 PRD 文件。
- 期望：`intake.inputMode=text`；先产出不预设页面方案的 Requirement Spec/PRD 并登记 `provenance=authored` 的 `source` 证据，再形成 reviewed `experienceDecision`；plan 门禁才通过；不跳过 Experience Decision 直接选型或上屏。

## 92. 上传 PRD 原文直读

- 输入：用户上传 PRD 文件并要求“按这份 PRD 输出，不用总结和优化”。
- 期望：`inputMode=prd-file`、`rewritePolicy=verbatim`、`prdArtifact` 为空；不生成精简版或优化版 PRD，不改写、不扩写、不重排结构；需求逐条回指原文位置。

## 93. 未经要求把上传 PRD 改写成摘要

- 输入：用户只说“按这份 PRD 输出”，执行者却把 PRD 压缩成“需求摘要”再当原文使用。
- 期望：plan 门禁拒绝（verbatim 模式出现 authored source 证据）；恢复方式是按原文重新读取，不是让用户接受摘要。

## 94. 文字需求只写了标题级 Requirement Spec

- 输入：文字需求产出的 Requirement Spec/PRD 只有目标和一段话，缺目标用户、用户任务、成功标准、范围、业务规则/数据/权限/依赖、进入上下文、预期结果、异常事实、验收标准和未决问题。
- 期望：Requirements Review 拒绝进入 Experience Decision；先补齐“问题与约束”层。此阶段不得为了完整性提前补页面地图、Modal/Drawer/Page、任务流、状态矩阵或内容脚本。

## 95. 用户要求改写 PRD

- 输入：用户上传 PRD 并说“帮我精简成执行版再出稿”。
- 期望：`rewritePolicy=rewrite-authorized`，`rewriteAuthorization.evidenceRefs` 指向用户原话的 authorization 证据；先读原文再产出改写稿，记录改写范围与未覆盖 requirement；不因默认 verbatim 拒绝用户要求。

## 96. 交付物必须问清

- 输入：用户给出完整 PRD，但没有说 Figma 还是网页 Demo。
- 期望：plan 前主动问一次；用户回复 Figma 时 `deliverable=figma`，回复 Demo 时 `deliverable=web-demo`，两者都要时 `both`；`deliverableDecision.evidenceRefs` 指向回复，不靠猜。

## 97. 交付物未回复默认 Demo

- 输入：AI 问“要 Figma 还是网页 Demo”，用户没回，继续给别的指令。
- 期望：`source=asked`、`userChoice=null`、`fallbackReason=no-reply`，`deliverable=web-demo`；不默认 Figma，也不反复追问。

## 98. 无法询问默认 Demo

- 输入：批量/自动化运行，没有交互通道可以问交付物。
- 期望：`source=fallback`、`fallbackReason=cannot-ask`，`deliverable=web-demo`；交付报告说明这是默认值，不是用户选择。

## 99. 正式件必须来自当次 liveLibrary

- 输入：槽位记 `formal-instance`，`chosenAssets` 指向一个本次搜索从未观察到的 key。
- 期望：build 拒绝；顶层 `liveLibrary` 必须记录 `libraryKey`、版本或指纹、`observedAt` 和本次观察到的 `ids`，选中 key 必须属于 `ids`。

## 100. liveLibrary 与 libraryCatalog 身份冲突

- 输入：`gap` 槽位的 `libraryCatalog.libraryKey` 与顶层 `liveLibrary.libraryKey` 不一致。
- 期望：build 拒绝；完整盘点必须锚定同一个当次发布库身份。

## 101. 评审 finding 未进问题台账

- 输入：final 评审报告有一条 `severity=P2` 的 finding，但 `issueIds` 为空、finding 没有 `issueId`。
- 期望：deliver 拒绝；P0/P1/P2 finding 必须带 `issueId`，且与问题台账的 severity 一致。

## 102. system 维度自审

- 输入：final `system` 评审的 reviewerId 等于 designerId。
- 期望：deliver 拒绝；plan/final 每个维度都要独立评审，UX 与 UI 另须不同评审者。

## 103. Demo live key 与本地 assetKey 不一致

- 输入：当次 live key 漂移，`manifestAssetKey` 仍指向本地正式封装，但没有记 `syncMismatch`。
- 期望：deliver 拒绝；补 `reason` 与 `evidenceRefs` 后通过，Demo 仍用正式封装，不手绘绕过。

## 104. 次要能力 degraded

- 输入：`demo-interaction` probe degraded，但实例化和截图已成立。
- 期望：不阻断；只有必需能力 blocked/degraded 才整体 paused-blocked。

## 105. web-demo 缺 screenshot 能力

- 输入：`web-demo` 交付，但 capabilities 没有 `screenshot`。
- 期望：build 拒绝；截图是 Figma 与 Demo 共同的必需取证能力。

## 106. gap 盘点漏判

- 输入：`inventory.scannedIds` 有两项，candidates 只覆盖其中一项。
- 期望：build 拒绝；每个 scanned id 都要有候选判定或排除记录。

## 107. 只读报告门禁

- 输入：`review-existing` 没有原 PRD，只有截图、final 评审和问题台账。
- 期望：`--gate report` 通过并记录 `stage=report`；调用 `--gate build` 被拒绝，不能冒充设计交付。

## 108. 只读报告输出 issues

- 输入：`review-existing` 的 final 评审 `verdict=issues`，P1 finding 带 `issueId` 回指问题台账。
- 期望：`--gate report` 通过；`verdict=issues` 必须有结构化 findings，且 P0/P1/P2 必须回指台账。

## 109. 只读报告缺当次截图

- 输入：`review-existing` 的可见 unit 没有当前 revision 的 screenshot capture。
- 期望：`--gate report` 拒绝；只读报告也必须以当次截图为主证据。

## 110. chosenAssets 只认 liveLibrary.ids

- 输入：候选资产只出现在 `libraryCatalog.ids`，不在 `liveLibrary.ids`，却被写进 `chosenAssets`。
- 期望：build 拒绝；`liveLibrary` 是当次发布库身份，`libraryCatalog` 只用于证明缺口。

## 111. both 分交付物交互等级

- 输入：`both` 的 unit 记 `interactionLevels={figma:design,demo:executed}`，两端 interaction 检查分别引用对应 level。
- 期望：deliver 通过；Figma 静态状态屏记 `design`，可点走查记 `executed`，不得把 Figma 伪造成 `executed`。

## 112. both 现网基线按交付物分开

- 输入：`both` 且 `liveBaseline=replicated`，只提供 Figma 的 baseline 对照。
- 期望：deliver 拒绝；Figma 与 Demo 各自需要当前 revision 的 baseline 检查，不能互相顶替。

## 113. 修复触发回 plan-review

- 输入：implementation 报告 `structureChange=true` 或 `changeImpact=main-action-change`。
- 期望：deliver 拒绝并返回 `nextAction=resume-plan`；不得直接进入最终交付。

## 114. paused-blocked 状态

- 输入：run 记录 `status=paused-blocked` 且写有 blockers 与恢复入口。
- 期望：状态合法但所有交付门禁拒绝，必须恢复并回到对应阶段后才能 complete。

## 115. 空发布库证明

- 输入：`liveLibrary.ids=[]` 且 `libraryCatalog.ids=[]`、槽位 inventory 全空、有工具证据与 `emptyProof=true`。
- 期望：build 通过；空库也必须给原始空目录证明，不能只写一个空数组。

## 116. 无 PRD 的授权迭代

- 输入：用户明确授权修复旧稿但没有 PRD 文件；把授权原文登记为 required source，requirements 以 `origin=derived` 回指观察事实与授权位置。
- 期望：plan 门禁通过并按 `reviewed-plan` 进入 build；`review-observed` 仍只读，不得直接写入。

## 117. nextAction 与 taskEvidenceRefs 校验

- 输入：`nextAction` 写成未知值，或 `taskEvidenceRefs` 指向非 task 证据。
- 期望：门禁拒绝；`nextAction` 必须是已知恢复/停止动作，中性任务脚本证据 kind 必须是 `task`。

## 118. plan 阶段独立评审隔离

- 输入：`independent-review` 能力证据 `isolated=false`，但 plan 维度的 reviewerId 已与 designerId 不同。
- 期望：plan 门禁拒绝；隔离能力不只看角色名，plan 与 deliver 都要核对隔离机制和评审者身份。

## 119. live 库必须是完整目录的子集

- 输入：`libraryCatalog.complete=true` 且 `ids` 为完整发布集合，但 `liveLibrary.ids` 里多出一个目录中不存在的组件。
- 期望：build 拒绝；完整目录是权威集合，现场观测只能少不能凭空多出未发布组件。

## 120. 计划评审触发器必须是受控值

- 输入：implementation 写 `requiresPlanReview='true'` 这类非布尔值，或 `changeImpact=['ia-change']` 这类未登记取值。
- 期望：deliver 拒绝；布尔标志必须是真布尔，changeImpact 只能使用文档登记的变更类型，未知字符串不能绕过回 plan 的触发器。

## 121. 写授权 scope 必须是字符串数组

- 输入：`authorization.scope='target'` 单字符串，或空数组。
- 期望：build 拒绝；scope 必须是至少一个非空字符串的数组，不能用子串匹配冒充目标授权。

## 122. blockers 必须是数组

- 输入：run 记录 `blockers={}` 这类对象。
- 期望：门禁拒绝；blockers 必须是数组，空对象不能被当成“没有阻塞”。

## 123. 评审 packetRef 必须指向 packet 证据

- 输入：review 的 `packetRef` 指向工具证据或不存在的 id。
- 期望：门禁拒绝；packetRef 必须引用 `kind=packet` 的证据，防止用任意证据冒充盲评包。

## 124. taskEvidenceRefs 可省略但不得错指

- 输入：省略 `taskEvidenceRefs` 字段，或让它指向非 task 证据。
- 期望：省略时门禁按空数组处理并放行；一旦填写，每一项都必须是 `kind=task` 的证据。

## 125. 空对象不得冒充空数组

- 输入：`slotBindings={}`、`childSlotIds={}`、`supersedes={}`、`writeWhitelist={}` 或 `expectedFacts=[]` 这类与声明类型不符的值。
- 期望：门禁拒绝；数组字段必须是数组、对象字段必须是对象，空对象/空列表不能被当成“没有内容”而放行。

## 126. 澄清记录与授权布尔类型

- 输入：`intake.clarifications` 里某项缺 `question` 或 `answer` 不是字符串/null；或 `authorization.fix={}` 这类非布尔值。
- 期望：门禁拒绝；澄清要能追溯追问与回复，授权标志必须是真布尔，不能被对象等值冒充。

## 127. 候选与盘点数组类型

- 输入：`candidates=['component']`、`chosenAssets=[{}]`、`inventory.eligibleIds=[1]` 或 `inventory.exclusions=[{}]`。
- 期望：门禁拒绝；candidates 必须是对象数组，chosenAssets/eligibleIds/scannedIds 必须是字符串数组，exclusions 每项必须带 id。

## 128. checks 与 liveLibrary 字段类型

- 输入：check 的 `unitId`/`deliverable` 写成对象，或 `liveLibrary.version`/`fingerprint` 写成对象。
- 期望：门禁拒绝；check 必须有非空字符串 unitId 与 deliverable，库版本/指纹只能是字符串或 null。

## 129. 独立 Demo slug 必须能生成合法组件名

- 输入：用 `1`、`1-abc` 这类以数字开头的 slug 生成独立业务 Demo。
- 期望：scaffold 拒绝；slug 必须以小写字母开头，避免生成 `1Screen` 这类非法组件标识符。

## 130. Fast 路由不得覆盖结构风险

- 输入：`executionProfile.level=fast`，但 assessment 中 `navigationChanged=true`、`permissionChanged=true` 或 `partialSuccess=true` 任一成立。
- 期望：plan 门禁拒绝并给出 minimum=full；不得因为 PRD 短、unit 少或组件已存在继续 Fast。

## 131. Fast 允许精简评审维度

- 输入：低风险单 unit、task model 不变、`executionProfile=fast`，plan 只有 requirements + experience 独立评审，final 只有独立 ui 评审；Experience report 的 `profileVerdict=keep` 且 happy-path simulation 通过。
- 期望：plan/deliver 允许通过；不得机械要求 Full 的七个评审维度。

## 132. Fast 发现真实 gap 自动升级

- 输入：plan 时满足 Fast，但 resolve 后槽位证明为 `gap`，或 compose 不是 `layoutOnly` 的简单宿主。
- 期望：build 拒绝并要求升级到 Standard；不能在 Fast 中继续全库盘点、自建新组件并冒充低成本路径。

## 133. 布局几何门禁不随档位降级

- 输入：组件实例身份与 description 都正确，但 `layout-geometry` 缺失，或同类 sibling 的实际间距 `[12,16,12]` 在 tolerance=1 下写 `within`。
- 期望：deliver 拒绝；Fast/Standard/Full 都必须有真实几何读回，组件调用正确不能抵消对齐/间距错误。

## 134. reviewer 维度可在一次隔离调用中批量产出

- 输入：Fast plan 由同一隔离 reviewer 在一次调用里分别输出 requirements 与 experience 两份结构化 review record，reviewerId 相同且不等于 designerId；final UI 使用另一隔离 reviewer。
- 期望：允许；独立性要求的是材料隔离和 reviewer 身份，不要求每个 dimension 单独启动一次 agent。若同一阶段同时存在 UX 与 UI，二者仍必须不同 reviewer。

## 135. 现有页面与组件库 Template 必须先匹配并按页面级复用

- 输入：用户要在现有流程后增加内容；原输入文件已有可接入页面，组件库 `【AI参考案例】Template` 内也存在名称或流程相近的子页面，或者本轮请求还给出用户参考页。
- 期望：UX/UI Freeze 后、组件解析前，先扫描原输入文件页面并写 `existingPageScan`，再检查 Template 子流程和用户参考。命中现有页面时判断 `direct-reuse` 或 `adapt-reuse`；直接复用只调整流程位置，改造复用列出实际 changeScope，直接/改造复用现有业务页面时对应 unit 必须有匹配 `liveBaseline`。只借鉴局部记 `reference-only`，不匹配记 `no-match`。有效旧页面可成为流程一步并给后续新页面提供壳层、导航、状态和内容连续性提示。来源只读，业务输出仍在原输入文件；不得因为来源已在 Skill 或原请求中出现而再次索要。

## 136. 表单未完成与真实错误分离

- 输入：反馈页必选类型、必填描述（无最少字数要求），可选图片；依次初次进入、仅选类型、输入一个有效字符、清空、失焦、按回车。
- 期望：初始/部分/清空/空值失焦均置灰禁用且无红字或错误装饰，组件下方不预留错误占位、不顶开布局；有效字符满足描述必填，不擅加长度门槛；图片为空不阻止提交；禁用状态回车不发请求、不提示错误。截图与实际状态一致。
- 边界：明确要求至少 10 字时，9 字为未完成，使用中性计数，10 字才可提交；非空邮箱格式错误经 Toast 报出并点名字段，组件下方不出现红字、不改变下方元素位置；真实提交网络失败保留输入，用 Toast 说明原因和重试入口，不画成“请填写”。错误稿与默认稿几何一致。

## 执行方式

自动契约反例：`python3 -m unittest discover -s tests -v`。运行记录契约版本为 3；场景 27～44、77～90、96～109、111～118 和 119～135 还需要独立代理基于实际输入走查行为；写清测试材料和观察，不能仅勾选期望。真实 Figma 集成回归需要可访问库、字体、隔离评审能力和实际 PRD，独立列执行状态，不用模拟替代；清单见 [使用说明](../docs/usage-guide.md) 的真实 MCP 回归一节。
