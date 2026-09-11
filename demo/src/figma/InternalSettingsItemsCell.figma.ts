// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=8451-3541
// source=src/generated/components.tsx
// component=InternalSettingsItemsCell
import figma from 'figma'

const instance = figma.selectedInstance
const prop_items = instance.getEnum("items", {
  "Radio": "Radio",
  "items": "items",
  "swtich": "swtich"
})

export default {
  example: figma.code`<InternalSettingsItemsCell items="${prop_items}" />`,
  imports: ['import { InternalSettingsItemsCell } from "./src/generated/components"'],
  id: "yb-8451-3541",
  metadata: {
    nestable: true,
    props: {
  "items": {
    "figmaName": "items",
    "type": "VARIANT",
    "options": [
      "Radio",
      "items",
      "swtich"
    ]
  }
},
  },
}
