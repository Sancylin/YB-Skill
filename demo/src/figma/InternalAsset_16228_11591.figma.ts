// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=16228-11591
// source=src/generated/components.tsx
// component=InternalAsset_16228_11591
import figma from 'figma'

const instance = figma.selectedInstance
const prop_property1 = instance.getEnum("Property 1", {
  "Default": "Default",
  "error": "error",
  "loading": "loading",
  "refresh": "refresh"
})

export default {
  example: figma.code`<InternalAsset_16228_11591 property1="${prop_property1}" />`,
  imports: ['import { InternalAsset_16228_11591 } from "./src/generated/components"'],
  id: "yb-16228-11591",
  metadata: {
    nestable: true,
    props: {
  "property1": {
    "figmaName": "Property 1",
    "type": "VARIANT",
    "options": [
      "Default",
      "error",
      "loading",
      "refresh"
    ]
  }
},
  },
}
