// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=2970-6179
// source=src/generated/components.tsx
// component=InternalActionsheetItem
import figma from 'figma'

const instance = figma.selectedInstance
const prop_icon = instance.getSlot("icon")
const prop_showIcon = instance.getBoolean("Show icon")
const prop_icon2 = instance.getSlot("icon2")
const prop_icon3 = instance.getSlot("icon3")
const prop_state = instance.getEnum("state", {
  "Default": "Default",
  "Disable": "Disable",
  "Pressed": "Pressed"
})

export default {
  example: figma.code`<InternalActionsheetItem ${prop_icon ? figma.code` icon={${prop_icon}}` : ''} ${prop_showIcon ? "showIcon" : ''} ${prop_icon2 ? figma.code` icon2={${prop_icon2}}` : ''} ${prop_icon3 ? figma.code` icon3={${prop_icon3}}` : ''} state="${prop_state}" />`,
  imports: ['import { InternalActionsheetItem } from "./src/generated/components"'],
  id: "yb-2970-6179",
  metadata: {
    nestable: true,
    props: {
  "icon": {
    "figmaName": "icon",
    "type": "SLOT",
    "options": []
  },
  "showIcon": {
    "figmaName": "Show icon",
    "type": "BOOLEAN",
    "options": []
  },
  "icon2": {
    "figmaName": "icon2",
    "type": "SLOT",
    "options": []
  },
  "icon3": {
    "figmaName": "icon3",
    "type": "SLOT",
    "options": []
  },
  "state": {
    "figmaName": "state",
    "type": "VARIANT",
    "options": [
      "Default",
      "Disable",
      "Pressed"
    ]
  }
},
  },
}
