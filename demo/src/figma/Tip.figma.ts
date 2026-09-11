// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=6229-10808
// source=src/generated/components.tsx
// component=Tip
import figma from 'figma'

const instance = figma.selectedInstance
const prop_line = instance.getEnum("line", {
  "single": "single",
  "double": "double"
})

export default {
  example: figma.code`<Tip line="${prop_line}" />`,
  imports: ['import { Tip } from "./src/generated/components"'],
  id: "yb-6229-10808",
  metadata: {
    nestable: false,
    props: {
  "line": {
    "figmaName": "line",
    "type": "VARIANT",
    "options": [
      "single",
      "double"
    ]
  }
},
  },
}
