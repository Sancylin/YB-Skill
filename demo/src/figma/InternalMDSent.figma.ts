// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=18455-29747
// source=src/generated/components.tsx
// component=InternalMDSent
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "file": "file",
  "image": "image",
  "wechat": "wechat",
  "公众号": "公众号"
})

export default {
  example: figma.code`<InternalMDSent type="${prop_type}" />`,
  imports: ['import { InternalMDSent } from "./src/generated/components"'],
  id: "yb-18455-29747",
  metadata: {
    nestable: true,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "file",
      "image",
      "wechat",
      "公众号"
    ]
  }
},
  },
}
