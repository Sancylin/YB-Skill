// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3995-29183
// source=src/generated/components.tsx
// component=ShareSheet
import figma from 'figma'

const instance = figma.selectedInstance
const prop_shareSheet = instance.getEnum("ShareSheet", {
  "Dialogue Share": "Dialogue Share",
  "File Share": "File Share"
})

export default {
  example: figma.code`<ShareSheet shareSheet="${prop_shareSheet}" />`,
  imports: ['import { ShareSheet } from "./src/generated/components"'],
  id: "yb-3995-29183",
  metadata: {
    nestable: false,
    props: {
  "shareSheet": {
    "figmaName": "ShareSheet",
    "type": "VARIANT",
    "options": [
      "Dialogue Share",
      "File Share"
    ]
  }
},
  },
}
