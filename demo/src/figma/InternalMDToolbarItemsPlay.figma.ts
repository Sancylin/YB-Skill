// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=18333-21837
// source=src/generated/components.tsx
// component=InternalMDToolbarItemsPlay
import figma from 'figma'

const instance = figma.selectedInstance
const prop_status = instance.getEnum("status", {
  "play": "play",
  "playing": "playing",
  "paused": "paused"
})

export default {
  example: figma.code`<InternalMDToolbarItemsPlay status="${prop_status}" />`,
  imports: ['import { InternalMDToolbarItemsPlay } from "./src/generated/components"'],
  id: "yb-18333-21837",
  metadata: {
    nestable: true,
    props: {
  "status": {
    "figmaName": "status",
    "type": "VARIANT",
    "options": [
      "play",
      "playing",
      "paused"
    ]
  }
},
  },
}
