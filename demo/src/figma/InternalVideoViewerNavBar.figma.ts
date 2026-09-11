// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=6583-1681
// source=src/generated/components.tsx
// component=InternalVideoViewerNavBar
import figma from 'figma'

const instance = figma.selectedInstance
const prop_indicator = instance.getBoolean("indicator")
const prop_type = instance.getEnum("type", {
  "createVideo": "createVideo",
  "sendVideo": "sendVideo"
})

export default {
  example: figma.code`<InternalVideoViewerNavBar ${prop_indicator ? "indicator" : ''} type="${prop_type}" />`,
  imports: ['import { InternalVideoViewerNavBar } from "./src/generated/components"'],
  id: "yb-6583-1681",
  metadata: {
    nestable: true,
    props: {
  "indicator": {
    "figmaName": "indicator",
    "type": "BOOLEAN",
    "options": []
  },
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "createVideo",
      "sendVideo"
    ]
  }
},
  },
}
