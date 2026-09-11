// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=82-944
// source=src/generated/components.tsx
// component=InternalStatusBar
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("Type", {
  "iPhone": "iPhone",
  "iPad": "iPad"
})

export default {
  example: figma.code`<InternalStatusBar type="${prop_type}" />`,
  imports: ['import { InternalStatusBar } from "./src/generated/components"'],
  id: "yb-82-944",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "Type",
    "type": "VARIANT",
    "options": [
      "iPhone",
      "iPad"
    ]
  }
},
  },
}
