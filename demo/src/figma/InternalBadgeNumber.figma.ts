// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=337-237
// source=src/generated/components.tsx
// component=InternalBadgeNumber
import figma from 'figma'

const instance = figma.selectedInstance
const prop_scale = instance.getEnum("Scale", {
  "Default": "Default",
  "Level 01": "Level 01",
  "Level 03": "Level 03",
  "Level 04": "Level 04",
  "Level 05": "Level 05",
  "Level 06": "Level 06",
  "Level 07": "Level 07"
})

export default {
  example: figma.code`<InternalBadgeNumber scale="${prop_scale}" />`,
  imports: ['import { InternalBadgeNumber } from "./src/generated/components"'],
  id: "yb-337-237",
  metadata: {
    nestable: true,
    props: {
  "scale": {
    "figmaName": "Scale",
    "type": "VARIANT",
    "options": [
      "Default",
      "Level 01",
      "Level 03",
      "Level 04",
      "Level 05",
      "Level 06",
      "Level 07"
    ]
  }
},
  },
}
