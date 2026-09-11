// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=15331-18879
// source=src/generated/components.tsx
// component=InternalMDIMG
import figma from 'figma'

const instance = figma.selectedInstance
const prop_iMGS = instance.getSlot("IMGS")
const prop_type = instance.getEnum("type", {
  "3:4": "3:4",
  "4:3": "4:3",
  "1:1": "1:1",
  "multi": "multi",
  "grid": "grid",
  "type6": "type6",
  "singleAIGC": "singleAIGC"
})

export default {
  example: figma.code`<InternalMDIMG ${prop_iMGS ? figma.code` iMGS={${prop_iMGS}}` : ''} type="${prop_type}" />`,
  imports: ['import { InternalMDIMG } from "./src/generated/components"'],
  id: "yb-15331-18879",
  metadata: {
    nestable: true,
    props: {
  "iMGS": {
    "figmaName": "IMGS",
    "type": "SLOT",
    "options": []
  },
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "3:4",
      "4:3",
      "1:1",
      "multi",
      "grid",
      "type6",
      "singleAIGC"
    ]
  }
},
  },
}
