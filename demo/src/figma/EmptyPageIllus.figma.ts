// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=6094-16751
// source=src/generated/components.tsx
// component=EmptyPageIllus
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "networkError": "networkError",
  "noContent": "noContent",
  "placeholder": "placeholder"
})

export default {
  example: figma.code`<EmptyPageIllus type="${prop_type}" />`,
  imports: ['import { EmptyPageIllus } from "./src/generated/components"'],
  id: "yb-6094-16751",
  metadata: {
    nestable: false,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "networkError",
      "noContent",
      "placeholder"
    ]
  }
},
  },
}
