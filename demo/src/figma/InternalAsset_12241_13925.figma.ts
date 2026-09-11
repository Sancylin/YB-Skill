// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=12241-13925
// source=src/generated/components.tsx
// component=InternalAsset_12241_13925
import figma from 'figma'

const instance = figma.selectedInstance
const prop_property1 = instance.getEnum("Property 1", {
  "loading": "loading",
  "error": "error",
  "reload": "reload"
})

export default {
  example: figma.code`<InternalAsset_12241_13925 property1="${prop_property1}" />`,
  imports: ['import { InternalAsset_12241_13925 } from "./src/generated/components"'],
  id: "yb-12241-13925",
  metadata: {
    nestable: true,
    props: {
  "property1": {
    "figmaName": "Property 1",
    "type": "VARIANT",
    "options": [
      "loading",
      "error",
      "reload"
    ]
  }
},
  },
}
