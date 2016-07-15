import React from 'react'
import axios from 'axios'
// import { FormattedMessage } from 'react-intl'

// import ComponentStyle from './ComponentStyle.postcss'
import BaseComponent from 'core/BaseComponent'

class TestInstanceLog extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind('fetchTestInstanceLog')

    this.state = {
      lines: []
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
            lines: this.state.lines.concat(response.data.results)
          })
          this._interval = setTimeout(
            () => {
              this.fetchTestInstanceLog(testInstanceUid, response.data.total)
            },
            2000
          )
        } else {
          // TODO
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
    let lines = this.state.lines

    return (
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
    )
  }
}

module.exports = TestInstanceLog
