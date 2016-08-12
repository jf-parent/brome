import React from 'react'
// import { FormattedMessage } from 'react-intl'
import BrowserBadge from 'components/ux/BrowserBadge'
import Collapse, { Panel } from 'rc-collapse'
import 'font-awesome-webpack'
import 'rc-collapse/assets/index.css'

import VideoPlayer from 'components/ux/VideoPlayer'
import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
// import ComponentStyle from './ComponentStyle.postcss'
import Pager from 'components/ux/Pager'
import BaseComponent from 'core/BaseComponent'

const TEST_RESULT_LIMIT = 10

class TestBatchTestResults extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'fetchTestResults',
      'getTestBatchUid'
    )
  }

  componentWillMount () {
    this.fetchTestResults(this.props.state.testbatchtestresults.skip, true)
    this._interval = setInterval(
      () => {
        this.fetchTestResults(this.props.state.testbatchtestresults.skip, false)
      },
      2000
    )
  }

  componentWillReceiveProps () {
    let testbatchtestresults = this.props.state.testbatchtestresults

    // Clear interval on terminated testbatch
    if (testbatchtestresults.testBatch) {
      if (testbatchtestresults.testBatch.terminated) {
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

  getTestBatchUid () {
    return this.props.location.query['testbatchuid']
  }

  fetchTestResults (skip, loading = false) {
    this.props.actions.doLoadTestResults(
      this.props.state.session,
      this.getTestBatchUid(),
      skip,
      TEST_RESULT_LIMIT,
      loading
    )
  }

  render () {
    let testbatchtestresults = this.props.state.testbatchtestresults

    if (testbatchtestresults.loading) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else if (testbatchtestresults.error) {
      return <ErrorMsg msgId={testbatchtestresults.error} name='error-test-batch-test-results' />
    } else {
      let testBatch = this.props.state.testbatchtestresults.testBatch

      return (
        <div>
          <h2>Test Results <small>({testBatch.friendly_name}) ({testBatch.uid})</small></h2>

          {(() => {
            let testResults = testbatchtestresults.testResults

            return testResults.map((testResult, index) => {
              let headerStyle = {}
              let headerIcon = null
              if (testResult.result) {
                headerStyle['color'] = 'green'
                headerIcon = 'fa-thumbs-up'
              } else {
                headerStyle['color'] = 'red'
                headerIcon = 'fa-thumbs-down'
              }
              let header = <div style={{top: '-40px'}} className='text-ellipsis'>
                <i className={'fa ' + headerIcon} style={headerStyle} aria-hidden='true'></i>
                {' '}
                {testResult.test_id}
                {' '}
                {testResult.title}
                <BrowserBadge
                  browserName={testResult.browser_capabilities.browserName}
                  browserVersion={testResult.browser_capabilities.version}
                  browserIcon={testResult.browser_capabilities.browserName}
                  platform={testResult.browser_capabilities.platform}
                />
              </div>
              return (
                <div key={index}>
                  <Collapse accordion>
                    <Panel header={header} key={index}>
                      <Collapse accordion>
                        <Panel header='Screenshot'>
                          {(() => {
                            if (testResult.screenshot_path !== '') {
                              return (
                                <a href={testResult.screenshot_path} target='_blank'>
                                  <img className='img-responsive' src={testResult.screenshot_path} />
                                </a>
                              )
                            } else {
                              return (
                                <small>No screenshot</small>
                              )
                            }
                          })()}
                        </Panel>
                        <Panel header='Video Capture'>
                          {(() => {
                            if (testResult.video_capture_path !== '') {
                              return (
                                <VideoPlayer src={testResult.video_capture_path} currentTime={testResult.video_capture_current_time} />
                              )
                            } else {
                              return (
                                <small>No video capture</small>
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
          <Pager
            skippedItem={testbatchtestresults.skip}
            fetchData={this.fetchTestResults}
            totalItem={testbatchtestresults.totalTestResults}
            itemPerPage={TEST_RESULT_LIMIT}
          />
        </div>
      )
    }
  }
}

module.exports = TestBatchTestResults
