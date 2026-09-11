# 基础规范现场解析

只用于真实缺口的自建层，或 Screen Spec 需要设备、画布、间距而组件 description 不足时。正式实例内部视觉不要再绑一遍。

本文件只指出规范源里去哪读。Skill 不保存 hex、字号表、圆角档、断点或间距数字。

## 何时加载

- 现场组件解析结论为 `gap`，进入缺口创建；
- 业务自建 layout-only / surface 需要颜色、文字、圆角、投影、蒙层、分割或间距；
- 设备或画布不确定，需要正式模板和适配规则。

不要为了给正式实例内部再刷一遍 token 而加载本文件。

## 规范源基础页

每次用当次 `get_libraries` 的 libraryKey，调用 `search_design_system`，或打开规范源对应页，读取变量、样式、组件 description 和说明画板正文。证据记入 Slot Evidence。

| 页 | 读什么 |
|---|---|
| `✅ 颜色 Color` | Color 变量 description |
| `✅ 字体 Typography` | Text Style 与 Typography 变量 |
| `✅ 投影 Shadow` | Effect Style description |
| `✅ 圆角 Round` | Round 变量 description |
| `✅ 蒙层 Mask` | 蒙层规范与相关资产 |
| `✅ 分割/描边 Divider` | 分割与描边规范 |
| `✅ iPad端` | `ipad 模板` 组件集 description；同页 `iPad适配规则` 规范说明组件 |
| `✅ 间距 Spacing` | Spacing 变量 description；同页 `间距规范` 说明画板 |

iPad 画布只解决设备窗口和方向：搜 `ipad 模板`，先判断是否 wide 再选竖屏或横屏。断点、主区宽度、Sheet / Alert / Menu 尺寸搜 `iPad适配规则`（规范说明，不是画布），不要把数值抄进 Skill，也不要编造分屏变体。规范说明组件和说明画板只可读，禁止 `createInstance` 到业务稿。

页面边距和自建层间距：搜 Spacing 变量，并打开 `间距规范` 画板看档位语义与例外。正式组件内部 padding / gap 跟该组件走，不要用 Spacing 变量去改实例内部。

## 读法

1. 写出语义角色（页面背景、主文字、surface 圆角、页面边距、iPad 画布等）；
2. `search_design_system`，限制当次 libraryKey；
3. 打开对应基础页，核对该页资产 description 或说明画板；
4. Text Style description 为空时，用 style 名称与层级语义核对，Typography 变量作为绑定目标；不能因 description 空而编造字号或字重；
5. 记录到 Slot Evidence 后再绑定到自建层。

## 输出证据

```text
semanticRole:
searchQuery:
liveAssetName:
liveKey:
type / modes:
descriptionExcerpt:
bindingTarget:
```

无法证明语义或绑定目标时为 `blocked`；插件能力不足时按 [../state-and-fallback.md](../state-and-fallback.md)。
