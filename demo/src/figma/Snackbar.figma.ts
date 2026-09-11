// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3499-4058
// source=src/generated/components.tsx
// component=Snackbar
import figma from 'figma'

const instance = figma.selectedInstance
const prop_actionButton = instance.getBoolean("ActionButton")
const prop_icon = instance.getBoolean("Icon")

export default {
  example: figma.code`<Snackbar ${prop_actionButton ? "actionButton" : ''} ${prop_icon ? "icon" : ''} />`,
  imports: ['import { Snackbar } from "./src/generated/components"'],
  id: "yb-3499-4058",
  metadata: {
    nestable: false,
    props: {
  "actionButton": {
    "figmaName": "ActionButton",
    "type": "BOOLEAN",
    "options": []
  },
  "icon": {
    "figmaName": "Icon",
    "type": "BOOLEAN",
    "options": []
  }
},
  },
}
