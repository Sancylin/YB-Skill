// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=559-4217
// source=src/generated/components.tsx
// component=RadioCheckBox
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "circled": "circled",
  "plain": "plain"
})
const prop_state = instance.getEnum("state", {
  "unchecked": "unchecked",
  "checked": "checked",
  "disabled": "disabled",
  "checkedDisabled": "checkedDisabled"
})
const prop_size = instance.getEnum("size", {
  "lg": "lg",
  "sm": "sm"
})

export default {
  example: figma.code`<RadioCheckBox type="${prop_type}" state="${prop_state}" size="${prop_size}" />`,
  imports: ['import { RadioCheckBox } from "./src/generated/components"'],
  id: "yb-559-4217",
  metadata: {
    nestable: false,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "circled",
      "plain"
    ]
  },
  "state": {
    "figmaName": "state",
    "type": "VARIANT",
    "options": [
      "unchecked",
      "checked",
      "disabled",
      "checkedDisabled"
    ]
  },
  "size": {
    "figmaName": "size",
    "type": "VARIANT",
    "options": [
      "lg",
      "sm"
    ]
  }
},
  },
}
