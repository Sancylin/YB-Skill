// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=4822-7543
// source=src/generated/components.tsx
// component=FileItems
import figma from 'figma'

const instance = figma.selectedInstance
const prop_showTime = instance.getBoolean("Show time")
const prop_des = instance.getSlot("des")
const prop_icon = instance.getSlot("Icon")
const prop_icon2 = instance.getEnum("icon", {
  "left": "left",
  "right": "right"
})

export default {
  example: figma.code`<FileItems ${prop_showTime ? "showTime" : ''} ${prop_des ? figma.code` des={${prop_des}}` : ''} ${prop_icon ? figma.code` icon={${prop_icon}}` : ''} icon2="${prop_icon2}" />`,
  imports: ['import { FileItems } from "./src/generated/components"'],
  id: "yb-4822-7543",
  metadata: {
    nestable: false,
    props: {
  "showTime": {
    "figmaName": "Show time",
    "type": "BOOLEAN",
    "options": []
  },
  "des": {
    "figmaName": "des",
    "type": "SLOT",
    "options": []
  },
  "icon": {
    "figmaName": "Icon",
    "type": "SLOT",
    "options": []
  },
  "icon2": {
    "figmaName": "icon",
    "type": "VARIANT",
    "options": [
      "left",
      "right"
    ]
  }
},
  },
}
