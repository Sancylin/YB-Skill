// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=5731-25367
// source=src/generated/components.tsx
// component=InternalAgentInputIcon
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("Type", {
  "Camera": "Camera",
  "Voice": "Voice",
  "Plus": "Plus",
  "Keyboard": "Keyboard",
  "Sticker": "Sticker",
  "Photo": "Photo"
})

export default {
  example: figma.code`<InternalAgentInputIcon type="${prop_type}" />`,
  imports: ['import { InternalAgentInputIcon } from "./src/generated/components"'],
  id: "yb-5731-25367",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "Type",
    "type": "VARIANT",
    "options": [
      "Camera",
      "Voice",
      "Plus",
      "Keyboard",
      "Sticker",
      "Photo"
    ]
  }
},
  },
}
