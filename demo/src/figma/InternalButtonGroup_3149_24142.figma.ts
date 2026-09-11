// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3149-24142
// source=src/generated/components.tsx
// component=InternalButtonGroup_3149_24142
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "1Btn": "1Btn",
  "2BtnHorizantal": "2BtnHorizantal",
  "2BtnVertical": "2BtnVertical"
})

export default {
  example: figma.code`<InternalButtonGroup_3149_24142 type="${prop_type}" />`,
  imports: ['import { InternalButtonGroup_3149_24142 } from "./src/generated/components"'],
  id: "yb-3149-24142",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "1Btn",
      "2BtnHorizantal",
      "2BtnVertical"
    ]
  }
},
  },
}
