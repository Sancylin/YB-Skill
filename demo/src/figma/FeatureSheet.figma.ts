// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=3149-27036
// source=src/generated/components.tsx
// component=FeatureSheet
import figma from 'figma'

const instance = figma.selectedInstance
const prop_indicator = instance.getBoolean("indicator")
const prop_pic = instance.getSlot("pic")

export default {
  example: figma.code`<FeatureSheet ${prop_indicator ? "indicator" : ''} ${prop_pic ? figma.code` pic={${prop_pic}}` : ''} />`,
  imports: ['import { FeatureSheet } from "./src/generated/components"'],
  id: "yb-3149-27036",
  metadata: {
    nestable: false,
    props: {
  "indicator": {
    "figmaName": "indicator",
    "type": "BOOLEAN",
    "options": []
  },
  "pic": {
    "figmaName": "pic",
    "type": "SLOT",
    "options": []
  }
},
  },
}
