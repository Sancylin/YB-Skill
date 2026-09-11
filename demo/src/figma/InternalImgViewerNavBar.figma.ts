// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=5414-13741
// source=src/generated/components.tsx
// component=InternalImgViewerNavBar
import figma from 'figma'

const instance = figma.selectedInstance
const prop_indicator = instance.getBoolean("indicator")
const prop_type = instance.getEnum("type", {
  "createImg": "createImg",
  "sendImg": "sendImg",
  "searchImg": "searchImg"
})

export default {
  example: figma.code`<InternalImgViewerNavBar ${prop_indicator ? "indicator" : ''} type="${prop_type}" />`,
  imports: ['import { InternalImgViewerNavBar } from "./src/generated/components"'],
  id: "yb-5414-13741",
  metadata: {
    nestable: true,
    props: {
  "indicator": {
    "figmaName": "indicator",
    "type": "BOOLEAN",
    "options": []
  },
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "createImg",
      "sendImg",
      "searchImg"
    ]
  }
},
  },
}
