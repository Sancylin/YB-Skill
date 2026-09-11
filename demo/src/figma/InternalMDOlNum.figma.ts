// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=15287-4718
// source=src/generated/components.tsx
// component=InternalMDOlNum
import figma from 'figma'

const instance = figma.selectedInstance
const prop_variant = instance.getEnum("variant", {
  "0-9": "0-9",
  "10+": "10+"
})

export default {
  example: figma.code`<InternalMDOlNum variant="${prop_variant}" />`,
  imports: ['import { InternalMDOlNum } from "./src/generated/components"'],
  id: "yb-15287-4718",
  metadata: {
    nestable: true,
    props: {
  "variant": {
    "figmaName": "variant",
    "type": "VARIANT",
    "options": [
      "0-9",
      "10+"
    ]
  }
},
  },
}
