// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=2850-9086
// source=src/generated/components.tsx
// component=InternalAsset_2850_9086
import figma from 'figma'

const instance = figma.selectedInstance
const prop_state = instance.getEnum("State", {
  "error": "error",
  "icon": "icon",
  "loading": "loading",
  "refresh": "refresh"
})

export default {
  example: figma.code`<InternalAsset_2850_9086 state="${prop_state}" />`,
  imports: ['import { InternalAsset_2850_9086 } from "./src/generated/components"'],
  id: "yb-2850-9086",
  metadata: {
    nestable: true,
    props: {
  "state": {
    "figmaName": "State",
    "type": "VARIANT",
    "options": [
      "error",
      "icon",
      "loading",
      "refresh"
    ]
  }
},
  },
}
