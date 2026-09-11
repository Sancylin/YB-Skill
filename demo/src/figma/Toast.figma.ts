// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3499-4402
// source=src/generated/components.tsx
// component=Toast
import figma from 'figma'

const instance = figma.selectedInstance
const prop_actionButton = instance.getBoolean("ActionButton")
const prop_icon = instance.getBoolean("Icon")
const prop_iconSlot = instance.getSlot("Icon Slot")
const prop_arrowIcon = instance.getBoolean("ArrowIcon")
const prop_type = instance.getEnum("Type", {
  "Default": "Default",
  "Vertical": "Vertical"
})

export default {
  example: figma.code`<Toast ${prop_actionButton ? "actionButton" : ''} ${prop_icon ? "icon" : ''} ${prop_iconSlot ? figma.code` iconSlot={${prop_iconSlot}}` : ''} ${prop_arrowIcon ? "arrowIcon" : ''} type="${prop_type}" />`,
  imports: ['import { Toast } from "./src/generated/components"'],
  id: "yb-3499-4402",
  metadata: {
    nestable: false,
    props: {
  "actionButton": {
    "figmaName": "ActionButton",
    "type": "BOOLEAN",
    "options": []
  },
  "icon": {
    "figmaName": "Icon",
    "type": "BOOLEAN",
    "options": []
  },
  "iconSlot": {
    "figmaName": "Icon Slot",
    "type": "SLOT",
    "options": []
  },
  "arrowIcon": {
    "figmaName": "ArrowIcon",
    "type": "BOOLEAN",
    "options": []
  },
  "type": {
    "figmaName": "Type",
    "type": "VARIANT",
    "options": [
      "Default",
      "Vertical"
    ]
  }
},
  },
}
