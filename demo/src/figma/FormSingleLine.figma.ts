// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=8841-7396
// source=src/generated/components.tsx
// component=FormSingleLine
import figma from 'figma'

const instance = figma.selectedInstance
const prop_active = instance.getBoolean("active")
const prop_align = instance.getEnum("align", {
  "middle": "middle",
  "left": "left"
})
const prop_input = instance.getEnum("input", {
  "off": "off",
  "on": "on"
})

export default {
  example: figma.code`<FormSingleLine ${prop_active ? "active" : ''} align="${prop_align}" input="${prop_input}" />`,
  imports: ['import { FormSingleLine } from "./src/generated/components"'],
  id: "yb-8841-7396",
  metadata: {
    nestable: false,
    props: {
  "active": {
    "figmaName": "active",
    "type": "BOOLEAN",
    "options": []
  },
  "align": {
    "figmaName": "align",
    "type": "VARIANT",
    "options": [
      "middle",
      "left"
    ]
  },
  "input": {
    "figmaName": "input",
    "type": "VARIANT",
    "options": [
      "off",
      "on"
    ]
  }
},
  },
}
