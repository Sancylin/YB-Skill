// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=15287-4740
// source=src/generated/components.tsx
// component=InternalMDProgress
import figma from 'figma'

const instance = figma.selectedInstance
const prop_status = instance.getEnum("status", {
  "clarify": "clarify",
  "done": "done",
  "loading": "loading"
})

export default {
  example: figma.code`<InternalMDProgress status="${prop_status}" />`,
  imports: ['import { InternalMDProgress } from "./src/generated/components"'],
  id: "yb-15287-4740",
  metadata: {
    nestable: true,
    props: {
  "status": {
    "figmaName": "status",
    "type": "VARIANT",
    "options": [
      "clarify",
      "done",
      "loading"
    ]
  }
},
  },
}
