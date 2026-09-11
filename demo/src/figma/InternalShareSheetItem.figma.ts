// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3436-37680
// source=src/generated/components.tsx
// component=InternalShareSheetItem
import figma from 'figma'

const instance = figma.selectedInstance
const prop_iconSlot = instance.getSlot("Icon Slot")

export default {
  example: figma.code`<InternalShareSheetItem ${prop_iconSlot ? figma.code` iconSlot={${prop_iconSlot}}` : ''} />`,
  imports: ['import { InternalShareSheetItem } from "./src/generated/components"'],
  id: "yb-3436-37680",
  metadata: {
    nestable: true,
    props: {
  "iconSlot": {
    "figmaName": "Icon Slot",
    "type": "SLOT",
    "options": []
  }
},
  },
}
