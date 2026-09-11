// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=8700-5804
// source=src/generated/components.tsx
// component=InternalVideoViewerFooterActionIndicator
import figma from 'figma'

const instance = figma.selectedInstance
const prop_status = instance.getEnum("status", {
  "pause": "pause",
  "play": "play",
  "drag": "drag"
})

export default {
  example: figma.code`<InternalVideoViewerFooterActionIndicator status="${prop_status}" />`,
  imports: ['import { InternalVideoViewerFooterActionIndicator } from "./src/generated/components"'],
  id: "yb-8700-5804",
  metadata: {
    nestable: true,
    props: {
  "status": {
    "figmaName": "status",
    "type": "VARIANT",
    "options": [
      "pause",
      "play",
      "drag"
    ]
  }
},
  },
}
