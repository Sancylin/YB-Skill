// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=4822-26458
// source=src/generated/components.tsx
// component=List
import figma from 'figma'

const instance = figma.selectedInstance
const prop_rightSlot = instance.getSlot("right slot")
const prop_leftSlot = instance.getSlot("left slot")
const prop_showHeader = instance.getBoolean("Show Header")
const prop_slot = instance.getSlot("slot")
const prop_type = instance.getEnum("type", {
  "smallFile": "smallFile",
  "settings": "settings",
  "largeFile": "largeFile"
})

export default {
  example: figma.code`<List ${prop_rightSlot ? figma.code` rightSlot={${prop_rightSlot}}` : ''} ${prop_leftSlot ? figma.code` leftSlot={${prop_leftSlot}}` : ''} ${prop_showHeader ? "showHeader" : ''} ${prop_slot ? figma.code` slot={${prop_slot}}` : ''} type="${prop_type}" />`,
  imports: ['import { List } from "./src/generated/components"'],
  id: "yb-4822-26458",
  metadata: {
    nestable: false,
    props: {
  "rightSlot": {
    "figmaName": "right slot",
    "type": "SLOT",
    "options": []
  },
  "leftSlot": {
    "figmaName": "left slot",
    "type": "SLOT",
    "options": []
  },
  "showHeader": {
    "figmaName": "Show Header",
    "type": "BOOLEAN",
    "options": []
  },
  "slot": {
    "figmaName": "slot",
    "type": "SLOT",
    "options": []
  },
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "smallFile",
      "settings",
      "largeFile"
    ]
  }
},
  },
}
