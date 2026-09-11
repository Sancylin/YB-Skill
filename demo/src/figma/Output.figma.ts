// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=8326-17561
// source=src/generated/components.tsx
// component=Output
import figma from 'figma'

const instance = figma.selectedInstance
const prop_property1 = instance.getEnum("Property 1", {
  "loading-moving": "loading-moving",
  "loading-silence": "loading-silence"
})

export default {
  example: figma.code`<Output property1="${prop_property1}" />`,
  imports: ['import { Output } from "./src/generated/components"'],
  id: "yb-8326-17561",
  metadata: {
    nestable: false,
    props: {
  "property1": {
    "figmaName": "Property 1",
    "type": "VARIANT",
    "options": [
      "loading-moving",
      "loading-silence"
    ]
  }
},
  },
}
