// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=18333-21907
// source=src/generated/components.tsx
// component=InternalMDToolbar
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "Default": "Default",
  "recreate": "recreate",
  "playing": "playing"
})

export default {
  example: figma.code`<InternalMDToolbar type="${prop_type}" />`,
  imports: ['import { InternalMDToolbar } from "./src/generated/components"'],
  id: "yb-18333-21907",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "Default",
      "recreate",
      "playing"
    ]
  }
},
  },
}
