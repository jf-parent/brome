import React from 'react'
import { Link } from 'react-router'
import { FormattedMessage } from 'react-intl'

// import ComponentStyle from './ComponentStyle.postcss'
import Breadcrumbs from 'components/ux/Breadcrumbs'
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
      'onSearch',
      'onSearchTextChange',
      'getTestBatch',
      'getPath',
      'getTestBatchUid',
      'fetchTestInstance'
    )

    this.state = {
      searchText: ''
    }
  }

  componentWillMount () {
    this.debug('componentWillUnmount')

    this.fetchTestInstance(0)
  }

  onSearch () {
    this.fetchTestInstance(0)
  }

  onSearchTextChange (event) {
    let searchText = event.target.value

    this.setState({searchText})
  }

  fetchTestInstance (skip) {
    this.props.actions.doFetchTestInstance(
      this.props.state.session,
      this.getTestBatchUid(),
      skip,
      TEST_INSTANCE_LIMIT,
      this.state.searchText
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
      let testBatch = this.getTestBatch()
      let routes = [
        {
          msgId: 'TestBatchDetail',
          to: '/testbatchdetail?testbatchuid=' + testBatch.uid
        },
        {
          msgId: 'TestInstanceList',
          disable: true
        }
      ]

      return (
        <div>
          <Breadcrumbs routes={routes} />
          <h2 className='text-center'>
            Test Instance List <small> ({testBatch.friendly_name}) ({testBatch.uid})</small>
          </h2>
          <div className='row'>
            <div className='col-xs-offset-8'>
              <input placeholder='search' value={this.state.searchText} onChange={this.onSearchTextChange} />
              {' '}
              <button className='btn btn-default btn-xs' onClick={this.onSearch}>
                <FormattedMessage
                  id='general.Search'
                  defaultMessage='Search'
                />
              </button>
            </div>
          </div>
          <ul>
          {(() => {
            return testInstances.map((testInstance, index) => {
              // TODO ellipsis
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
          <Pager
            skippedItem={testinstancelist.skip}
            fetchData={this.fetchTestInstance}
            totalItem={testinstancelist.totalTestInstance}
            itemPerPage={TEST_INSTANCE_LIMIT}
          />
        </div>
      )
    }
  }
}

module.exports = TestInstanceList
