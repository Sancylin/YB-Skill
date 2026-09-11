// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=5170-6519
// source=src/generated/components.tsx
// component=Status
import figma from 'figma'

const instance = figma.selectedInstance
const prop_property1 = instance.getEnum("Property 1", {
  "error": "error",
  "loading": "loading",
  "refresh": "refresh",
  "Variant6": "Variant6",
  "Variant5": "Variant5",
  "Variant7": "Variant7",
  "icon": "icon",
  "Variant8": "Variant8"
})

export default {
  example: figma.code`<Status property1="${prop_property1}" />`,
  imports: ['import { Status } from "./src/generated/components"'],
  id: "yb-5170-6519",
  metadata: {
    nestable: false,
    props: {
  "property1": {
    "figmaName": "Property 1",
    "type": "VARIANT",
    "options": [
      "error",
      "loading",
      "refresh",
      "Variant6",
      "Variant5",
      "Variant7",
      "icon",
      "Variant8"
    ]
  }
},
  },
}
