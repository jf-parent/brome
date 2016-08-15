import React from 'react'
import { FormattedMessage, defineMessages } from 'react-intl'
import LaddaButton from 'components/ux/LaddaButton'
import BrowserBadge from 'components/ux/BrowserBadge'
import Collapse, { Panel } from 'rc-collapse'
import 'font-awesome-webpack'
import 'rc-collapse/assets/index.css'
import Select from 'react-select'
import 'react-select/dist/react-select.css'

import VideoPlayer from 'components/ux/VideoPlayer'
import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
// import ComponentStyle from './ComponentStyle.postcss'
import Pager from 'components/ux/Pager'
import BaseComponent from 'core/BaseComponent'

const TEST_RESULT_LIMIT = 10

const testBatchTestResultsMessages = defineMessages({
  filterByPlaceholder: {
    id: 'testbatchtestresults.FilterBy',
    defaultMessage: 'Search (test id)'
  }
})

class TestBatchTestResults extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'fetchTestResults',
      'onSearch',
      'onChangeOrderBy',
      'getTestBatchUid'
    )
  }

  componentWillMount () {
    this.fetchTestResults(this.props.state.testbatchtestresults.skip, true)
    this._interval = setInterval(
      () => {
        this.fetchTestResults(this.props.state.testbatchtestresults.skip, false)
      },
      2000
    )

    // TODO add orderBy and filterBy url params
  }

  componentWillReceiveProps () {
    let testbatchtestresults = this.props.state.testbatchtestresults

    // Clear interval on terminated testbatch
    if (testbatchtestresults.testBatch) {
      if (testbatchtestresults.testBatch.terminated) {
        if (this._interval) {
          clearInterval(this._interval)
          this._interval = null
        }
      }
    }
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')
    clearInterval(this._interval)
  }

  onSearch (event) {
    event.preventDefault()
    let testid = this.refs.inputFilterBy.value
    let testbatchtestresults = this.props.state.testbatchtestresults

    if (testid) {
      this.fetchTestResults(
        0,
        true,
        testid,
        testbatchtestresults.orderBy
      )
    }
  }

  onChangeOrderBy (orderBy) {
    let testbatchtestresults = this.props.state.testbatchtestresults
    let effectiveOrderBy = 'clear'

    if (orderBy) {
      effectiveOrderBy = orderBy.value
    }

    this.fetchTestResults(
      0,
      true,
      testbatchtestresults.filterBy,
      effectiveOrderBy
    )
  }

  getTestBatchUid () {
    return this.props.location.query['testbatchuid']
  }

  fetchTestResults (skip, loading = false, filterBy = null, orderBy = null) {
    let testbatchtestresults = this.props.state.testbatchtestresults

    this.props.actions.doLoadTestResults(
      this.props.state.session,
      this.getTestBatchUid(),
      skip,
      TEST_RESULT_LIMIT,
      loading,
      filterBy || testbatchtestresults.filterBy,
      orderBy || testbatchtestresults.orderBy,
    )
  }

  render () {
    let testbatchtestresults = this.props.state.testbatchtestresults

    if (testbatchtestresults.loading) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else if (testbatchtestresults.error) {
      return <ErrorMsg msgId={testbatchtestresults.error} name='error-test-batch-test-results' />
    } else {
      const { formatMessage } = this._reactInternalInstance._context.intl
      const filterByPlaceholder = formatMessage(testBatchTestResultsMessages.filterByPlaceholder)
      let testBatch = testbatchtestresults.testBatch

      // TODO translate
      let orderByOptions = [
        {value: 'created_ts_asc', label: 'Created timestamp (asc)'},
        {value: 'created_ts_desc', label: 'Created timestamp (desc)'},
        {value: 'testid_asc', label: 'Test id (asc)'},
        {value: 'testid_desc', label: 'Test id (desc)'},
        {value: 'title_asc', label: 'Title (asc)'},
        {value: 'title_desc', label: 'Title (desc)'},
        {value: 'result_asc', label: 'Result (asc)'},
        {value: 'result_desc', label: 'Result (desc)'}
      ]

      return (
        <div className='container-fluid'>
          <div className='row'>
            <div className='col-xs-12 col-sm-12 col-md-12 col-lg-12'>
              <h2>Test Results <small>({testBatch.friendly_name}) ({testBatch.uid})</small></h2>
            </div>
          </div>
          <div className='row' style={{marginBottom: '15px'}}>
            <div className='col-xs-12 col-sm-12 col-md-3 col-lg-3'>
              <Select
                placeholder='OrderBy'
                name='orderBy'
                value={testbatchtestresults.orderBy}
                options={orderByOptions}
                onChange={this.onChangeOrderBy}
              />
            </div>
            <div className='col-xs-12 col-sm-12 col-md-3 col-lg-3'>
              <input className='form-control' ref='inputFilterBy' placeholder={filterByPlaceholder} required defaultValue={testbatchtestresults.filterBy} />
            </div>
            <div className='col-xs-12 col-sm-12 col-md-2 col-lg-2'>
              <LaddaButton ref='searchButton' btnClass='btn btn-md btn-primary btn-block' isLoading={testbatchtestresults.loading} onSubmit={this.onSearch}>
                <i className='fa fa-search' aria-hidden='true'></i>
                {' '}
                <FormattedMessage
                  id='testBatchTestResults.Search'
                  defaultMessage='Search'
                />
              </LaddaButton>
            </div>
          </div>
          {(() => {
            let testResults = testbatchtestresults.testResults

            return testResults.map((testResult, index) => {
              let headerStyle = {}
              let headerIcon = null
              if (testResult.result) {
                headerStyle['color'] = 'green'
                headerIcon = 'fa-thumbs-up'
              } else {
                headerStyle['color'] = 'red'
                headerIcon = 'fa-thumbs-down'
              }
              let header = <div style={{top: '-40px'}} className='text-ellipsis'>
                <i className={'fa ' + headerIcon} style={headerStyle} aria-hidden='true'></i>
                {' '}
                {testResult.testid}
                {' '}
                {testResult.title}
                <BrowserBadge
                  browserName={testResult.browser_capabilities.browserName}
                  browserVersion={testResult.browser_capabilities.version}
                  browserIcon={testResult.browser_capabilities.browserName}
                  platform={testResult.browser_capabilities.platform}
                />
              </div>
              return (
                <div className='row' key={index}>
                  <Collapse accordion>
                    <Panel header={header} key={index}>
                      <Collapse accordion>
                        <Panel header='Screenshot'>
                          {(() => {
                            if (testResult.screenshot_path !== '') {
                              return (
                                <a href={testResult.screenshot_path} target='_blank'>
                                  <img className='img-responsive' src={testResult.screenshot_path} />
                                </a>
                              )
                            } else {
                              return (
                                <small>No screenshot</small>
                              )
                            }
                          })()}
                        </Panel>
                        <Panel header='Video Capture'>
                          {(() => {
                            if (testResult.video_capture_path !== '') {
                              return (
                                <VideoPlayer src={testResult.video_capture_path} currentTime={testResult.video_capture_current_time} />
                              )
                            } else {
                              return (
                                <small>No video capture</small>
                              )
                            }
                          })()}
                        </Panel>
                      </Collapse>
                    </Panel>
                  </Collapse>
                </div>
              )
            })
          })()}
          <Pager
            skippedItem={testbatchtestresults.skip}
            fetchData={this.fetchTestResults}
            totalItem={testbatchtestresults.totalTestResults}
            itemPerPage={TEST_RESULT_LIMIT}
          />
        </div>
      )
    }
  }
}

module.exports = TestBatchTestResults
