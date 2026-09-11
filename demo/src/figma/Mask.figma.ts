// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=67-529
// source=src/generated/components.tsx
// component=Mask
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "drawer mask": "drawer mask",
  "popup mask": "popup mask"
})

export default {
  example: figma.code`<Mask type="${prop_type}" />`,
  imports: ['import { Mask } from "./src/generated/components"'],
  id: "yb-67-529",
  metadata: {
    nestable: false,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "drawer mask",
      "popup mask"
    ]
  }
},
  },
}
