import { useState } from 'react'
import { Button, FormDoubleLine, NavBar, Toast } from '../../generated/components'
import { HostCanvas } from '../../library/HostCanvas'
import { DemoShell } from '../DemoShell'

const MAX_LENGTH = 300
const MIN_LENGTH = 10

function catalogUrl() {
  const url = new URL(window.location.href)
  url.searchParams.delete('screen')
  return `${url.pathname}${url.search}${url.hash}`
}

export function FeedbackDemo() {
  const [feedback, setFeedback] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  const contentLength = feedback.trim().length
  const canSubmit = contentLength >= MIN_LENGTH && !submitted

  function updateFeedback(value: string) {
    setFeedback(value.slice(0, MAX_LENGTH))
    setSubmitted(false)
  }

  function submitFeedback() {
    if (!canSubmit) return
    setSubmitted(true)
  }

  return (
    <DemoShell
      chrome={
        <>
          <a href={catalogUrl()}>返回组件目录</a>
          <button onClick={() => setTheme((value) => (value === 'light' ? 'dark' : 'light'))} type="button">
            {theme === 'light' ? 'Dark' : 'Light'}
          </button>
        </>
      }
      chromeLabel="意见反馈预览"
      theme={theme}
    >
      <HostCanvas aria-label="意见反馈移动端示例" canvasRole="grouped" className="feedback-phone" data-theme={theme}>
        <NavBar
          barType="Fixed Color Bg"
          divider
          leftButton
          onAction={(action) => {
            if (action === 'back') window.location.assign(catalogUrl())
          }}
          rightButton={false}
        >
          意见反馈
        </NavBar>

        <div className="feedback-content">
          <header>
            <h1>告诉我们你的建议</h1>
            <p>你的反馈会帮助我们持续改善使用体验。</p>
          </header>

          <div className="feedback-form">
            <FormDoubleLine
              active
              input="on"
              label="反馈内容"
              maxLength={MAX_LENGTH}
              onChange={updateFeedback}
              placeholder="请描述遇到的问题或你的建议（至少 10 个字）"
              propDelete={feedback.length > 0}
              value={feedback}
            />
            <div className="feedback-form-meta">
              <span className="feedback-form-hints">
                <span>请勿填写敏感个人信息</span>
                {contentLength > 0 && contentLength < MIN_LENGTH ? (
                  <span className="is-warning">还需 {MIN_LENGTH - contentLength} 个字</span>
                ) : null}
              </span>
              <span>{feedback.length}/{MAX_LENGTH}</span>
            </div>
          </div>

          <Button
            className="feedback-submit"
            onAction={submitFeedback}
            size="L"
            state={canSubmit ? 'Default' : 'Disable'}
            type="Primary"
          >
            {submitted ? '已提交' : '提交反馈'}
          </Button>

          <p className="feedback-privacy">提交即表示你同意我们仅将此内容用于产品体验改进。</p>
        </div>

        {submitted && (
          <div className="feedback-toast">
            <Toast actionButton={false} icon={false} type="Default" onAction={() => setSubmitted(false)}>
              反馈提交成功
            </Toast>
          </div>
        )}
      </HostCanvas>
    </DemoShell>
  )
}
