// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=5731-25475
// source=src/generated/components.tsx
// component=InternalAgentInputButtonCombination
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("Type", {
  "Voice & Plus": "Voice & Plus",
  "Keyboard & Plus": "Keyboard & Plus",
  "Send & Plus": "Send & Plus",
  "Stop & Plus": "Stop & Plus",
  "Send & Voice & Plus": "Send & Voice & Plus",
  "Plus Only": "Plus Only",
  "Voice Only": "Voice Only",
  "Send Only": "Send Only"
})

export default {
  example: figma.code`<InternalAgentInputButtonCombination type="${prop_type}" />`,
  imports: ['import { InternalAgentInputButtonCombination } from "./src/generated/components"'],
  id: "yb-5731-25475",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "Type",
    "type": "VARIANT",
    "options": [
      "Voice & Plus",
      "Keyboard & Plus",
      "Send & Plus",
      "Stop & Plus",
      "Send & Voice & Plus",
      "Plus Only",
      "Voice Only",
      "Send Only"
    ]
  }
},
  },
}
