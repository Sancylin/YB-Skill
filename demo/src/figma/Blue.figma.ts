// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=8262-6063
// source=src/generated/components.tsx
// component=Blue
import figma from 'figma'

const instance = figma.selectedInstance
const prop_property1 = instance.getEnum("Property 1", {
  "1": "1",
  "2": "2"
})

export default {
  example: figma.code`<Blue property1="${prop_property1}" />`,
  imports: ['import { Blue } from "./src/generated/components"'],
  id: "yb-8262-6063",
  metadata: {
    nestable: false,
    props: {
  "property1": {
    "figmaName": "Property 1",
    "type": "VARIANT",
    "options": [
      "1",
      "2"
    ]
  }
},
  },
}
