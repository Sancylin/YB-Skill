// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=19766-25427
// source=src/generated/components.tsx
// component=SettingsFullWidthItem
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "单行列表-常规": "单行列表-常规",
  "单行列表-带开关": "单行列表-带开关",
  "双行列表-常规": "双行列表-常规",
  "双行列表-带开关": "双行列表-带开关",
  "三行列表-常规": "三行列表-常规",
  "三行列表-带开关": "三行列表-带开关",
  "居中按钮": "居中按钮",
  "居中按钮-敏感操作": "居中按钮-敏感操作"
})
const prop_showDot = instance.getBoolean("showDot")

export default {
  example: figma.code`<SettingsFullWidthItem type="${prop_type}" ${prop_showDot ? "showDot" : ''} />`,
  imports: ['import { SettingsFullWidthItem } from "./src/generated/components"'],
  id: "yb-19766-25427",
  metadata: {
    nestable: false,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "单行列表-常规",
      "单行列表-带开关",
      "双行列表-常规",
      "双行列表-带开关",
      "三行列表-常规",
      "三行列表-带开关",
      "居中按钮",
      "居中按钮-敏感操作"
    ]
  },
  "showDot": {
    "figmaName": "showDot",
    "type": "BOOLEAN",
    "options": []
  }
},
  },
}
