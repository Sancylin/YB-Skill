// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=5759-3000
// source=src/generated/components.tsx
// component=InternalAgentInputPrimaryButton
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("Type", {
  "Send": "Send",
  "Stop": "Stop"
})

export default {
  example: figma.code`<InternalAgentInputPrimaryButton type="${prop_type}" />`,
  imports: ['import { InternalAgentInputPrimaryButton } from "./src/generated/components"'],
  id: "yb-5759-3000",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "Type",
    "type": "VARIANT",
    "options": [
      "Send",
      "Stop"
    ]
  }
},
  },
}
