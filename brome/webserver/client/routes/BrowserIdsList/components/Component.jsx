import React from 'react'
import { Link } from 'react-router'
// import { FormattedMessage } from 'react-intl'

// import ComponentStyle from './ComponentStyle.postcss'
import Breadcrumbs from 'components/ux/Breadcrumbs'
import BrowserBadge from 'components/ux/BrowserBadge'
import ErrorMsg from 'components/ux/ErrorMsg'
import Pager from 'components/ux/Pager'
import Loading from 'components/ux/Loading'
import BaseComponent from 'core/BaseComponent'

const BROWSER_IDS_LIMIT = 10

class BrowserIdsList extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'getPath',
      'getTestBatchUid',
      'getTestBatch',
      'fetchBrowserIds'
    )
  }

  componentWillMount () {
    this.debug('componentWillUnmount')

    this.fetchBrowserIds(0)
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
          this.fetchBrowserIds(0)
        },
        2000)
      }
    }
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')

    clearInterval(this._interval)
  }

  fetchBrowserIds (skip) {
    let data = {
      token: this.props.state.session.token,
      actions: {
        action: 'read',
        uid: this.getTestBatchUid(),
        skip: skip,
        limit: BROWSER_IDS_LIMIT,
        model: 'testbatch'
      }
    }

    this.props.actions.doFetchBrowserIds(
      data,
      skip,
      BROWSER_IDS_LIMIT
    )
  }

  getPath () {
    return this.props.location.query['path']
  }

  getTestBatchUid () {
    return this.props.location.query['testbatchuid']
  }

  getTestBatch () {
    return this.props.state.browseridslist.testBatch
  }

  render () {
    let browseridslist = this.props.state.browseridslist
    let path = this.getPath()

    if (browseridslist.error) {
      return <ErrorMsg msgId={browseridslist.error} />
    } else if (browseridslist.loading) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else {
      let browserIdsList = browseridslist.browserIdsList
      let testBatch = this.getTestBatch()
      let routes = [
        {
          msgId: 'TestBatchDetail',
          to: '/testbatchdetail?testbatchuid=' + testBatch.uid
        },
        {
          msgId: 'BrowserIdsList',
          disable: true
        }
      ]

      return (
        <div>
          <Breadcrumbs routes={routes} />
          <h2 className='text-center'>
            Browser Ids List <small> ({testBatch.friendly_name}) ({testBatch.uid})</small>
          </h2>
          <ul>
          {(() => {
            return browserIdsList.map((browserId, index) => {
              return (
                <li key={index}>
                  <small>
                    <Link
                      className='btn btn-default btn-link'
                      to={
                        path +
                        '?browserId=' + browserId.id +
                        '&browserName=' + browserId.capabilities.browserName +
                        '&browserIcon=' + browserId.capabilities.browserName +
                        '&browserVersion=' + browserId.capabilities.version +
                        '&platform=' + browserId.capabilities.platform +
                        '&testbatchuid=' + testBatch.uid
                      }
                    >
                      <BrowserBadge
                        browserName={browserId.capabilities.browserName}
                        browserIcon={browserId.capabilities.browserName}
                        browserVersion={browserId.capabilities.version}
                        platform={browserId.capabilities.platform}
                      />
                    </Link>
                  </small>
                </li>
              )
            })
          })()}
          </ul>
          <Pager
            skippedItem={browseridslist.skip}
            fetchData={this.fetchBrowserIds}
            totalItem={browseridslist.totalBrowserIds}
            itemPerPage={BROWSER_IDS_LIMIT}
          />
        </div>
      )
    }
  }
}

module.exports = BrowserIdsList
