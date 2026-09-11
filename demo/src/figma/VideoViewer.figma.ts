// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=8720-3833
// source=src/generated/components.tsx
// component=VideoViewer
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "sendVideo": "sendVideo",
  "createVideo": "createVideo"
})

export default {
  example: figma.code`<VideoViewer type="${prop_type}" />`,
  imports: ['import { VideoViewer } from "./src/generated/components"'],
  id: "yb-8720-3833",
  metadata: {
    nestable: false,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "sendVideo",
      "createVideo"
    ]
  }
},
  },
}
