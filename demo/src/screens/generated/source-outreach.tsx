import { useEffect, useRef, useState } from 'react'
import {
  BottomSheet,
  Button,
  Card,
  Markdown,
  Mask,
  NavBar,
  TabBar,
  Toast,
} from '../../generated/components'
import { Icon } from '../../library/Icon'
import { HostCanvas } from '../../library/HostCanvas'
import { DemoShell } from '../DemoShell'

type Scene = 'thinking' | 'freshness' | 'news-cards' | 'related-videos' | 'cards-loading' | 'cards-error' | 'no-cards'
type Theme = 'light' | 'dark'
type InputType = 'Default' | 'Inputting' | 'Stopped'

type SourceDetail = {
  domain: string
  site: string
  snippet?: string
  time?: string
  title: string
}

const NEWS_CARDS: SourceDetail[] = [
  {
    domain: 'reuters.com',
    site: 'Reuters',
    time: '11小时前',
    title: 'Bessent says US to apply measures never seen on Iran',
    snippet: '美方表态准备采取前所未见的经济措施，进一步孤立伊朗。',
  },
  {
    domain: 'reuters.com',
    site: 'Reuters',
    time: '5小时前',
    title: 'A conflict on autopilot? How sanctions now target the full oil chain',
    snippet: '制裁对象开始覆盖出口、回款和第三方中介整条链。',
  },
]

const FRESHNESS_SOURCES: SourceDetail[] = [
  {
    domain: 'xinhuanet.com',
    site: '新华社',
    time: '2小时前',
    title: '美股盘前：标普500期货小幅上涨，科技股财报季或引发波动',
    snippet: '美股期货小幅高开，科技股财报季可能带来波动。',
  },
  {
    domain: 'cs.com.cn',
    site: '中国证券报',
    time: '3小时前',
    title: '英伟达财报今晚公布，关注 AI 需求与数据中心',
    snippet: '市场关注英伟达业绩对 AI 需求和数据中心资本开支的指引。',
  },
]

const SCENES: Array<{ id: Scene; label: string }> = [
  { id: 'thinking', label: '思考中' },
  { id: 'freshness', label: '场景一·时效' },
  { id: 'news-cards', label: '场景二·新闻卡' },
  { id: 'related-videos', label: '相关视频' },
  { id: 'cards-loading', label: '卡片加载' },
  { id: 'cards-error', label: '卡片失败' },
  { id: 'no-cards', label: '无合格信源' },
]

function catalogUrl() {
  const url = new URL(window.location.href)
  url.searchParams.delete('screen')
  return `${url.pathname}${url.search}${url.hash}`
}

function promptFor(scene: Scene) {
  if (scene === 'freshness') return '美股市场最近的动荡'
  if (scene === 'related-videos') return '给我几个学习植物学的讲解视频'
  return '美国最近对伊朗有什么制裁措施？'
}

function linkIcon() {
  return <Icon decorative name="Icon/link" size={20} />
}

function sheetCopy(scene: Scene, detail: SourceDetail) {
  if (scene === 'freshness') {
    return {
      title: '信源',
      descText: detail.time ? `${detail.site} · ${detail.time}` : `${detail.site} · 非新闻来源`,
      buttonLabel: '查看来源',
    }
  }
  return {
    title: '新闻预览',
    descText: detail.time ? `${detail.site} · ${detail.time}` : detail.site,
    buttonLabel: '打开原文',
  }
}

export function SourceOutreachDemo() {
  const [scene, setScene] = useState<Scene>('news-cards')
  const [theme, setTheme] = useState<Theme>('light')
  const [inputType, setInputType] = useState<InputType>('Default')
  const [toast, setToast] = useState('')
  const [detail, setDetail] = useState<SourceDetail | null>(null)
  const sceneRef = useRef(scene)
  const detailRef = useRef(detail)
  sceneRef.current = scene
  detailRef.current = detail

  useEffect(() => {
    if (!toast) return undefined
    const timer = window.setTimeout(() => setToast(''), 3000)
    return () => window.clearTimeout(timer)
  }, [toast])

  const openOriginal = (source: SourceDetail) => {
    setDetail(null)
    setToast(`即将打开 ${source.domain}`)
  }

  const copy = detail ? sheetCopy(scene, detail) : null

  const onAction = (action: string) => {
    if (action === 'mask' || action === 'close') {
      setDetail(null)
      return
    }
    if (action === 'press') {
      if (detailRef.current) {
        openOriginal(detailRef.current)
        return
      }
      if (sceneRef.current === 'cards-error') {
        setScene('news-cards')
        setToast('已重新匹配信源')
      }
      return
    }
    if (action === 'share') {
      setToast('即将分享这篇报道')
      return
    }
    if (action === 'video' || action === 'play') setToast('即将播放讲解视频')
    if (action.startsWith('follow-up:')) setToast('已填入追问')
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
                setDetail(null)
                setInputType(item.id === 'thinking' ? 'Stopped' : 'Default')
              }}
              type="button"
            >
              {item.label}
            </button>
          ))}
        </>
      }
      chromeLabel="信源外展预览"
      theme={theme}
    >
      <HostCanvas aria-label="信源外展对话页" canvasRole="primary" className="agent-conversation-phone" data-theme={theme}>
        <NavBar barType="Agent" divider leftButton rightButton>
          元宝
        </NavBar>

        <div className="agent-conversation-content" data-response-state={scene}>
          <Markdown variant="prompt">{promptFor(scene)}</Markdown>

          {scene === 'thinking' ? (
            <div className="markdown-response markdown-response-thinking" data-state="thinking">
              <Markdown
                body="正在核对近 3 天的权威公开报道，并确认是不是新闻媒体。"
                variant="Progress"
                {...{ status: 'loading' }}
              >
                正在检索权威新闻信源
              </Markdown>
            </div>
          ) : null}

          {scene === 'freshness' ? <FreshnessAnswer onAction={onAction} onOpenSource={setDetail} /> : null}

          {scene === 'news-cards' || scene === 'cards-loading' || scene === 'cards-error' || scene === 'no-cards' ? (
            <NewsAnswer onAction={onAction} onOpenCard={setDetail} scene={scene} />
          ) : null}

          {scene === 'related-videos' ? <VideoAnswer onAction={onAction} /> : null}
        </div>

        <TabBar selected="Tab 1 & Input" {...{ __agentType: inputType }} onAction={onAction} />

        {detail && copy ? (
          <div className="yb-sheet-layer source-overlay">
            <Mask onAction={onAction} type="popup mask" />
            <BottomSheet
              buttonGroup
              handle
              navBar
              onAction={onAction}
              {...{
                buttonType: '1Btn' as const,
                title: copy.title,
                descText: copy.descText,
                buttonLabel: copy.buttonLabel,
                leftIconName: 'Icon/close-sm',
                rightIconName: 'Icon/share',
              }}
            >
              <div className="source-sheet-content">
                <strong>{detail.title}</strong>
                {detail.snippet ? <p>{detail.snippet}</p> : null}
              </div>
            </BottomSheet>
          </div>
        ) : null}

        {toast ? (
          <div className="source-toast">
            <Toast actionButton={false} icon={false} onAction={() => setToast('')} type="Default">
              {toast}
            </Toast>
          </div>
        ) : null}
      </HostCanvas>
    </DemoShell>
  )
}

function OutputCard({
  source,
  onOpen,
}: {
  source: SourceDetail
  onOpen: (source: SourceDetail) => void
}) {
  return (
    <button className="source-output-hit" onClick={() => onOpen(source)} type="button">
      <Card
        card="Output"
        content={<span>{source.time ? `${source.site} · ${source.time}` : source.site}</span>}
        leftSlot={linkIcon()}
        pressed="off"
      >
        {source.title}
      </Card>
    </button>
  )
}

function FreshnessAnswer({
  onAction,
  onOpenSource,
}: {
  onAction: (action: string) => void
  onOpenSource: (source: SourceDetail) => void
}) {
  return (
    <div className="markdown-response markdown-response-completed" data-state="completed">
      <Markdown variant="Body">
        按北京时间今晚来看，美股 8 月 26 日盘还没收，所以下面用的是前一交易日收盘后的公开信息。市场仍在消化科技股财报和利率预期，波动主要集中在纳指和英伟达相关链条。
      </Markdown>
      <Markdown
        variant="UL"
        items={['标普500与纳指期货小幅波动，市场在等科技股业绩指引。', '英伟达财报窗口临近，AI 需求和数据中心开支是定价核心。', '以下信源均来自近 3 天内的公开报道。']}
      />
      <div className="source-output-stack" data-module="freshness">
        {FRESHNESS_SOURCES.map((source) => (
          <OutputCard key={source.title} onOpen={onOpenSource} source={source} />
        ))}
      </div>
      <Markdown items={['英伟达今晚可能怎么定价？', '标普500关键支撑在哪？']} onAction={onAction} variant="followUp" />
      <Markdown onAction={onAction} variant="Toolbar" />
    </div>
  )
}

function NewsAnswer({
  scene,
  onOpenCard,
  onAction,
}: {
  scene: Scene
  onOpenCard: (card: SourceDetail) => void
  onAction: (action: string) => void
}) {
  return (
    <div className="markdown-response markdown-response-completed" data-state="completed">
      <Markdown variant="Body">
        到 8 月 20 日，OFAC 还没放出新的正式制裁清单，所以当前更像政策加码信号，而不是已经落地的新一轮制裁。美国正在把打击面从“卖油”扩到出口、回款、洗钱和采购回流的整条链。
      </Markdown>
      <Markdown
        items={
          scene === 'no-cards'
            ? [
                '8 月 13 日，美方表态准备采取“前所未见”的经济措施进一步孤立伊朗。',
                '制裁对象开始覆盖中国、香港、阿联酋等地的第三方中介。',
                '这一题没有达到时效或资讯门槛的合格信源，所以文末不出新闻卡。',
              ]
            : [
                '8 月 13 日，美方表态准备采取“前所未见”的经济措施进一步孤立伊朗。',
                '制裁对象开始覆盖中国、香港、阿联酋等地的第三方中介。',
                '更完整的一手报道可以看文末的新闻卡。',
              ]
        }
        variant="UL"
      />
      {scene === 'cards-loading' ? (
        <Markdown body="正在按近 3 天报道和媒体类型匹配新闻卡。" variant="Progress" {...{ status: 'loading' }}>
          正在匹配权威新闻信源
        </Markdown>
      ) : null}
      {scene === 'cards-error' ? (
        <>
          <Markdown variant="Body">新闻卡暂时没有加载出来，可以重试。</Markdown>
          <Button className="source-card-retry" onAction={onAction} size="S" type="Outline">
            重试
          </Button>
        </>
      ) : null}
      {scene === 'news-cards' ? (
        <div className="source-output-stack" data-module="news">
          {NEWS_CARDS.map((card) => (
            <OutputCard key={card.title} onOpen={onOpenCard} source={card} />
          ))}
        </div>
      ) : null}
      {scene === 'cards-loading' ? null : (
        <>
          <Markdown
            items={['下一轮制裁可能覆盖哪些中介？', '和现在已生效的清单有什么差别？']}
            onAction={onAction}
            variant="followUp"
          />
          <Markdown onAction={onAction} variant="Toolbar" />
        </>
      )}
    </div>
  )
}

function VideoAnswer({ onAction }: { onAction: (action: string) => void }) {
  return (
    <div className="markdown-response markdown-response-completed" data-state="completed">
      <Markdown variant="Body">
        如果你想系统学植物学，而不是只查某一种植物，下面这些讲解更适合入门。这一题不是强资讯场景，所以出相关视频，不出新闻卡。
      </Markdown>
      <Markdown
        onAction={onAction}
        variant="video"
        {...{ videoType: 'horizontal', videoOwner: '植物志讲解', videoTime: '3天前' }}
      >
        植物学入门：叶片、花和科属怎么认
      </Markdown>
      <Markdown items={['POWO 和植物智怎么配合用？', '再给几个中文讲解']} onAction={onAction} variant="followUp" />
      <Markdown onAction={onAction} variant="Toolbar" />
    </div>
  )
}

export default SourceOutreachDemo
