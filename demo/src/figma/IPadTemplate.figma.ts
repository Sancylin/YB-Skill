// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=8535-12469
// source=src/generated/components.tsx
// component=IPadTemplate
import figma from 'figma'

const instance = figma.selectedInstance
const prop_displayMode = instance.getEnum("展示方式", {
  "横屏": "横屏",
  "竖屏": "竖屏"
})

export default {
  example: figma.code`<IPadTemplate displayMode="${prop_displayMode}" />`,
  imports: ['import { IPadTemplate } from "./src/generated/components"'],
  id: "yb-8535-12469",
  metadata: {
    nestable: false,
    props: {
  "displayMode": {
    "figmaName": "展示方式",
    "type": "VARIANT",
    "options": [
      "横屏",
      "竖屏"
    ]
  }
},
  },
}
