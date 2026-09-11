// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=6229-10822
// source=src/generated/components.tsx
// component=Guide
import figma from 'figma'

const instance = figma.selectedInstance
const prop_direction = instance.getEnum("direction", {
  "up": "up",
  "bottom": "bottom"
})

export default {
  example: figma.code`<Guide direction="${prop_direction}" />`,
  imports: ['import { Guide } from "./src/generated/components"'],
  id: "yb-6229-10822",
  metadata: {
    nestable: false,
    props: {
  "direction": {
    "figmaName": "direction",
    "type": "VARIANT",
    "options": [
      "up",
      "bottom"
    ]
  }
},
  },
}
