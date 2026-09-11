// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3582-29365
// source=src/generated/components.tsx
// component=MenuDivider
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "horiThin": "horiThin",
  "vertical": "vertical",
  "horiBold": "horiBold"
})

export default {
  example: figma.code`<MenuDivider type="${prop_type}" />`,
  imports: ['import { MenuDivider } from "./src/generated/components"'],
  id: "yb-3582-29365",
  metadata: {
    nestable: false,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "horiThin",
      "vertical",
      "horiBold"
    ]
  }
},
  },
}
