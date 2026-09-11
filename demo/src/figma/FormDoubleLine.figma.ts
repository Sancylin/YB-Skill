// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=8841-7399
// source=src/generated/components.tsx
// component=FormDoubleLine
import figma from 'figma'

const instance = figma.selectedInstance
const prop_active = instance.getBoolean("active")
const prop_propDelete = instance.getBoolean("delete")
const prop_cursor = instance.getSlot("Cursor")
const prop_scroll = instance.getBoolean("scroll")
const prop_input = instance.getEnum("input", {
  "off": "off",
  "on": "on"
})

export default {
  example: figma.code`<FormDoubleLine ${prop_active ? "active" : ''} ${prop_propDelete ? "propDelete" : ''} ${prop_cursor ? figma.code` cursor={${prop_cursor}}` : ''} ${prop_scroll ? "scroll" : ''} input="${prop_input}" />`,
  imports: ['import { FormDoubleLine } from "./src/generated/components"'],
  id: "yb-8841-7399",
  metadata: {
    nestable: false,
    props: {
  "active": {
    "figmaName": "active",
    "type": "BOOLEAN",
    "options": []
  },
  "propDelete": {
    "figmaName": "delete",
    "type": "BOOLEAN",
    "options": []
  },
  "cursor": {
    "figmaName": "Cursor",
    "type": "SLOT",
    "options": []
  },
  "scroll": {
    "figmaName": "scroll",
    "type": "BOOLEAN",
    "options": []
  },
  "input": {
    "figmaName": "input",
    "type": "VARIANT",
    "options": [
      "off",
      "on"
    ]
  }
},
  },
}
