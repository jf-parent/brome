import React from 'react'
// import { FormattedMessage } from 'react-intl'

// import ComponentStyle from './ComponentStyle.postcss'
import BaseComponent from 'core/BaseComponent'

class TestBatchList extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    // this._bind('')
  }

  componentWillMount () {
    debugger
    let data = {
      'actions': {
        'action': 'read',
        'model': 'testbatch'
      },
      'token': this.props.state.session.token
    }
    this.props.actions.loadTestBatch(data)
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')
  }

  render () {
    return (
      <h1>Test Batch</h1>
    )
  }
}

module.exports = TestBatchList
