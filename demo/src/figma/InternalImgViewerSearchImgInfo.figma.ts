// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=5414-20212
// source=src/generated/components.tsx
// component=InternalImgViewerSearchImgInfo
import figma from 'figma'

const instance = figma.selectedInstance
const prop_ecommerce = instance.getBoolean("Ecommerce")
const prop_comment = instance.getBoolean("comment")

export default {
  example: figma.code`<InternalImgViewerSearchImgInfo ${prop_ecommerce ? "ecommerce" : ''} ${prop_comment ? "comment" : ''} />`,
  imports: ['import { InternalImgViewerSearchImgInfo } from "./src/generated/components"'],
  id: "yb-5414-20212",
  metadata: {
    nestable: true,
    props: {
  "ecommerce": {
    "figmaName": "Ecommerce",
    "type": "BOOLEAN",
    "options": []
  },
  "comment": {
    "figmaName": "comment",
    "type": "BOOLEAN",
    "options": []
  }
},
  },
}
