// url=https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/Yuanbao-Mobile-Components?node-id=82-3021
// source=src/generated/components.tsx
// component=NavBar
import figma from 'figma'

const instance = figma.selectedInstance
const prop_primaryBg = instance.getBoolean("PrimaryBg")
const prop_leftSlot = instance.getSlot("Left Slot")
const prop_rightSlot = instance.getSlot("Right Slot")
const prop_redDot = instance.getBoolean("RedDot")
const prop_themeBg = instance.getBoolean("ThemeBg")
const prop_whiteBGH5 = instance.getBoolean("WhiteBG(H5)")
const prop_divider = instance.getBoolean("Divider")
const prop_title = instance.getBoolean("Title")
const prop_leftButton = instance.getBoolean("Left Button")
const prop_rightButton = instance.getBoolean("Right Button")
const prop_secondaryBg = instance.getBoolean("SecondaryBg")
const prop_badgeNumber = instance.getBoolean("Badge Number")
const prop_middleSlot = instance.getSlot("Middle Slot")
const prop_barType = instance.getEnum("Bar Type", {
  "Agent": "Agent",
  "Gradient Color Bg": "Gradient Color Bg",
  "Fixed Color Bg": "Fixed Color Bg",
  "Agent_iPad": "Agent_iPad",
  "Gradient Color Bg_iPad": "Gradient Color Bg_iPad",
  "Fixed Color Bg_iPad": "Fixed Color Bg_iPad",
  "Bar new icon": "Bar new icon"
})

export default {
  example: figma.code`<NavBar ${prop_primaryBg ? "primaryBg" : ''} ${prop_leftSlot ? figma.code` leftSlot={${prop_leftSlot}}` : ''} ${prop_rightSlot ? figma.code` rightSlot={${prop_rightSlot}}` : ''} ${prop_redDot ? "redDot" : ''} ${prop_themeBg ? "themeBg" : ''} ${prop_whiteBGH5 ? "whiteBGH5" : ''} ${prop_divider ? "divider" : ''} ${prop_title ? "title" : ''} ${prop_leftButton ? "leftButton" : ''} ${prop_rightButton ? "rightButton" : ''} ${prop_secondaryBg ? "secondaryBg" : ''} ${prop_badgeNumber ? "badgeNumber" : ''} ${prop_middleSlot ? figma.code` middleSlot={${prop_middleSlot}}` : ''} barType="${prop_barType}" />`,
  imports: ['import { NavBar } from "./src/generated/components"'],
  id: "yb-82-3021",
  metadata: {
    nestable: false,
    props: {
  "primaryBg": {
    "figmaName": "PrimaryBg",
    "type": "BOOLEAN",
    "options": []
  },
  "leftSlot": {
    "figmaName": "Left Slot",
    "type": "SLOT",
    "options": []
  },
  "rightSlot": {
    "figmaName": "Right Slot",
    "type": "SLOT",
    "options": []
  },
  "redDot": {
    "figmaName": "RedDot",
    "type": "BOOLEAN",
    "options": []
  },
  "themeBg": {
    "figmaName": "ThemeBg",
    "type": "BOOLEAN",
    "options": []
  },
  "whiteBGH5": {
    "figmaName": "WhiteBG(H5)",
    "type": "BOOLEAN",
    "options": []
  },
  "divider": {
    "figmaName": "Divider",
    "type": "BOOLEAN",
    "options": []
  },
  "title": {
    "figmaName": "Title",
    "type": "BOOLEAN",
    "options": []
  },
  "leftButton": {
    "figmaName": "Left Button",
    "type": "BOOLEAN",
    "options": []
  },
  "rightButton": {
    "figmaName": "Right Button",
    "type": "BOOLEAN",
    "options": []
  },
  "secondaryBg": {
    "figmaName": "SecondaryBg",
    "type": "BOOLEAN",
    "options": []
  },
  "badgeNumber": {
    "figmaName": "Badge Number",
    "type": "BOOLEAN",
    "options": []
  },
  "middleSlot": {
    "figmaName": "Middle Slot",
    "type": "SLOT",
    "options": []
  },
  "barType": {
    "figmaName": "Bar Type",
    "type": "VARIANT",
    "options": [
      "Agent",
      "Gradient Color Bg",
      "Fixed Color Bg",
      "Agent_iPad",
      "Gradient Color Bg_iPad",
      "Fixed Color Bg_iPad",
      "Bar new icon"
    ]
  }
},
  },
}
