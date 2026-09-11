// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=77-272
// source=src/generated/components.tsx
// component=Divider
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "default": "default",
  "PAI": "PAI",
  "withLabel": "withLabel"
})
const prop_direction = instance.getEnum("direction", {
  "horizontal": "horizontal",
  "vertical": "vertical"
})

export default {
  example: figma.code`<Divider type="${prop_type}" direction="${prop_direction}" />`,
  imports: ['import { Divider } from "./src/generated/components"'],
  id: "yb-77-272",
  metadata: {
    nestable: false,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "default",
      "PAI",
      "withLabel"
    ]
  },
  "direction": {
    "figmaName": "direction",
    "type": "VARIANT",
    "options": [
      "horizontal",
      "vertical"
    ]
  }
},
  },
}
