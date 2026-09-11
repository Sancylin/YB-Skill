// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=2850-35131
// source=src/generated/components.tsx
// component=Card
import figma from 'figma'

const instance = figma.selectedInstance
const prop_content = instance.getSlot("内容")
const prop_leftSlot = instance.getSlot("Left Slot")
const prop_close = instance.getBoolean("Close")
const prop_card = instance.getEnum("Card", {
  "File": "File",
  "Output": "Output"
})
const prop_pressed = instance.getEnum("Pressed", {
  "on": "on",
  "off": "off"
})

export default {
  example: figma.code`<Card ${prop_content ? figma.code` content={${prop_content}}` : ''} ${prop_leftSlot ? figma.code` leftSlot={${prop_leftSlot}}` : ''} ${prop_close ? "close" : ''} card="${prop_card}" pressed="${prop_pressed}" />`,
  imports: ['import { Card } from "./src/generated/components"'],
  id: "yb-2850-35131",
  metadata: {
    nestable: false,
    props: {
  "content": {
    "figmaName": "内容",
    "type": "SLOT",
    "options": []
  },
  "leftSlot": {
    "figmaName": "Left Slot",
    "type": "SLOT",
    "options": []
  },
  "close": {
    "figmaName": "Close",
    "type": "BOOLEAN",
    "options": []
  },
  "card": {
    "figmaName": "Card",
    "type": "VARIANT",
    "options": [
      "File",
      "Output"
    ]
  },
  "pressed": {
    "figmaName": "Pressed",
    "type": "VARIANT",
    "options": [
      "on",
      "off"
    ]
  }
},
  },
}
