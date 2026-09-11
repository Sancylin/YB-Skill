// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3412-84459
// source=src/generated/components.tsx
// component=Search
import figma from 'figma'

const instance = figma.selectedInstance
const prop_paiName = instance.getBoolean("paiName")
const prop_status = instance.getEnum("status", {
  "default": "default",
  "focus": "focus",
  "inputted": "inputted"
})

export default {
  example: figma.code`<Search ${prop_paiName ? "paiName" : ''} status="${prop_status}" />`,
  imports: ['import { Search } from "./src/generated/components"'],
  id: "yb-3412-84459",
  metadata: {
    nestable: false,
    props: {
  "paiName": {
    "figmaName": "paiName",
    "type": "BOOLEAN",
    "options": []
  },
  "status": {
    "figmaName": "status",
    "type": "VARIANT",
    "options": [
      "default",
      "focus",
      "inputted"
    ]
  }
},
  },
}
