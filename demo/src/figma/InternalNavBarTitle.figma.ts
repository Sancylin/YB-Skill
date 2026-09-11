// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=2592-2871
// source=src/generated/components.tsx
// component=InternalNavBarTitle
import figma from 'figma'

const instance = figma.selectedInstance
const prop_dualTitle = instance.getEnum("Dual Title", {
  "True": "True",
  "False": "False"
})

export default {
  example: figma.code`<InternalNavBarTitle dualTitle="${prop_dualTitle}" />`,
  imports: ['import { InternalNavBarTitle } from "./src/generated/components"'],
  id: "yb-2592-2871",
  metadata: {
    nestable: true,
    props: {
  "dualTitle": {
    "figmaName": "Dual Title",
    "type": "VARIANT",
    "options": [
      "True",
      "False"
    ]
  }
},
  },
}
