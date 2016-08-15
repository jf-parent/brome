import React from 'react'
import axios from 'axios'
// import { FormattedMessage } from 'react-intl'

// import ComponentStyle from './ComponentStyle.postcss'
import Breadcrumbs from 'components/ux/Breadcrumbs'
import BrowserBadge from 'components/ux/BrowserBadge'
import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
import BaseComponent from 'core/BaseComponent'

class TestInstanceLog extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind('fetchTestInstanceLog')

    this.state = {
      lines: [],
      loading: true,
      error: null,
      parent: null,
      name: null
    }
  }

  fetchTestInstanceLog (testInstanceUid, skip) {
    let data = {
      'model': 'testinstance',
      'uid': testInstanceUid,
      'skip': skip
    }

    axios.post('/api/logstreamout', data)
      .then((response) => {
        this.debug('/api/logstreamout (data) (response)', data, response)

        if (response.data.success) {
          this.setState({
            lines: this.state.lines.concat(response.data.results),
            loading: false,
            parent: response.data.parent,
            name: response.data.name
          })

          if (!response.data.parent.terminated) {
            this._interval = setTimeout(
              () => {
                this.fetchTestInstanceLog(testInstanceUid, response.data.total)
              },
              2000
            )
          }
        } else {
          this.setState({
            loading: false,
            error: response.data.error
          })
        }
      })
  }

  componentWillMount () {
    let testInstanceUid = this.props.location.query['testinstanceuid']

    setTimeout(
      () => {
        this.fetchTestInstanceLog(testInstanceUid, 0)
      }
    )
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')
    clearInterval(this._interval)
  }

  render () {
    if (this.state.loading) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else if (this.state.error) {
      return <ErrorMsg msgId={this.state.error} />
    } else {
      let lines = this.state.lines
      let logStyle = {
        border: '2px solid black',
        padding: '4px',
        margin: '4px',
        overflow: 'scroll'
      }
      let routes = [
        {
          msgId: 'TestBatchDetail',
          to: '/testbatchdetail?testbatchuid=' + this.state.parent.test_batch_id
        },
        {
          msgId: 'TestInstanceList',
          to: 'testinstancelist?path=testinstancelog&testbatchuid=' + this.state.parent.test_batch_id
        },
        {
          msgId: 'TestInstanceLog',
          disable: true
        }
      ]

      let browserBadge = <BrowserBadge
        browserName={this.state.parent.browser_capabilities.browserName}
        browserIcon={this.state.parent.browser_capabilities.browserName}
        browserVersion={this.state.parent.browser_capabilities.version}
        platform={this.state.parent.browser_capabilities.platform}
      />
      return (
        <div>
          <Breadcrumbs routes={routes} />
          <h2>Test Batch Log <small>({this.state.parent.name} - {browserBadge}) ({this.state.parent.test_batch_id})</small></h2>
          <span>
            Log:{' '}
          </span>
          <b>
            {this.state.name}
          </b>
          <div style={logStyle}>
            <ol>
              {(() => {
                return lines.map((line, index) => {
                  return (
                    <li key={index}>
                      <small>
                        <i>{line}</i>
                      </small>
                    </li>
                  )
                })
              })()}
            </ol>
          </div>
        </div>
      )
    }
  }
}

module.exports = TestInstanceLog
