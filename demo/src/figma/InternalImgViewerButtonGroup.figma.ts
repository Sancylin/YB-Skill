// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=5414-20542
// source=src/generated/components.tsx
// component=InternalImgViewerButtonGroup
import figma from 'figma'

const instance = figma.selectedInstance
const prop_num = instance.getEnum("num", {
  "1": "1",
  "2": "2",
  "3": "3"
})

export default {
  example: figma.code`<InternalImgViewerButtonGroup num="${prop_num}" />`,
  imports: ['import { InternalImgViewerButtonGroup } from "./src/generated/components"'],
  id: "yb-5414-20542",
  metadata: {
    nestable: true,
    props: {
  "num": {
    "figmaName": "num",
    "type": "VARIANT",
    "options": [
      "1",
      "2",
      "3"
    ]
  }
},
  },
}
