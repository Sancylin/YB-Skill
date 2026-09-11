// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=443-2123
// source=src/generated/components.tsx
// component=InternalButtonGroup_443_2123
import figma from 'figma'

const instance = figma.selectedInstance
const prop_buttonGroup = instance.getSlot("buttonGroup")
const prop_num = instance.getEnum("num", {
  "1": "1",
  "2": "2",
  "multi": "multi"
})

export default {
  example: figma.code`<InternalButtonGroup_443_2123 ${prop_buttonGroup ? figma.code` buttonGroup={${prop_buttonGroup}}` : ''} num="${prop_num}" />`,
  imports: ['import { InternalButtonGroup_443_2123 } from "./src/generated/components"'],
  id: "yb-443-2123",
  metadata: {
    nestable: true,
    props: {
  "buttonGroup": {
    "figmaName": "buttonGroup",
    "type": "SLOT",
    "options": []
  },
  "num": {
    "figmaName": "num",
    "type": "VARIANT",
    "options": [
      "2",
      "1",
      "multi"
    ]
  }
},
  },
}
