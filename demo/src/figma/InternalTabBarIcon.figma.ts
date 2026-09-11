// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=119-9587
// source=src/generated/components.tsx
// component=InternalTabBarIcon
import figma from 'figma'

const instance = figma.selectedInstance
const prop_badge = instance.getBoolean("Badge")
const prop_redDot = instance.getBoolean("RedDot")

export default {
  example: figma.code`<InternalTabBarIcon ${prop_badge ? "badge" : ''} ${prop_redDot ? "redDot" : ''} />`,
  imports: ['import { InternalTabBarIcon } from "./src/generated/components"'],
  id: "yb-119-9587",
  metadata: {
    nestable: true,
    props: {
  "badge": {
    "figmaName": "Badge",
    "type": "BOOLEAN",
    "options": []
  },
  "redDot": {
    "figmaName": "RedDot",
    "type": "BOOLEAN",
    "options": []
  }
},
  },
}
