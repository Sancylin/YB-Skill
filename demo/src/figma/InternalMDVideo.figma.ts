// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=15331-17801
// source=src/generated/components.tsx
// component=InternalMDVideo
import figma from 'figma'

const instance = figma.selectedInstance
const prop_videos = instance.getSlot("videos")
const prop_type = instance.getEnum("type", {
  "horizontal": "horizontal",
  "multi": "multi",
  "vertical": "vertical"
})

export default {
  example: figma.code`<InternalMDVideo ${prop_videos ? figma.code` videos={${prop_videos}}` : ''} type="${prop_type}" />`,
  imports: ['import { InternalMDVideo } from "./src/generated/components"'],
  id: "yb-15331-17801",
  metadata: {
    nestable: true,
    props: {
  "videos": {
    "figmaName": "videos",
    "type": "SLOT",
    "options": []
  },
  "type": {
    "figmaName": "type",
    "type": "VARIANT",
    "options": [
      "horizontal",
      "multi",
      "vertical"
    ]
  }
},
  },
}
