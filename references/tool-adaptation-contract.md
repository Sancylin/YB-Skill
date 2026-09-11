# 当前工具适配

每次会话读取本次所需工具声明；参数和调用限制以当前声明为准。记录工具名、实际参数、响应证据及可获得的声明指纹；宿主未暴露 schema 时写 unknown，不能编造。

- get_libraries 的组织库列表可能支持 offset；只传该接口实际返回的偏移。
- 当前 list_file_components_for_code_connect 仅接受 fileKey，并保证仅返回已发布组件。不存在 cursor 参数；仅将来接口明确支持才分页。不强制返回 published=true。工具输出被截断、失败或完整性未知时不得 complete。
- search_design_system 按当前批量规则调用，一个意图一项。空搜索不证明缺口，也不成为机械换词重试的理由；使用已获准只读目录/页面盘点定位，仍过描述门禁。未执行意图不登记成功。
- get_design_context、use_figma 等若要求读取配套 skill，调用前加载；缺少前置能力明确恢复，不猜 API。
- snapshots 从实际目标读回；截图必须真正获取。错误、临时失败按提示有限重试；未知能力记 unknown。

scripts/runlib/tools.py 提供目录完整性决策辅助；它不调用 MCP，也不鉴定声明真伪。调用者必须以原始工具证据填写 only_published/truncated 等参数。完整发布目录的全量输出只在当前任务目录留存。
