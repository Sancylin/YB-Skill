// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3582-18800
// source=src/generated/components.tsx
// component=MenuHorizontalItem
import figma from 'figma'

const instance = figma.selectedInstance
const prop_check = instance.getBoolean("check")
const prop_entry = instance.getBoolean("entry")
const prop_desc = instance.getBoolean("desc")
const prop_icon = instance.getSlot("icon")
const prop_pressed = instance.getEnum("pressed", {
  "off": "off",
  "on": "on"
})

export default {
  example: figma.code`<MenuHorizontalItem ${prop_check ? "check" : ''} ${prop_entry ? "entry" : ''} ${prop_desc ? "desc" : ''} ${prop_icon ? figma.code` icon={${prop_icon}}` : ''} pressed="${prop_pressed}" />`,
  imports: ['import { MenuHorizontalItem } from "./src/generated/components"'],
  id: "yb-3582-18800",
  metadata: {
    nestable: false,
    props: {
  "check": {
    "figmaName": "check",
    "type": "BOOLEAN",
    "options": []
  },
  "entry": {
    "figmaName": "entry",
    "type": "BOOLEAN",
    "options": []
  },
  "desc": {
    "figmaName": "desc",
    "type": "BOOLEAN",
    "options": []
  },
  "icon": {
    "figmaName": "icon",
    "type": "SLOT",
    "options": []
  },
  "pressed": {
    "figmaName": "pressed",
    "type": "VARIANT",
    "options": [
      "off",
      "on"
    ]
  }
},
  },
}
