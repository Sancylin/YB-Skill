// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3616-10908
// source=src/generated/components.tsx
// component=Tooltip
import figma from 'figma'

const instance = figma.selectedInstance
const prop_icon = instance.getSlot("icon")
const prop_showIcon = instance.getBoolean("showIcon")
const prop_showClose = instance.getBoolean("showClose")
const prop_type = instance.getEnum("type", {
  "normal": "normal",
  "mix": "mix"
})
const prop_direction = instance.getEnum("direction", {
  "up": "up",
  "bottom": "bottom"
})

export default {
  example: figma.code`<Tooltip ${prop_icon ? figma.code` icon={${prop_icon}}` : ''} ${prop_showIcon ? "showIcon" : ''} ${prop_showClose ? "showClose" : ''} type="${prop_type}" direction="${prop_direction}" />`,
  imports: ['import { Tooltip } from "./src/generated/components"'],
  id: "yb-3616-10908",
  metadata: {
    nestable: false,
    props: {
  "icon": {
    "figmaName": "icon",
    "type": "SLOT",
    "options": []
  },
  "showIcon": {
    "figmaName": "showIcon",
    "type": "BOOLEAN",
    "options": []
  },
  "showClose": {
    "figmaName": "showClose",
    "type": "BOOLEAN",
    "options": []
  },
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "normal",
      "mix"
    ]
  },
  "direction": {
    "figmaName": "direction",
    "type": "VARIANT",
    "options": [
      "up",
      "bottom"
    ]
  }
},
  },
}
