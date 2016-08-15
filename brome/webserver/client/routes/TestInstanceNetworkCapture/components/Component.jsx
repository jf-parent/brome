import React from 'react'
// import { FormattedMessage } from 'react-intl'
import Collapse, { Panel } from 'rc-collapse'
import 'rc-collapse/assets/index.css'

// import ComponentStyle from './ComponentStyle.postcss'
import Breadcrumbs from 'components/ux/Breadcrumbs'
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
      'fetchTestInstanceNetworkCapture'
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
      let routes = [
        {
          msgId: 'TestBatchDetail',
          to: '/testbatchdetail?testbatchuid=' + testBatch.uid
        },
        {
          msgId: 'TestInstanceNetworkCapture',
          disable: true
        }
      ]

      return (
        <div>
          <Breadcrumbs routes={routes} />
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
                      <a href={testInstance.network_capture_path} className='btn btn-default'>
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
          <Pager
            skippedItem={testinstancenetworkcapture.skip}
            fetchData={this.fetchTestInstanceNetworkCapture}
            totalItem={testinstancenetworkcapture.totalTestInstanceNetworkCapture}
            itemPerPage={TEST_INSTANCE_NETWORK_CAPTURE_LIMIT}
          />
        </div>
      )
    }
  }
}

module.exports = TestInstanceNetworkCapture
