import React from 'react'
import { defineMessages, injectIntl, FormattedMessage } from 'react-intl'
import Collapse, { Panel } from 'rc-collapse'
import 'rc-collapse/assets/index.css'

import Breadcrumbs from 'components/ux/Breadcrumbs'
import VideoPlayer from 'components/ux/VideoPlayer'
import BrowserBadge from 'components/ux/BrowserBadge'
import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
// import ComponentStyle from './ComponentStyle.postcss'
import BaseComponent from 'core/BaseComponent'

const testBatchCrashesMessages = defineMessages({
  screenshotPlaceholder: {
    id: 'testBatchCrashes.Screenshot',
    defaultMessage: 'Screenshot'
  },
  videoCapturePlaceholder: {
    id: 'testBatchCrashes.VideoCapture',
    defaultMessage: 'Video Capture'
  }
})

class TestBatchCrashes extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'fetchTestBatchCrashes',
      'getTestBatchUid',
      'getTestBatch'
    )
  }

  componentWillMount () {
    this.debug('componentWillMount')

    this.fetchTestBatchCrashes(true)
    this._interval = setInterval(
      () => {
        this.fetchTestBatchCrashes(false)
      },
      2000
    )
  }

  componentWillReceiveProps () {
    let testBatch = this.getTestBatch()

    // Clear interval on terminated testbatch
    if (testBatch) {
      if (testBatch.terminated) {
        if (this._interval) {
          clearInterval(this._interval)
          this._interval = null
        }
      }
    }
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')
    clearInterval(this._interval)
  }

  fetchTestBatchCrashes (loading) {
    this.props.actions.doLoadTestBatchCrashes(
      this.props.state.session,
      this.getTestBatchUid(),
      loading
    )
  }

  getTestBatchUid () {
    return this.props.location.query['testbatchuid']
  }

  getTestBatch () {
    return this.props.state.testbatchcrashes.testBatch
  }

  render () {
    let testbatchcrashes = this.props.state.testbatchcrashes

    if (testbatchcrashes.error) {
      return <ErrorMsg msgId={testbatchcrashes.error} />
    } else if (testbatchcrashes.crashes === null) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else {
      let testBatch = this.props.state.testbatchcrashes.testBatch
      const { formatMessage } = this.props.intl
      const videoCapturePlaceholder = formatMessage(testBatchCrashesMessages.videoCapturePlaceholder)
      const screenshotPlaceholder = formatMessage(testBatchCrashesMessages.screenshotPlaceholder)

      let routes = [
        {
          msgId: 'TestBatchDetail',
          to: '/testbatchdetail?testbatchuid=' + testBatch.uid
        },
        {
          msgId: 'TestBatchCrashes',
          disable: true
        }
      ]
      return (
        <div>
          <Breadcrumbs routes={routes} />
          <h2>
            <FormattedMessage
              id='testBatchCrashes.TestBatchCrashes'
              defaultMessage='Test Batch Crashes'
            />
            {' '}
            <small>({testBatch.friendly_name}) ({testBatch.uid})</small>
          </h2>

          {(() => {
            let crashes = testbatchcrashes.crashes

            return crashes.map((crash, index) => {
              let crashTitle = <div style={{top: '-40px'}} className='text-ellipsis'>
                <i className='fa fa-exclamation-triangle' aria-hidden='true'></i>
                {' '}
                {crash.title}
                <BrowserBadge
                  browserName={crash.browser_capabilities.browserName}
                  browserIcon={crash.browser_capabilities.browserName}
                  browserVersion={crash.browser_capabilities.version}
                  platform={crash.browser_capabilities.platform}
                />
              </div>

              return (
                <div key={index}>
                  <Collapse accordion>
                    <Panel header={crashTitle} key={index}>
                      <Collapse accordion>
                        <Panel header='Trace'>
                          <div style={{overflow: 'scroll'}}>
                            <ol>
                              {(() => {
                                return crash.trace.map((line, index) => {
                                  return (
                                    <li key={index}>
                                      <small>
                                        {line}
                                      </small>
                                    </li>
                                  )
                                })
                              })()}
                            </ol>
                          </div>
                        </Panel>
                        <Panel header={screenshotPlaceholder}>
                          {(() => {
                            if (crash.screenshot_path !== '') {
                              return (
                                <a href={crash.screenshot_path} target='_blank'>
                                  <img className='img-responsive' src={crash.screenshot_path} />
                                </a>
                              )
                            } else {
                              return (
                                <small>
                                  <FormattedMessage
                                    id='testBatchCrashes.NoScreenshot'
                                    defaultMessage='No screenshot'
                                  />
                                </small>
                              )
                            }
                          })()}
                        </Panel>
                        <Panel header={videoCapturePlaceholder}>
                          {(() => {
                            if (crash.video_capture_path !== '') {
                              return (
                                <VideoPlayer src={crash.video_capture_path} currentTime={crash.video_capture_current_time} />
                              )
                            } else {
                              return (
                                <small>
                                  <FormattedMessage
                                    id='testBatchCrashes.NoVideoCapture'
                                    defaultMessage='No video capture'
                                  />
                                </small>
                              )
                            }
                          })()}
                        </Panel>
                      </Collapse>
                    </Panel>
                  </Collapse>
                </div>
              )
            })
          })()}
        </div>
      )
    }
  }
}

module.exports = injectIntl(TestBatchCrashes)
