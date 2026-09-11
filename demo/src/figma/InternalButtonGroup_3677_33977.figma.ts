// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3677-33977
// source=src/generated/components.tsx
// component=InternalButtonGroup_3677_33977
import figma from 'figma'

const instance = figma.selectedInstance
const prop_num = instance.getEnum("num", {
  "1": "1",
  "2": "2"
})

export default {
  example: figma.code`<InternalButtonGroup_3677_33977 num="${prop_num}" />`,
  imports: ['import { InternalButtonGroup_3677_33977 } from "./src/generated/components"'],
  id: "yb-3677-33977",
  metadata: {
    nestable: true,
    props: {
  "num": {
    "figmaName": "num",
    "type": "VARIANT",
    "options": [
      "2",
      "1"
    ]
  }
},
  },
}
