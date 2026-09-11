// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=4139-19690
// source=src/generated/components.tsx
// component=SettingsItems
import figma from 'figma'

const instance = figma.selectedInstance
const prop_state = instance.getEnum("state", {
  "primary": "primary",
  "secondary": "secondary",
  "withsubtitle": "withsubtitle"
})

export default {
  example: figma.code`<SettingsItems state="${prop_state}" />`,
  imports: ['import { SettingsItems } from "./src/generated/components"'],
  id: "yb-4139-19690",
  metadata: {
    nestable: false,
    props: {
  "state": {
    "figmaName": "state",
    "type": "VARIANT",
    "options": [
      "primary",
      "secondary",
      "withsubtitle"
    ]
  }
},
  },
}
