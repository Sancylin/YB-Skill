// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=1396-5016
// source=src/generated/components.tsx
// component=Button
import figma from 'figma'

const instance = figma.selectedInstance
const prop_leftSlot = instance.getSlot("Left Slot")
const prop_rightSlot = instance.getSlot("Right Slot")
const prop_rightIcon = instance.getBoolean("Right icon")
const prop_leftIcon = instance.getBoolean("Left icon")
const prop_shadow = instance.getBoolean("Shadow")
const prop_type = instance.getEnum("Type", {
  "Primary": "Primary",
  "Secondary": "Secondary",
  "Gray": "Gray",
  "Alert": "Alert",
  "Outline": "Outline",
  "Text": "Text"
})
const prop_size = instance.getEnum("Size", {
  "L": "L",
  "M": "M",
  "M-": "M-",
  "S+": "S+",
  "S": "S",
  "XS": "XS"
})
const prop_state = instance.getEnum("State", {
  "Default": "Default",
  "Pressed": "Pressed",
  "Disable": "Disable"
})

export default {
  example: figma.code`<Button ${prop_leftSlot ? figma.code` leftSlot={${prop_leftSlot}}` : ''} ${prop_rightSlot ? figma.code` rightSlot={${prop_rightSlot}}` : ''} ${prop_rightIcon ? "rightIcon" : ''} ${prop_leftIcon ? "leftIcon" : ''} ${prop_shadow ? "shadow" : ''} type="${prop_type}" size="${prop_size}" state="${prop_state}" />`,
  imports: ['import { Button } from "./src/generated/components"'],
  id: "yb-1396-5016",
  metadata: {
    nestable: false,
    props: {
  "leftSlot": {
    "figmaName": "Left Slot",
    "type": "SLOT",
    "options": []
  },
  "rightSlot": {
    "figmaName": "Right Slot",
    "type": "SLOT",
    "options": []
  },
  "rightIcon": {
    "figmaName": "Right icon",
    "type": "BOOLEAN",
    "options": []
  },
  "leftIcon": {
    "figmaName": "Left icon",
    "type": "BOOLEAN",
    "options": []
  },
  "shadow": {
    "figmaName": "Shadow",
    "type": "BOOLEAN",
    "options": []
  },
  "type": {
    "figmaName": "Type",
    "type": "VARIANT",
    "options": [
      "Primary",
      "Secondary",
      "Gray",
      "Alert",
      "Outline",
      "Text"
    ]
  },
  "size": {
    "figmaName": "Size",
    "type": "VARIANT",
    "options": [
      "L",
      "M",
      "M-",
      "S+",
      "S",
      "XS"
    ]
  },
  "state": {
    "figmaName": "State",
    "type": "VARIANT",
    "options": [
      "Default",
      "Pressed",
      "Disable"
    ]
  }
},
  },
}
