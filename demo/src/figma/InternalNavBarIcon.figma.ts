// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3216-33636
// source=src/generated/components.tsx
// component=InternalNavBarIcon
import figma from 'figma'

const instance = figma.selectedInstance
const prop_leftSlot = instance.getSlot("Left Slot")
const prop_rightSlot = instance.getSlot("Right Slot")
const prop_showRightIcon = instance.getBoolean("Show Right icon")
const prop_showLeftIcon = instance.getBoolean("Show Left icon")
const prop_bg = instance.getEnum("bg", {
  "on": "on",
  "off": "off"
})

export default {
  example: figma.code`<InternalNavBarIcon ${prop_leftSlot ? figma.code` leftSlot={${prop_leftSlot}}` : ''} ${prop_rightSlot ? figma.code` rightSlot={${prop_rightSlot}}` : ''} ${prop_showRightIcon ? "showRightIcon" : ''} ${prop_showLeftIcon ? "showLeftIcon" : ''} bg="${prop_bg}" />`,
  imports: ['import { InternalNavBarIcon } from "./src/generated/components"'],
  id: "yb-3216-33636",
  metadata: {
    nestable: true,
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
  "bg": {
    "figmaName": "bg",
    "type": "VARIANT",
    "options": [
      "on",
      "off"
    ]
  }
},
  },
}
