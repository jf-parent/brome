import React from 'react'
import axios from 'axios'
// import { FormattedMessage } from 'react-intl'

import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
// import ComponentStyle from './ComponentStyle.postcss'
import BaseComponent from 'core/BaseComponent'

class TestBatchRunnerLog extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind('fetchTestBachRunnerLog')

    this.state = {
      lines: [],
      loading: true,
      parent: null,
      error: null,
      name: null
    }
  }

  fetchTestBachRunnerLog (testBatchUid, skip) {
    let data = {
      'model': 'testbatch',
      'uid': testBatchUid,
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
          if (!response.parent.terminated) {
            this._interval = setTimeout(
              () => {
                this.fetchTestBachRunnerLog(testBatchUid, response.data.total)
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
    let testBatchUid = this.props.location.query['testbatchuid']

    this._interval = setTimeout(
      () => {
        this.fetchTestBachRunnerLog(testBatchUid, 0)
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
      return <ErrorMsg msgId={this.state.error} name='error-runner-log' />
    } else {
      let lines = this.state.lines
      let logStyle = {
        border: '2px solid black',
        padding: '4px',
        margin: '4px',
        overflow: 'scroll'
      }

      return (
        <div>
          <h2>Test Batch Log <small>({this.state.parent.friendly_name}) ({this.state.parent.uid})</small></h2>
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

module.exports = TestBatchRunnerLog
