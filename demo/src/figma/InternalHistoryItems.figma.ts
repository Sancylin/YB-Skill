// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3438-109094
// source=src/generated/components.tsx
// component=InternalHistoryItems
import figma from 'figma'

const instance = figma.selectedInstance
const prop_clear = instance.getBoolean("clear")
const prop_result = instance.getEnum("result", {
  "true": "true",
  "false": "false"
})

export default {
  example: figma.code`<InternalHistoryItems ${prop_clear ? "clear" : ''} result="${prop_result}" />`,
  imports: ['import { InternalHistoryItems } from "./src/generated/components"'],
  id: "yb-3438-109094",
  metadata: {
    nestable: true,
    props: {
  "clear": {
    "figmaName": "clear",
    "type": "BOOLEAN",
    "options": []
  },
  "result": {
    "figmaName": "result",
    "type": "VARIANT",
    "options": [
      "true",
      "false"
    ]
  }
},
  },
}
