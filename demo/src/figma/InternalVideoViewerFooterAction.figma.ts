// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=6583-3503
// source=src/generated/components.tsx
// component=InternalVideoViewerFooterAction
import figma from 'figma'

const instance = figma.selectedInstance
const prop_buttonGroup = instance.getBoolean("buttonGroup")

export default {
  example: figma.code`<InternalVideoViewerFooterAction ${prop_buttonGroup ? "buttonGroup" : ''} />`,
  imports: ['import { InternalVideoViewerFooterAction } from "./src/generated/components"'],
  id: "yb-6583-3503",
  metadata: {
    nestable: true,
    props: {
  "buttonGroup": {
    "figmaName": "buttonGroup",
    "type": "BOOLEAN",
    "options": []
  }
},
  },
}
