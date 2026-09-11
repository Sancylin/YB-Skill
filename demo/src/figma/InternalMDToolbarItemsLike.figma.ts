// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=18333-21815
// source=src/generated/components.tsx
// component=InternalMDToolbarItemsLike
import figma from 'figma'

const instance = figma.selectedInstance
const prop_click = instance.getEnum("click", {
  "true": "true",
  "false": "false"
})

export default {
  example: figma.code`<InternalMDToolbarItemsLike click="${prop_click}" />`,
  imports: ['import { InternalMDToolbarItemsLike } from "./src/generated/components"'],
  id: "yb-18333-21815",
  metadata: {
    nestable: true,
    props: {
  "click": {
    "figmaName": "click",
    "type": "VARIANT",
    "options": [
      "true",
      "false"
    ]
  }
},
  },
}
