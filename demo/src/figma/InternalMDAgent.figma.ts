// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=19073-63353
// source=src/generated/components.tsx
// component=InternalMDAgent
import figma from 'figma'

const instance = figma.selectedInstance
const prop_image = instance.getSlot("image")
const prop_property1 = instance.getEnum("Property 1", {
  "search": "search",
  "skill": "skill",
  "bash": "bash",
  "write": "write",
  "edit": "edit",
  "读取": "读取",
  "fetch": "fetch",
  "搜图": "搜图",
  "类型13": "类型13",
  "ocr": "ocr",
  "任务": "任务",
  "视频": "视频",
  "澄清": "澄清"
})

export default {
  example: figma.code`<InternalMDAgent ${prop_image ? figma.code` image={${prop_image}}` : ''} property1="${prop_property1}" />`,
  imports: ['import { InternalMDAgent } from "./src/generated/components"'],
  id: "yb-19073-63353",
  metadata: {
    nestable: true,
    props: {
  "image": {
    "figmaName": "image",
    "type": "SLOT",
    "options": []
  },
  "property1": {
    "figmaName": "Property 1",
    "type": "VARIANT",
    "options": [
      "search",
      "skill",
      "bash",
      "write",
      "edit",
      "读取",
      "fetch",
      "搜图",
      "类型13",
      "ocr",
      "任务",
      "视频",
      "澄清"
    ]
  }
},
  },
}
