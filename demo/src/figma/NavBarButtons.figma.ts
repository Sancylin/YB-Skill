// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=76-689
// source=src/generated/components.tsx
// component=NavBarButtons
import figma from 'figma'

const instance = figma.selectedInstance
const prop_leftSlot = instance.getSlot("Left Slot")
const prop_rightSlot = instance.getSlot("Right Slot")
const prop_showRightIcon = instance.getBoolean("Show Right icon")
const prop_showLeftIcon = instance.getBoolean("Show Left icon")
const prop_type = instance.getEnum("Type", {
  "Single": "Single",
  "Multiple": "Multiple",
  "Icon&Text": "Icon&Text",
  "Text": "Text",
  "Back&Badge": "Back&Badge"
})

export default {
  example: figma.code`<NavBarButtons ${prop_leftSlot ? figma.code` leftSlot={${prop_leftSlot}}` : ''} ${prop_rightSlot ? figma.code` rightSlot={${prop_rightSlot}}` : ''} ${prop_showRightIcon ? "showRightIcon" : ''} ${prop_showLeftIcon ? "showLeftIcon" : ''} type="${prop_type}" />`,
  imports: ['import { NavBarButtons } from "./src/generated/components"'],
  id: "yb-76-689",
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
  "showRightIcon": {
    "figmaName": "Show Right icon",
    "type": "BOOLEAN",
    "options": []
  },
  "showLeftIcon": {
    "figmaName": "Show Left icon",
    "type": "BOOLEAN",
    "options": []
  },
  "type": {
    "figmaName": "Type",
    "type": "VARIANT",
    "options": [
      "Single",
      "Multiple",
      "Icon&Text",
      "Text",
      "Back&Badge"
    ]
  }
},
  },
}
