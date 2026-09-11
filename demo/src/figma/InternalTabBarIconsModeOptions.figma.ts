// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=5544-3301
// source=src/generated/components.tsx
// component=InternalTabBarIconsModeOptions
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("Type", {
  "AskYuanbao": "AskYuanbao",
  "Pai": "Pai",
  "Discovery": "Discovery",
  "We": "We",
  "Last time": "Last time"
})
const prop_state = instance.getEnum("State", {
  "off": "off",
  "on": "on"
})

export default {
  example: figma.code`<InternalTabBarIconsModeOptions type="${prop_type}" state="${prop_state}" />`,
  imports: ['import { InternalTabBarIconsModeOptions } from "./src/generated/components"'],
  id: "yb-5544-3301",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "Type",
    "type": "VARIANT",
    "options": [
      "AskYuanbao",
      "Pai",
      "Discovery",
      "We",
      "Last time"
    ]
  },
  "state": {
    "figmaName": "State",
    "type": "VARIANT",
    "options": [
      "off",
      "on"
    ]
  }
},
  },
}
