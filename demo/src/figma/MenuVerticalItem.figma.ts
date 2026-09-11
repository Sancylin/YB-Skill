// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3582-29348
// source=src/generated/components.tsx
// component=MenuVerticalItem
import figma from 'figma'

const instance = figma.selectedInstance
const prop_icon = instance.getSlot("icon")
const prop_pressed = instance.getEnum("pressed", {
  "off": "off",
  "on": "on"
})

export default {
  example: figma.code`<MenuVerticalItem ${prop_icon ? figma.code` icon={${prop_icon}}` : ''} pressed="${prop_pressed}" />`,
  imports: ['import { MenuVerticalItem } from "./src/generated/components"'],
  id: "yb-3582-29348",
  metadata: {
    nestable: false,
    props: {
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
