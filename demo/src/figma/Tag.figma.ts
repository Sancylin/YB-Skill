// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=6350-4028
// source=src/generated/components.tsx
// component=Tag
import figma from 'figma'

const instance = figma.selectedInstance
const prop_slot = instance.getSlot("Slot")
const prop_showIcon = instance.getBoolean("Show Icon")
const prop_type = instance.getEnum("type", {
  "Badge": "Badge",
  "Default": "Default",
  "Role": "Role",
  "Bot": "Bot"
})

export default {
  example: figma.code`<Tag ${prop_slot ? figma.code` slot={${prop_slot}}` : ''} ${prop_showIcon ? "showIcon" : ''} type="${prop_type}" />`,
  imports: ['import { Tag } from "./src/generated/components"'],
  id: "yb-6350-4028",
  metadata: {
    nestable: false,
    props: {
  "slot": {
    "figmaName": "Slot",
    "type": "SLOT",
    "options": []
  },
  "showIcon": {
    "figmaName": "Show Icon",
    "type": "BOOLEAN",
    "options": []
  },
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "Badge",
      "Default",
      "Role",
      "Bot"
    ]
  }
},
  },
}
