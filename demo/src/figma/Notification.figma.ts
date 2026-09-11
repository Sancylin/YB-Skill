// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=6743-12139
// source=src/generated/components.tsx
// component=Notification
import figma from 'figma'

const instance = figma.selectedInstance
const prop_iconSlot = instance.getSlot("IconSlot")
const prop_button = instance.getBoolean("Button")
const prop_close = instance.getBoolean("Close")
const prop_subtitle = instance.getBoolean("Subtitle")
const prop_icon = instance.getBoolean("Icon")
const prop_entry = instance.getBoolean("Entry")
const prop_notification = instance.getEnum("Notification", {
  "pic": "pic",
  "icon": "icon"
})

export default {
  example: figma.code`<Notification ${prop_iconSlot ? figma.code` iconSlot={${prop_iconSlot}}` : ''} ${prop_button ? "button" : ''} ${prop_close ? "close" : ''} ${prop_subtitle ? "subtitle" : ''} ${prop_icon ? "icon" : ''} ${prop_entry ? "entry" : ''} notification="${prop_notification}" />`,
  imports: ['import { Notification } from "./src/generated/components"'],
  id: "yb-6743-12139",
  metadata: {
    nestable: false,
    props: {
  "iconSlot": {
    "figmaName": "IconSlot",
    "type": "SLOT",
    "options": []
  },
  "button": {
    "figmaName": "Button",
    "type": "BOOLEAN",
    "options": []
  },
  "close": {
    "figmaName": "Close",
    "type": "BOOLEAN",
    "options": []
  },
  "subtitle": {
    "figmaName": "Subtitle",
    "type": "BOOLEAN",
    "options": []
  },
  "icon": {
    "figmaName": "Icon",
    "type": "BOOLEAN",
    "options": []
  },
  "entry": {
    "figmaName": "Entry",
    "type": "BOOLEAN",
    "options": []
  },
  "notification": {
    "figmaName": "Notification",
    "type": "VARIANT",
    "options": [
      "pic",
      "icon"
    ]
  }
},
  },
}
