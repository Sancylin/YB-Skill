// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=8700-5777
// source=src/generated/components.tsx
// component=ImgViewer
import figma from 'figma'

const instance = figma.selectedInstance
const prop_type = instance.getEnum("type", {
  "searchImg": "searchImg",
  "createImg": "createImg"
})

export default {
  example: figma.code`<ImgViewer type="${prop_type}" />`,
  imports: ['import { ImgViewer } from "./src/generated/components"'],
  id: "yb-8700-5777",
  metadata: {
    nestable: false,
    props: {
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "searchImg",
      "createImg"
    ]
  }
},
  },
}
