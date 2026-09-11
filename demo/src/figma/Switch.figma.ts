// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=1436-10
// source=src/generated/components.tsx
// component=Switch
import figma from 'figma'

const instance = figma.selectedInstance
const prop_turnOn = instance.getEnum("turnOn", {
  "true": "true",
  "false": "false"
})
const prop_disabled = instance.getEnum("disabled", {
  "false": "false",
  "true": "true"
})

export default {
  example: figma.code`<Switch turnOn="${prop_turnOn}" disabled="${prop_disabled}" />`,
  imports: ['import { Switch } from "./src/generated/components"'],
  id: "yb-1436-10",
  metadata: {
    nestable: false,
    props: {
  "turnOn": {
    "figmaName": "turnOn",
    "type": "VARIANT",
    "options": [
      "true",
      "false"
    ]
  },
  "disabled": {
    "figmaName": "disabled",
    "type": "VARIANT",
    "options": [
      "false",
      "true"
    ]
  }
},
  },
}
