// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3149-24851
// source=src/generated/components.tsx
// component=InternalIndicator
import figma from 'figma'

const instance = figma.selectedInstance
const prop_focus = instance.getEnum("focus", {
  "1": "1",
  "2": "2",
  "3": "3",
  "4": "4"
})

export default {
  example: figma.code`<InternalIndicator focus="${prop_focus}" />`,
  imports: ['import { InternalIndicator } from "./src/generated/components"'],
  id: "yb-3149-24851",
  metadata: {
    nestable: true,
    props: {
  "focus": {
    "figmaName": "focus",
    "type": "VARIANT",
    "options": [
      "1",
      "2",
      "3",
      "4"
    ]
  }
},
  },
}
