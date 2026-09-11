// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3633-29866
// source=src/generated/components.tsx
// component=MenuHorizontal
import figma from 'figma'

const instance = figma.selectedInstance
const prop_headerItems = instance.getSlot("headerItems")
const prop_defaultItems = instance.getSlot("defaultItems")
const prop_groupItem = instance.getSlot("groupItem")
const prop_showHeaderItem = instance.getBoolean("showHeaderItem")
const prop_showGroupItem = instance.getBoolean("showGroupItem")

export default {
  example: figma.code`<MenuHorizontal ${prop_headerItems ? figma.code` headerItems={${prop_headerItems}}` : ''} ${prop_defaultItems ? figma.code` defaultItems={${prop_defaultItems}}` : ''} ${prop_groupItem ? figma.code` groupItem={${prop_groupItem}}` : ''} ${prop_showHeaderItem ? "showHeaderItem" : ''} ${prop_showGroupItem ? "showGroupItem" : ''} />`,
  imports: ['import { MenuHorizontal } from "./src/generated/components"'],
  id: "yb-3633-29866",
  metadata: {
    nestable: false,
    props: {
  "headerItems": {
    "figmaName": "headerItems",
    "type": "SLOT",
    "options": []
  },
  "defaultItems": {
    "figmaName": "defaultItems",
    "type": "SLOT",
    "options": []
  },
  "groupItem": {
    "figmaName": "groupItem",
    "type": "SLOT",
    "options": []
  },
  "showHeaderItem": {
    "figmaName": "showHeaderItem",
    "type": "BOOLEAN",
    "options": []
  },
  "showGroupItem": {
    "figmaName": "showGroupItem",
    "type": "BOOLEAN",
    "options": []
  }
},
  },
}
