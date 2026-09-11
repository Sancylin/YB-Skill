// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=15287-4723
// source=src/generated/components.tsx
// component=InternalMDOl
import figma from 'figma'

const instance = figma.selectedInstance
const prop_level = instance.getEnum("level", {
  "1": "1",
  "2": "2",
  "3": "3"
})

export default {
  example: figma.code`<InternalMDOl level="${prop_level}" />`,
  imports: ['import { InternalMDOl } from "./src/generated/components"'],
  id: "yb-15287-4723",
  metadata: {
    nestable: true,
    props: {
  "level": {
    "figmaName": "level",
    "type": "VARIANT",
    "options": [
      "1",
      "2",
      "3"
    ]
  }
},
  },
}
