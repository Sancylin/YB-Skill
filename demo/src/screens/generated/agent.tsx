import { useRef, useState } from 'react'
import {
  Button,
  Markdown,
  NavBar,
  TabBar,
} from '../../generated/components'
import { HostCanvas } from '../../library/HostCanvas'
import { DemoShell } from '../DemoShell'

type Scene = 'default' | 'thinking' | 'completed' | 'error'
type Theme = 'light' | 'dark'
type InputType = 'Default' | 'Inputting' | 'Stopped'

const PROMPT = '明天要给领导汇报 Q3 进展，帮我整理成能直接念的要点'
const TABLE_ROWS = (
  <>
    <tr>
      <td>收入</td>
      <td>完成率 96%</td>
      <td>差 4 个点在渠道转化。补救方案已经排到本周，口播时先报完成率，再补这一句原因。</td>
    </tr>
    <tr>
      <td>重点项目</td>
      <td>3 个已上线</td>
      <td>用户侧反馈稳定。其中 1 个延期到 10 月，风险可控，10 月第一周给最终排期。</td>
    </tr>
    <tr>
      <td>渠道转化</td>
      <td>缺口 4 个点</td>
      <td>主要落在转化漏斗后半段，本周会把补救动作同步给销售和运营，避免只报完成率。</td>
    </tr>
    <tr>
      <td>下一步</td>
      <td>10 月第一周</td>
      <td>延期项目给出最终排期；口播按开场 20 秒加三句要点展开，不临场加新数字。</td>
    </tr>
  </>
)

const SCENES: Array<{ id: Scene; label: string }> = [
  { id: 'default', label: '默认' },
  { id: 'thinking', label: '思考中' },
  { id: 'completed', label: '完成' },
  { id: 'error', label: '错误重试' },
]

function catalogUrl() {
  const url = new URL(window.location.href)
  url.searchParams.delete('screen')
  return `${url.pathname}${url.search}${url.hash}`
}

function inputTypeFor(scene: Scene, override: InputType): InputType {
  if (scene === 'thinking') return 'Stopped'
  return override
}

export function AgentConversationDemo() {
  const [scene, setScene] = useState<Scene>('completed')
  const [theme, setTheme] = useState<Theme>('light')
  const [inputType, setInputType] = useState<InputType>('Default')
  const sceneRef = useRef(scene)
  sceneRef.current = scene

  const onAction = (action: string) => {
    const current = sceneRef.current
    if (action === 'send' && current === 'default') {
      setScene('thinking')
      setInputType('Stopped')
    }
    if (action === 'stop' && current === 'thinking') {
      setScene('completed')
      setInputType('Default')
    }
    if (action === 'press' && current === 'error') {
      setScene('thinking')
      setInputType('Stopped')
    }
  }

  return (
    <DemoShell
      chrome={
        <>
          <a href={catalogUrl()}>返回组件目录</a>
          <button onClick={() => setTheme((value) => (value === 'light' ? 'dark' : 'light'))} type="button">
            {theme === 'light' ? 'Dark' : 'Light'}
          </button>
          {SCENES.map((item) => (
            <button
              className={scene === item.id ? 'selected' : ''}
              key={item.id}
              onClick={() => {
                setScene(item.id)
                setInputType(item.id === 'thinking' ? 'Stopped' : 'Default')
              }}
              type="button"
            >
              {item.label}
            </button>
          ))}
        </>
      }
      chromeLabel="对话状态预览"
      theme={theme}
    >
      <HostCanvas aria-label="Agent 对话页" canvasRole="primary" className="agent-conversation-phone" data-theme={theme}>
        <NavBar barType="Agent" divider leftButton rightButton>
          元宝
        </NavBar>

        <div className="agent-conversation-content" data-response-state={scene}>
          {scene !== 'default' ? <Markdown variant="prompt">{PROMPT}</Markdown> : null}

          {scene === 'thinking' ? (
            <div className="markdown-response markdown-response-thinking" data-state="thinking">
              <Markdown
                body="先核对收入、项目节点和风险，再整理成能直接念的要点。"
                variant="Progress"
                {...{ status: 'loading' }}
              >
                正在检索本季度材料
              </Markdown>
            </div>
          ) : null}

          {scene === 'completed' ? <CompletedAnswer onAction={onAction} /> : null}

          {scene === 'error' ? (
            <div className="markdown-response" data-state="error">
              <Markdown variant="Body">材料没有取全，这一轮没法整理成可念的要点。保留刚才的问题，点重试会继续用当前上下文。</Markdown>
              <Button onAction={onAction} size="S" type="Outline">
                重试
              </Button>
            </div>
          ) : null}
        </div>

        <TabBar
          selected="Tab 1 & Input"
          {...{ __agentType: inputTypeFor(scene, inputType) }}
          onAction={onAction}
        />
      </HostCanvas>
    </DemoShell>
  )
}

function CompletedAnswer({ onAction }: { onAction: (action: string) => void }) {
  return (
    <div className="markdown-response markdown-response-completed" data-state="completed">
      <Markdown variant="Others+H3">开场 20 秒</Markdown>
      <Markdown variant="Body">
        领导好。Q3 整体按计划推进，收入完成率 96%，三个重点项目已经上线，有一个延期到 10 月。下面按可直接念的顺序说。
      </Markdown>
      <Markdown variant="Others+H3">三句要点</Markdown>
      <Markdown
        variant="OL"
        items={[
          '收入差 4 个点，主要在渠道转化，补救方案已经排到本周。',
          '三个重点项目按期上线，用户侧反馈稳定。',
          '延期项目风险可控，10 月第一周给最终排期。',
        ]}
      />
      <Markdown variant="Others+H3">数字对照</Markdown>
      <Markdown tableContent={TABLE_ROWS} variant="Table" />
      <Markdown variant="Code" />
      <Markdown variant="IMG" />
      <Markdown items={['帮我压成 1 分钟口播', '把延期项目的风险写成三句话']} onAction={onAction} variant="followUp" />
      <Markdown onAction={onAction} variant="Toolbar" />
    </div>
  )
}

export default AgentConversationDemo
