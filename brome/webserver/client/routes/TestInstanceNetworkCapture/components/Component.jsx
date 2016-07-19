import React from 'react'
// import { FormattedMessage } from 'react-intl'
import Collapse, { Panel } from 'rc-collapse'
import 'rc-collapse/assets/index.css'

// import ComponentStyle from './ComponentStyle.postcss'
import BrowserBadge from 'components/ux/BrowserBadge'
import ErrorMsg from 'components/ux/ErrorMsg'
import Pager from 'components/ux/Pager'
import Loading from 'components/ux/Loading'
import BaseComponent from 'core/BaseComponent'

const TEST_INSTANCE_NETWORK_CAPTURE_LIMIT = 10

class TestInstanceNetworkCapture extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'getTestBatch',
      'getTestBatchUid',
      'fetchTestInstanceNetworkCapture',
      'onFirstClick',
      'onPreviousClick',
      'onNextClick',
      'onLastClick',
      'getCurrentPage'
    )
  }

  componentWillMount () {
    this.debug('componentWillUnmount')

    this.fetchTestInstanceNetworkCapture(0)
  }

  componentWillReceiveProps () {
    let testBatch = this.getTestBatch()

    // Add a setTimeout if the testBatch is live
    // Remove the interval otherwise
    if (testBatch) {
      // Terminated
      if (testBatch.terminated) {
        if (this._interval) {
          clearInterval(this._interval)
          this._interval = null
        }
      // Alive
      } else {
        this._interval = setTimeout(() => {
          this.fetchTestInstanceNetworkCapture(0)
        },
        2000)
      }
    }
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')

    clearInterval(this._interval)
  }

  onFirstClick () {
    this.debug('onFirstClick')
    this.fetchTestInstanceNetworkCapture(0)
  }

  onLastClick () {
    this.debug('onLastClick')
    let skip = Math.floor(this.props.state.testinstancenetworkcapture.totalTestInstance / TEST_INSTANCE_NETWORK_CAPTURE_LIMIT) * TEST_INSTANCE_NETWORK_CAPTURE_LIMIT
    this.fetchTestInstanceNetworkCapture(skip)
  }

  onNextClick () {
    this.debug('onNextClick')
    let skip = (this.getCurrentPage() + 1) * TEST_INSTANCE_NETWORK_CAPTURE_LIMIT
    this.fetchTestInstanceNetworkCapture(skip)
  }

  onPreviousClick () {
    this.debug('onPreviousClick')
    let skip = this.props.state.testinstancenetworkcapture.skip - TEST_INSTANCE_NETWORK_CAPTURE_LIMIT
    this.fetchTestInstanceNetworkCapture(skip)
  }

  getCurrentPage () {
    return this.props.state.testinstancenetworkcapture.skip / this.props.state.testinstancenetworkcapture.limit
  }

  fetchTestInstanceNetworkCapture (skip) {
    this.props.actions.doFetchTestInstanceNetworkCapture(
      this.props.state.session,
      this.getTestBatchUid(),
      skip,
      TEST_INSTANCE_NETWORK_CAPTURE_LIMIT
    )
  }

  getTestBatchUid () {
    return this.props.location.query['testbatchuid']
  }

  getTestBatch () {
    return this.props.state.testinstancenetworkcapture.testBatch
  }

  render () {
    let testinstancenetworkcapture = this.props.state.testinstancenetworkcapture

    if (testinstancenetworkcapture.error) {
      return <ErrorMsg msgId={testinstancenetworkcapture.error} />
    } else if (testinstancenetworkcapture.testInstanceNetworkCaptureList === null) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else {
      let testInstances = this.props.state.testinstancenetworkcapture.testInstanceNetworkCaptureList
      let testBatch = this.getTestBatch()

      return (
        <div>
          <h2 className='text-center'>
            Test Instance Network Capture List <small> ({testBatch.friendly_name}) ({testBatch.uid})</small>
          </h2>
          <ul>
          {(() => {
            return testInstances.map((testInstance, index) => {
              let title = <span>
                {testInstance.name}
                <BrowserBadge
                  browserName={testInstance.browser_capabilities.browserName}
                  browserIcon={testInstance.browser_capabilities.browserName}
                  browserVersion={testInstance.browser_capabilities.version}
                  platform={testInstance.browser_capabilities.platform}
                />
              </span>
              return (
                <div key={index}>
                  <Collapse accordion>
                    <Panel header={title} key={index}>
                      <a href={'/test_results/' + testInstance.network_capture_path} className='btn btn-default'>
                        Download
                      </a>
                      <button className='btn btn-default'>
                        Analyse
                      </button>
                    </Panel>
                  </Collapse>
                </div>
              )
            })
          })()}
          </ul>
          {(() => {
            if (testBatch.terminated) {
              let totalPage = parseInt(Math.ceil(this.props.state.testinstancenetworkcapture.totalTestInstance / TEST_INSTANCE_NETWORK_CAPTURE_LIMIT))
              return (
                <Pager
                  totalPage={totalPage}
                  currentPage={this.getCurrentPage()}
                  onFirstClick={this.onFirstClick}
                  onLastClick={this.onLastClick}
                  onNextClick={this.onNextClick}
                  onPreviousClick={this.onPreviousClick}
                />
              )
            } else {
              return null
            }
          })()}
        </div>
      )
    }
  }
}

module.exports = TestInstanceNetworkCapture
