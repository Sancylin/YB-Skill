import { FeedbackDemo } from './examples/FeedbackDemo'
import { AgentConversationDemo } from './generated/agent'
import { SourceOutreachDemo } from './generated/source-outreach'
import type { DemoScreenRegistry } from './types'

export const screenRegistry = {
  agent: {
    component: AgentConversationDemo,
    description: '用户提问后看到思考中到完成态结构化回答，可追问和再输入',
    title: 'Agent 对话页',
  },
  'source-outreach': {
    component: SourceOutreachDemo,
    description: '搜索问答文末给出时效信源或新闻卡，相关视频与新闻卡互斥',
    title: '信源外展',
  },
  feedback: {
    component: FeedbackDemo,
    description: '可输入、校验并提交的完整移动端意见反馈页',
    title: '意见反馈',
  },
} as const satisfies DemoScreenRegistry

export type ScreenId = keyof typeof screenRegistry

export function isScreenId(value: string): value is ScreenId {
  return Object.hasOwn(screenRegistry, value)
}
