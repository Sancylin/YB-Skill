// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=10785-4054
// source=src/generated/components.tsx
// component=InternalBrowserToolbarIcon
import figma from 'figma'

const instance = figma.selectedInstance
const prop_direction = instance.getEnum("Direction", {
  "Left": "Left",
  "Right": "Right"
})
const prop_disable = instance.getEnum("Disable", {
  "True": "True",
  "False": "False"
})

export default {
  example: figma.code`<InternalBrowserToolbarIcon direction="${prop_direction}" disable="${prop_disable}" />`,
  imports: ['import { InternalBrowserToolbarIcon } from "./src/generated/components"'],
  id: "yb-10785-4054",
  metadata: {
    nestable: true,
    props: {
  "direction": {
    "figmaName": "Direction",
    "type": "VARIANT",
    "options": [
      "Left",
      "Right"
    ]
  },
  "disable": {
    "figmaName": "Disable",
    "type": "VARIANT",
    "options": [
      "True",
      "False"
    ]
  }
},
  },
}
