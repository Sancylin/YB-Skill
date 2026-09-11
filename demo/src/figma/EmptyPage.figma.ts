// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=4928-8762
// source=src/generated/components.tsx
// component=EmptyPage
import figma from 'figma'

const instance = figma.selectedInstance
const prop_description = instance.getBoolean("description")
const prop_button = instance.getBoolean("button")

export default {
  example: figma.code`<EmptyPage ${prop_description ? "description" : ''} ${prop_button ? "button" : ''} />`,
  imports: ['import { EmptyPage } from "./src/generated/components"'],
  id: "yb-4928-8762",
  metadata: {
    nestable: false,
    props: {
  "description": {
    "figmaName": "description",
    "type": "BOOLEAN",
    "options": []
  },
  "button": {
    "figmaName": "button",
    "type": "BOOLEAN",
    "options": []
  }
},
  },
}
