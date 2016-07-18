import React from 'react'
// import { FormattedMessage } from 'react-intl'
import Collapse, { Panel } from 'rc-collapse'
import 'font-awesome-webpack'
import 'rc-collapse/assets/index.css'

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
      'onFirstClick',
      'onPreviousClick',
      'onNextClick',
      'onLastClick',
      'getTestBatchUid',
      'getCurrentPage'
    )
  }

  componentWillMount () {
    this._interval = setInterval(
      () => {
        this.fetchTestResults(this.props.state.testbatchtestresults.skip)
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

  fetchTestResults (skip) {
    this.props.actions.doLoadTestResults(
      this.props.state.session,
      this.getTestBatchUid(),
      skip,
      TEST_RESULT_LIMIT
    )
  }

  getCurrentPage () {
    return this.props.state.testbatchtestresults.skip / this.props.state.testbatchtestresults.limit
  }

  onFirstClick () {
    this.debug('onFirstClick')
    this.fetchTestResults(0)
  }

  onLastClick () {
    this.debug('onLastClick')
    let skip = Math.floor(this.props.state.testbatchtestresults.totalTestBatch / TEST_RESULT_LIMIT) * TEST_RESULT_LIMIT
    this.fetchTestResults(skip)
  }

  onNextClick () {
    this.debug('onNextClick')
    let nextPage = (this.getCurrentPage() + 1) * TEST_RESULT_LIMIT
    this.fetchTestResults(nextPage)
  }

  onPreviousClick () {
    this.debug('onPreviousClick')
    let previousPage = this.props.state.testbatchtestresults.skip - TEST_RESULT_LIMIT
    this.fetchTestResults(previousPage)
  }

  render () {
    let testbatchtestresults = this.props.state.testbatchtestresults

    if (!testbatchtestresults.testResults.length) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else if (testbatchtestresults.error) {
      return <ErrorMsg msgId={testbatchtestresults.error} name='error-test-batch-test-results' />
    } else {
      let testBatch = this.props.state.testbatchtestresults.testBatch
      let totalPage = parseInt(Math.ceil(this.props.state.testbatchtestresults.totalTestResults / TEST_RESULT_LIMIT))
      let currentPage = this.getCurrentPage()

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
              let header = <span><i className={'fa ' + headerIcon} style={headerStyle} aria-hidden='true'></i>{' '}{testResult.title}</span>
              return (
                <div key={index}>
                  <Collapse accordion>
                    <Panel header={header} key={index}>
                      <Collapse accordion>
                        <Panel header='Screenshot'>
                          {(() => {
                            if (testResult.screenshot_path !== '') {
                              let path = '/test_results/' + testResult.screenshot_path
                              return (
                                <a href={path} target='_blank'>
                                  <img className='img-responsive' src={path} />
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
                            if (testResult.videocapture_path !== '') {
                              return (
                                <small>TODO</small>
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
            totalPage={totalPage}
            currentPage={currentPage}
            onFirstClick={this.onFirstClick}
            onLastClick={this.onLastClick}
            onNextClick={this.onNextClick}
            onPreviousClick={this.onPreviousClick}
          />
        </div>
      )
    }
  }
}

module.exports = TestBatchTestResults
