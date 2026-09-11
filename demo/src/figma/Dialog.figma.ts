// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=434-5381
// source=src/generated/components.tsx
// component=Dialog
import figma from 'figma'

const instance = figma.selectedInstance
const prop_picIconSlot = instance.getSlot("pic&iconSlot")
const prop_picIconSwitch = instance.getBoolean("pic&iconSwitch")
const prop_titleSwitch = instance.getBoolean("titleSwitch")
const prop_bodySlot = instance.getSlot("bodySlot")
const prop_bodySwitch = instance.getBoolean("bodySwitch")

export default {
  example: figma.code`<Dialog ${prop_picIconSlot ? figma.code` picIconSlot={${prop_picIconSlot}}` : ''} ${prop_picIconSwitch ? "picIconSwitch" : ''} ${prop_titleSwitch ? "titleSwitch" : ''} ${prop_bodySlot ? figma.code` bodySlot={${prop_bodySlot}}` : ''} ${prop_bodySwitch ? "bodySwitch" : ''} />`,
  imports: ['import { Dialog } from "./src/generated/components"'],
  id: "yb-434-5381",
  metadata: {
    nestable: false,
    props: {
  "picIconSlot": {
    "figmaName": "pic&iconSlot",
    "type": "SLOT",
    "options": []
  },
  "picIconSwitch": {
    "figmaName": "pic&iconSwitch",
    "type": "BOOLEAN",
    "options": []
  },
  "titleSwitch": {
    "figmaName": "titleSwitch",
    "type": "BOOLEAN",
    "options": []
  },
  "bodySlot": {
    "figmaName": "bodySlot",
    "type": "SLOT",
    "options": []
  },
  "bodySwitch": {
    "figmaName": "bodySwitch",
    "type": "BOOLEAN",
    "options": []
  }
},
  },
}
