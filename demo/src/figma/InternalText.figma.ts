// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3149-26973
// source=src/generated/components.tsx
// component=InternalText
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "singleLine": "singleLine",
  "multiLine": "multiLine"
})

export default {
  example: figma.code`<InternalText type="${prop_type}" />`,
  imports: ['import { InternalText } from "./src/generated/components"'],
  id: "yb-3149-26973",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "singleLine",
      "multiLine"
    ]
  }
},
  },
}
