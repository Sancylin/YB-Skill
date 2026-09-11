// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3149-22513
// source=src/generated/components.tsx
// component=InternalNavbar
import figma from 'figma'

const instance = figma.selectedInstance
const prop_leftIcon = instance.getBoolean("leftIcon")
const prop_rightIcon = instance.getBoolean("rightIcon")
const prop_description = instance.getBoolean("description")
const prop_divider = instance.getBoolean("divider")
const prop_content = instance.getBoolean("content")
const prop_leftSlot = instance.getSlot("leftSlot")
const prop_rightSlot = instance.getSlot("rightSlot")
const prop_type = instance.getEnum("type", {
  "default": "default",
  "tabCard": "tabCard"
})
const prop_position = instance.getEnum("position", {
  "left": "left",
  "middle": "middle"
})

export default {
  example: figma.code`<InternalNavbar ${prop_leftIcon ? "leftIcon" : ''} ${prop_rightIcon ? "rightIcon" : ''} ${prop_description ? "description" : ''} ${prop_divider ? "divider" : ''} ${prop_content ? "content" : ''} ${prop_leftSlot ? figma.code` leftSlot={${prop_leftSlot}}` : ''} ${prop_rightSlot ? figma.code` rightSlot={${prop_rightSlot}}` : ''} type="${prop_type}" position="${prop_position}" />`,
  imports: ['import { InternalNavbar } from "./src/generated/components"'],
  id: "yb-3149-22513",
  metadata: {
    nestable: true,
    props: {
  "leftIcon": {
    "figmaName": "leftIcon",
    "type": "BOOLEAN",
    "options": []
  },
  "rightIcon": {
    "figmaName": "rightIcon",
    "type": "BOOLEAN",
    "options": []
  },
  "description": {
    "figmaName": "description",
    "type": "BOOLEAN",
    "options": []
  },
  "divider": {
    "figmaName": "divider",
    "type": "BOOLEAN",
    "options": []
  },
  "content": {
    "figmaName": "content",
    "type": "BOOLEAN",
    "options": []
  },
  "leftSlot": {
    "figmaName": "leftSlot",
    "type": "SLOT",
    "options": []
  },
  "rightSlot": {
    "figmaName": "rightSlot",
    "type": "SLOT",
    "options": []
  },
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "default",
      "tabCard"
    ]
  },
  "position": {
    "figmaName": "position",
    "type": "VARIANT",
    "options": [
      "left",
      "middle"
    ]
  }
},
  },
}
