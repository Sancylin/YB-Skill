// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=5779-38683
// source=src/generated/components.tsx
// component=AgentInput
import figma from 'figma'

const instance = figma.selectedInstance
const prop_slot = instance.getSlot("Slot")
const prop_leftBtn = instance.getBoolean("Left Btn")
const prop_iconSlot = instance.getSlot("Icon-Slot")
const prop_type = instance.getEnum("Type", {
  "Default": "Default",
  "Voice": "Voice",
  "Inputting": "Inputting",
  "Stopped": "Stopped",
  "Upload": "Upload",
  "Long Text": "Long Text",
  "Atomic-Default": "Atomic-Default",
  "Atomic-Customized": "Atomic-Customized"
})

export default {
  example: figma.code`<AgentInput ${prop_slot ? figma.code` slot={${prop_slot}}` : ''} ${prop_leftBtn ? "leftBtn" : ''} ${prop_iconSlot ? figma.code` iconSlot={${prop_iconSlot}}` : ''} type="${prop_type}" />`,
  imports: ['import { AgentInput } from "./src/generated/components"'],
  id: "yb-5779-38683",
  metadata: {
    nestable: false,
    props: {
  "slot": {
    "figmaName": "Slot",
    "type": "SLOT",
    "options": []
  },
  "leftBtn": {
    "figmaName": "Left Btn",
    "type": "BOOLEAN",
    "options": []
  },
  "iconSlot": {
    "figmaName": "Icon-Slot",
    "type": "SLOT",
    "options": []
  },
  "type": {
    "figmaName": "Type",
    "type": "VARIANT",
    "options": [
      "Default",
      "Voice",
      "Inputting",
      "Stopped",
      "Upload",
      "Long Text",
      "Atomic-Default",
      "Atomic-Customized"
    ]
  }
},
  },
}
