// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=4169-19868
// source=src/generated/components.tsx
// component=MenuVertical
import figma from 'figma'

const instance = figma.selectedInstance
const prop_defaultItems = instance.getSlot("defaultItems")
const prop_groupItems = instance.getSlot("GroupItems")
const prop_showGroupItems = instance.getBoolean("showGroupItems")
const prop_direction = instance.getEnum("direction", {
  "up": "up",
  "down": "down"
})

export default {
  example: figma.code`<MenuVertical ${prop_defaultItems ? figma.code` defaultItems={${prop_defaultItems}}` : ''} ${prop_groupItems ? figma.code` groupItems={${prop_groupItems}}` : ''} ${prop_showGroupItems ? "showGroupItems" : ''} direction="${prop_direction}" />`,
  imports: ['import { MenuVertical } from "./src/generated/components"'],
  id: "yb-4169-19868",
  metadata: {
    nestable: false,
    props: {
  "defaultItems": {
    "figmaName": "defaultItems",
    "type": "SLOT",
    "options": []
  },
  "groupItems": {
    "figmaName": "GroupItems",
    "type": "SLOT",
    "options": []
  },
  "showGroupItems": {
    "figmaName": "showGroupItems",
    "type": "BOOLEAN",
    "options": []
  },
  "direction": {
    "figmaName": "direction",
    "type": "VARIANT",
    "options": [
      "up",
      "down"
    ]
  }
},
  },
}
