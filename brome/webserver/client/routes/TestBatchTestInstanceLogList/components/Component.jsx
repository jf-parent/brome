import React from 'react'
import { Link } from 'react-router'
// import { FormattedMessage } from 'react-intl'

// import ComponentStyle from './ComponentStyle.postcss'
import Pager from 'components/ux/Pager'
import Loading from 'components/ux/Loading'
import BaseComponent from 'core/BaseComponent'

const TEST_INSTANCE_LIMIT = 10

class TestBatchTestInstanceLogList extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'onFirstClick',
      'onPreviousClick',
      'onNextClick',
      'onLastClick',
      'getCurrentPage'
    )
  }

  onFirstClick () {
    this.debug('onFirstClick')
    this.fetchTestInstance(0)
  }

  onLastClick () {
    this.debug('onLastClick')
    let skip = Math.floor(this.props.state.testbatchtestinstanceloglist.totalTestInstance / TEST_INSTANCE_LIMIT) * TEST_INSTANCE_LIMIT
    this.fetchTestInstance(skip)
  }

  onNextClick () {
    this.debug('onNextClick')
    let skip = (this.getCurrentPage() + 1) * TEST_INSTANCE_LIMIT
    this.fetchTestInstance(skip)
  }

  onPreviousClick () {
    this.debug('onPreviousClick')
    let skip = this.props.state.testbatchtestinstanceloglist.skip - TEST_INSTANCE_LIMIT
    this.fetchTestInstance(skip)
  }

  getCurrentPage () {
    return this.props.state.testbatchtestinstanceloglist.skip / this.props.state.testbatchtestinstanceloglist.limit
  }

  fetchTestInstance (pageg) {
    let testBatchUid = this.props.location.query['testbatchuid']
    let data = {
      'method': 'list_test_instances',
      'uid': testBatchUid,
      'limit': 10,
      'skip': 0
    }
    this.props.actions.doFetchTestInstance(data)
  }

  componentWillMount () {
    this.debug('componentWillUnmount')

    this.fetchTestInstance(0)
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')
  }

  render () {
    let loading = this.props.state.testbatchtestinstanceloglist.loading

    if (loading) {
      return <Loading />
    } else {
      let testInstances = this.props.state.testbatchtestinstanceloglist.testInstanceList
      let totalPage = parseInt(Math.ceil(this.props.state.testbatchtestinstanceloglist.totalTestInstance / TEST_INSTANCE_LIMIT))
      let currentPage = this.getCurrentPage()
      return (
        <div>
          <h2>
            Test Instance Log
          </h2>
          <ul>
          {(() => {
            return testInstances.map((value, index) => {
              return (
                <li key={index}>
                  <small>
                    <Link className='btn btn-default btn-link' to={'testinstancelog?testinstanceuid=' + value.uid}>
                      {value.name}
                    </Link>
                  </small>
                </li>
              )
            })
          })()}
          </ul>
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

module.exports = TestBatchTestInstanceLogList
