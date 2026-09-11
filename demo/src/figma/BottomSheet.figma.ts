// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=2866-50905
// source=src/generated/components.tsx
// component=BottomSheet
import figma from 'figma'

const instance = figma.selectedInstance
const prop_handle = instance.getBoolean("handle")
const prop_content = instance.getSlot("content")
const prop_navBar = instance.getBoolean("navBar")
const prop_buttonGroup = instance.getBoolean("buttonGroup")

export default {
  example: figma.code`<BottomSheet ${prop_handle ? "handle" : ''} ${prop_content ? figma.code` content={${prop_content}}` : ''} ${prop_navBar ? "navBar" : ''} ${prop_buttonGroup ? "buttonGroup" : ''} />`,
  imports: ['import { BottomSheet } from "./src/generated/components"'],
  id: "yb-2866-50905",
  metadata: {
    nestable: false,
    props: {
  "handle": {
    "figmaName": "handle",
    "type": "BOOLEAN",
    "options": []
  },
  "content": {
    "figmaName": "content",
    "type": "SLOT",
    "options": []
  },
  "navBar": {
    "figmaName": "navBar",
    "type": "BOOLEAN",
    "options": []
  },
  "buttonGroup": {
    "figmaName": "buttonGroup",
    "type": "BOOLEAN",
    "options": []
  }
},
  },
}
