// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=15287-4201
// source=src/generated/components.tsx
// component=Markdown
import figma from 'figma'

const instance = figma.selectedInstance
const prop_olSlot = instance.getSlot("ol_slot")
const prop_ulSlot = instance.getSlot("ul_slot")
const prop_tableContent = instance.getSlot("table_content")
const prop_items = instance.getSlot("items")
const prop_quoteText = instance.getSlot("QuoteText")
const prop_body = instance.getSlot("body")
const prop_latex = instance.getSlot("latex")
const prop_promptAttachment = instance.getBoolean("promptAttachment")
const prop_variant = instance.getEnum("variant", {
  "prompt": "prompt",
  "Progress": "Progress",
  "H1": "H1",
  "H2": "H2",
  "Others+H2": "Others+H2",
  "H3": "H3",
  "Others+H3": "Others+H3",
  "H4": "H4",
  "Others+H4": "Others+H4",
  "Body": "Body",
  "OL": "OL",
  "UL": "UL",
  "Divider": "Divider",
  "Table": "Table",
  "Code": "Code",
  "File": "File",
  "Quote": "Quote",
  "InlineLaTex": "InlineLaTex",
  "WrappedInlineLaTex": "WrappedInlineLaTex",
  "DisplayLaTex": "DisplayLaTex",
  "sugForm": "sugForm",
  "Toolbar": "Toolbar",
  "followUp": "followUp",
  "video": "video",
  "IMG": "IMG",
  "ImgWidget": "ImgWidget",
  "miniProgram": "miniProgram",
  "AiEdu": "AiEdu",
  "recording": "recording"
})

export default {
  example: figma.code`<Markdown ${prop_olSlot ? figma.code` olSlot={${prop_olSlot}}` : ''} ${prop_ulSlot ? figma.code` ulSlot={${prop_ulSlot}}` : ''} ${prop_tableContent ? figma.code` tableContent={${prop_tableContent}}` : ''} ${prop_items ? figma.code` items={${prop_items}}` : ''} ${prop_quoteText ? figma.code` quoteText={${prop_quoteText}}` : ''} ${prop_body ? figma.code` body={${prop_body}}` : ''} ${prop_latex ? figma.code` latex={${prop_latex}}` : ''} ${prop_promptAttachment ? "promptAttachment" : ''} variant="${prop_variant}" />`,
  imports: ['import { Markdown } from "./src/generated/components"'],
  id: "yb-15287-4201",
  metadata: {
    nestable: false,
    props: {
  "olSlot": {
    "figmaName": "ol_slot",
    "type": "SLOT",
    "options": []
  },
  "ulSlot": {
    "figmaName": "ul_slot",
    "type": "SLOT",
    "options": []
  },
  "tableContent": {
    "figmaName": "table_content",
    "type": "SLOT",
    "options": []
  },
  "items": {
    "figmaName": "items",
    "type": "SLOT",
    "options": []
  },
  "quoteText": {
    "figmaName": "QuoteText",
    "type": "SLOT",
    "options": []
  },
  "body": {
    "figmaName": "body",
    "type": "SLOT",
    "options": []
  },
  "latex": {
    "figmaName": "latex",
    "type": "SLOT",
    "options": []
  },
  "promptAttachment": {
    "figmaName": "promptAttachment",
    "type": "BOOLEAN",
    "options": []
  },
  "variant": {
    "figmaName": "variant",
    "type": "VARIANT",
    "options": [
      "prompt",
      "Progress",
      "H1",
      "H2",
      "Others+H2",
      "H3",
      "Others+H3",
      "H4",
      "Others+H4",
      "Body",
      "OL",
      "UL",
      "Divider",
      "Table",
      "Code",
      "File",
      "Quote",
      "InlineLaTex",
      "WrappedInlineLaTex",
      "DisplayLaTex",
      "sugForm",
      "Toolbar",
      "followUp",
      "video",
      "IMG",
      "ImgWidget",
      "miniProgram",
      "AiEdu",
      "recording"
    ]
  }
},
  },
}
