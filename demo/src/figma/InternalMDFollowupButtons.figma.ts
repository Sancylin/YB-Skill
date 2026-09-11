// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=15287-4858
// source=src/generated/components.tsx
// component=InternalMDFollowupButtons
import figma from 'figma'

const instance = figma.selectedInstance
const prop_property1 = instance.getEnum("Property 1", {
  "longText": "longText",
  "multi2": "multi2",
  "multi3": "multi3",
  "single": "single"
})

export default {
  example: figma.code`<InternalMDFollowupButtons property1="${prop_property1}" />`,
  imports: ['import { InternalMDFollowupButtons } from "./src/generated/components"'],
  id: "yb-15287-4858",
  metadata: {
    nestable: true,
    props: {
  "property1": {
    "figmaName": "Property 1",
    "type": "VARIANT",
    "options": [
      "longText",
      "multi2",
      "multi3",
      "single"
    ]
  }
},
  },
}
