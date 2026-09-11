// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=434-6365
// source=src/generated/components.tsx
// component=InternalDialogBody
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "singleText": "singleText",
  "multiText": "multiText",
  "overflowText": "overflowText",
  "leftCheckbox": "leftCheckbox",
  "middleCheckbox": "middleCheckbox"
})

export default {
  example: figma.code`<InternalDialogBody type="${prop_type}" />`,
  imports: ['import { InternalDialogBody } from "./src/generated/components"'],
  id: "yb-434-6365",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "singleText",
      "multiText",
      "overflowText",
      "leftCheckbox",
      "middleCheckbox"
    ]
  }
},
  },
}
