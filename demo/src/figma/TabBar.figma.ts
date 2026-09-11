// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=119-10030
// source=src/generated/components.tsx
// component=TabBar
import figma from 'figma'

const instance = figma.selectedInstance
const prop_selected = instance.getEnum("Selected", {
  "Tab 1 & Input": "Tab 1 & Input",
  "Tab 1": "Tab 1",
  "Tab 2": "Tab 2",
  "Tab 3": "Tab 3",
  "Tab 4": "Tab 4"
})

export default {
  example: figma.code`<TabBar selected="${prop_selected}" />`,
  imports: ['import { TabBar } from "./src/generated/components"'],
  id: "yb-119-10030",
  metadata: {
    nestable: false,
    props: {
  "selected": {
    "figmaName": "Selected",
    "type": "VARIANT",
    "options": [
      "Tab 1 & Input",
      "Tab 1",
      "Tab 2",
      "Tab 3",
      "Tab 4"
    ]
  }
},
  },
}
