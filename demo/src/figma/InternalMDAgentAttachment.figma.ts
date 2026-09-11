// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=19064-29059
// source=src/generated/components.tsx
// component=InternalMDAgentAttachment
import figma from 'figma'

const instance = figma.selectedInstance
const prop_slot = instance.getSlot("Slot")
const prop_slot2 = instance.getSlot("Slot 2")
const prop_slot3 = instance.getSlot("Slot 3")
const prop_slot4 = instance.getSlot("Slot 4")
const prop_slot5 = instance.getSlot("Slot 5")
const prop_attachmentType = instance.getEnum("附件类型", {
  "fetch": "fetch",
  "search": "search",
  "file": "file",
  "img": "img",
  "video": "video"
})

export default {
  example: figma.code`<InternalMDAgentAttachment ${prop_slot ? figma.code` slot={${prop_slot}}` : ''} ${prop_slot2 ? figma.code` slot2={${prop_slot2}}` : ''} ${prop_slot3 ? figma.code` slot3={${prop_slot3}}` : ''} ${prop_slot4 ? figma.code` slot4={${prop_slot4}}` : ''} ${prop_slot5 ? figma.code` slot5={${prop_slot5}}` : ''} attachmentType="${prop_attachmentType}" />`,
  imports: ['import { InternalMDAgentAttachment } from "./src/generated/components"'],
  id: "yb-19064-29059",
  metadata: {
    nestable: true,
    props: {
  "slot": {
    "figmaName": "Slot",
    "type": "SLOT",
    "options": []
  },
  "slot2": {
    "figmaName": "Slot 2",
    "type": "SLOT",
    "options": []
  },
  "slot3": {
    "figmaName": "Slot 3",
    "type": "SLOT",
    "options": []
  },
  "slot4": {
    "figmaName": "Slot 4",
    "type": "SLOT",
    "options": []
  },
  "slot5": {
    "figmaName": "Slot 5",
    "type": "SLOT",
    "options": []
  },
  "attachmentType": {
    "figmaName": "附件类型",
    "type": "VARIANT",
    "options": [
      "fetch",
      "search",
      "file",
      "img",
      "video"
    ]
  }
},
  },
}
