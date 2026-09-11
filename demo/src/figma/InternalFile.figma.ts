// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=2850-10220
// source=src/generated/components.tsx
// component=InternalFile
import figma from 'figma'

const instance = figma.selectedInstance
const prop_file = instance.getEnum("File", {
  "Audio": "Audio",
  "Code": "Code",
  "Excel": "Excel",
  "Link": "Link",
  "PDF": "PDF",
  "PPT": "PPT",
  "Picture": "Picture",
  "Text": "Text",
  "Unknow": "Unknow",
  "Video": "Video",
  "Word": "Word",
  "zip": "zip",
  "markdown": "markdown"
})
const prop_mode = instance.getEnum("Mode", {
  "Dark": "Dark",
  "Light": "Light"
})

export default {
  example: figma.code`<InternalFile file="${prop_file}" mode="${prop_mode}" />`,
  imports: ['import { InternalFile } from "./src/generated/components"'],
  id: "yb-2850-10220",
  metadata: {
    nestable: true,
    props: {
  "file": {
    "figmaName": "File",
    "type": "VARIANT",
    "options": [
      "Audio",
      "Code",
      "Excel",
      "Link",
      "PDF",
      "PPT",
      "Picture",
      "Text",
      "Unknow",
      "Video",
      "Word",
      "zip",
      "markdown"
    ]
  },
  "mode": {
    "figmaName": "Mode",
    "type": "VARIANT",
    "options": [
      "Dark",
      "Light"
    ]
  }
},
  },
}
