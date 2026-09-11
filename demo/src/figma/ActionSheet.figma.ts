// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3312-37197
// source=src/generated/components.tsx
// component=ActionSheet
import figma from 'figma'

const instance = figma.selectedInstance
const prop_showDesc = instance.getBoolean("Show desc")
const prop_item = instance.getSlot("item")
const prop_desc = instance.getSlot("desc")

export default {
  example: figma.code`<ActionSheet ${prop_showDesc ? "showDesc" : ''} ${prop_item ? figma.code` item={${prop_item}}` : ''} ${prop_desc ? figma.code` desc={${prop_desc}}` : ''} />`,
  imports: ['import { ActionSheet } from "./src/generated/components"'],
  id: "yb-3312-37197",
  metadata: {
    nestable: false,
    props: {
  "showDesc": {
    "figmaName": "Show desc",
    "type": "BOOLEAN",
    "options": []
  },
  "item": {
    "figmaName": "item",
    "type": "SLOT",
    "options": []
  },
  "desc": {
    "figmaName": "desc",
    "type": "SLOT",
    "options": []
  }
},
  },
}
