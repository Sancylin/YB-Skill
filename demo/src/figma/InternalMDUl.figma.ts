// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=15287-4730
// source=src/generated/components.tsx
// component=InternalMDUl
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "solid": "solid"
})
const prop_level = instance.getEnum("level", {
  "1": "1",
  "2": "2",
  "3": "3"
})

export default {
  example: figma.code`<InternalMDUl type="${prop_type}" level="${prop_level}" />`,
  imports: ['import { InternalMDUl } from "./src/generated/components"'],
  id: "yb-15287-4730",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "solid"
    ]
  },
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
