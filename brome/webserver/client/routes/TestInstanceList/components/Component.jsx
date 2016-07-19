import React from 'react'
import { Link } from 'react-router'
// import { FormattedMessage } from 'react-intl'

// import ComponentStyle from './ComponentStyle.postcss'
import BrowserBadge from 'components/ux/BrowserBadge'
import ErrorMsg from 'components/ux/ErrorMsg'
import Pager from 'components/ux/Pager'
import Loading from 'components/ux/Loading'
import BaseComponent from 'core/BaseComponent'

const TEST_INSTANCE_LIMIT = 10

class TestInstanceList extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'getTestBatch',
      'getPath',
      'getTestBatchUid',
      'fetchTestInstance',
      'onFirstClick',
      'onPreviousClick',
      'onNextClick',
      'onLastClick',
      'getCurrentPage'
    )
  }

  componentWillMount () {
    this.debug('componentWillUnmount')

    this.fetchTestInstance(0)
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
          this.fetchTestInstance(0)
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
    this.fetchTestInstance(0)
  }

  onLastClick () {
    this.debug('onLastClick')
    let skip = Math.floor(this.props.state.testinstancelist.totalTestInstance / TEST_INSTANCE_LIMIT) * TEST_INSTANCE_LIMIT
    this.fetchTestInstance(skip)
  }

  onNextClick () {
    this.debug('onNextClick')
    let skip = (this.getCurrentPage() + 1) * TEST_INSTANCE_LIMIT
    this.fetchTestInstance(skip)
  }

  onPreviousClick () {
    this.debug('onPreviousClick')
    let skip = this.props.state.testinstancelist.skip - TEST_INSTANCE_LIMIT
    this.fetchTestInstance(skip)
  }

  getCurrentPage () {
    return this.props.state.testinstancelist.skip / this.props.state.testinstancelist.limit
  }

  fetchTestInstance (skip) {
    this.props.actions.doFetchTestInstance(
      this.props.state.session,
      this.getTestBatchUid(),
      skip,
      TEST_INSTANCE_LIMIT
    )
  }

  getPath () {
    return this.props.location.query['path']
  }

  getTestBatchUid () {
    return this.props.location.query['testbatchuid']
  }

  getTestBatch () {
    return this.props.state.testinstancelist.testBatch
  }

  render () {
    let testinstancelist = this.props.state.testinstancelist
    let path = this.getPath()

    if (testinstancelist.error) {
      return <ErrorMsg msgId={testinstancelist.error} />
    } else if (testinstancelist.testInstanceList === null) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else {
      let testInstances = this.props.state.testinstancelist.testInstanceList
      let totalPage = parseInt(Math.ceil(this.props.state.testinstancelist.totalTestInstance / TEST_INSTANCE_LIMIT))
      let currentPage = this.getCurrentPage()
      let testBatch = this.getTestBatch()

      return (
        <div>
          <h2 className='text-center'>
            Test Instance List <small> ({testBatch.friendly_name}) ({testBatch.uid})</small>
          </h2>
          <ul>
          {(() => {
            return testInstances.map((testInstance, index) => {
              return (
                <li key={index}>
                  <small>
                    <Link className='btn btn-default btn-link' to={path + '?testinstanceuid=' + testInstance.uid}>
                      {testInstance.name}
                      <BrowserBadge
                        browserName={testInstance.browser_capabilities.browserName}
                        browserIcon={testInstance.browser_capabilities.browserName}
                        browserVersion={testInstance.browser_capabilities.version}
                        platform={testInstance.browser_capabilities.platform}
                      />
                    </Link>
                  </small>
                </li>
              )
            })
          })()}
          </ul>
          {(() => {
            if (testBatch.terminated) {
              return (
                <Pager
                  totalPage={totalPage}
                  currentPage={currentPage}
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

module.exports = TestInstanceList
