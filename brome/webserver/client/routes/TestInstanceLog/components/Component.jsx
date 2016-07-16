import React from 'react'
import axios from 'axios'
// import { FormattedMessage } from 'react-intl'

// import ComponentStyle from './ComponentStyle.postcss'
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
            name: response.data.name
          })
          // TODO don't setTimeout if the log is not alive
          this._interval = setTimeout(
            () => {
              this.fetchTestInstanceLog(testInstanceUid, response.data.total)
            },
            2000
          )
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
      return <Loading />
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
                        {line}
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
