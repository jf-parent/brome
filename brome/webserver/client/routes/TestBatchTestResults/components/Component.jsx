import React from 'react'
import { defineMessages, injectIntl, FormattedMessage } from 'react-intl'
import LaddaButton from 'components/ux/LaddaButton'
import BrowserBadge from 'components/ux/BrowserBadge'
import Collapse, { Panel } from 'rc-collapse'
import 'font-awesome-webpack'
import 'rc-collapse/assets/index.css'
import Select from 'react-select'
import 'react-select/dist/react-select.css'

import Breadcrumbs from 'components/ux/Breadcrumbs'
import VideoPlayer from 'components/ux/VideoPlayer'
import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
// import ComponentStyle from './ComponentStyle.postcss'
import Pager from 'components/ux/Pager'
import BaseComponent from 'core/BaseComponent'

const TEST_RESULT_LIMIT = 10

const testBatchTestResultsMessages = defineMessages({
  filterByPlaceholder: {
    id: 'testBatchTestResults.FilterBy',
    defaultMessage: 'Search (test id)'
  },
  screenshotPlaceholder: {
    id: 'testBatchTestResults.Screenshot',
    defaultMessage: 'Screenshot'
  },
  videoCapturePlaceholder: {
    id: 'testBatchTestResults.VideoCapture',
    defaultMessage: 'Video Capture'
  },
  createdTimestampAscPlaceholder: {
    id: 'testBatchTestResults.CreatedTimestampAsc',
    defaultMessage: 'Created timestamp (asc)'
  },
  createdTimestampDescPlaceholder: {
    id: 'testBatchTestResults.CreatedTimestampDesc',
    defaultMessage: 'Created timestamp (desc)'
  },
  testIdAscPlaceholder: {
    id: 'testBatchTestResults.TestIdAsc',
    defaultMessage: 'Test id (asc)'
  },
  testIdDescPlaceholder: {
    id: 'testBatchTestResults.TestIdDesc',
    defaultMessage: 'Test id (desc)'
  },
  titleAscPlaceholder: {
    id: 'testBatchTestResults.TitleAsc',
    defaultMessage: 'Title (asc)'
  },
  titleDescPlaceholder: {
    id: 'testBatchTestResults.TitleDesc',
    defaultMessage: 'Title (desc)'
  },
  resultAscPlaceholder: {
    id: 'testBatchTestResults.ResultAsc',
    defaultMessage: 'Result (asc)'
  },
  resultDescPlaceholder: {
    id: 'testBatchTestResults.ResultDesc',
    defaultMessage: 'Result (desc)'
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

    if (testid === '') {
      testid = true
    }
    this.fetchTestResults(
      0,
      true,
      testid,
      testbatchtestresults.orderBy
    )
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
      const { formatMessage } = this.props.intl
      const filterByPlaceholder = formatMessage(testBatchTestResultsMessages.filterByPlaceholder)
      const videoCapturePlaceholder = formatMessage(testBatchTestResultsMessages.videoCapturePlaceholder)
      const screenshotPlaceholder = formatMessage(testBatchTestResultsMessages.screenshotPlaceholder)
      const createdTimestampAscPlaceholder = formatMessage(testBatchTestResultsMessages.createdTimestampAscPlaceholder)
      const createdTimestampDescPlaceholder = formatMessage(testBatchTestResultsMessages.createdTimestampAscPlaceholder)
      const testIdAscPlaceholder = formatMessage(testBatchTestResultsMessages.testIdAscPlaceholder)
      const testIdDescPlaceholder = formatMessage(testBatchTestResultsMessages.testIdDescPlaceholder)
      const titleAscPlaceholder = formatMessage(testBatchTestResultsMessages.titleAscPlaceholder)
      const titleDescPlaceholder = formatMessage(testBatchTestResultsMessages.titleDescPlaceholder)
      const resultAscPlaceholder = formatMessage(testBatchTestResultsMessages.resultAscPlaceholder)
      const resultDescPlaceholder = formatMessage(testBatchTestResultsMessages.resultDescPlaceholder)
      let testBatch = testbatchtestresults.testBatch

      // TODO translate
      let orderByOptions = [
        {value: 'created_ts_asc', label: createdTimestampAscPlaceholder},
        {value: 'created_ts_desc', label: createdTimestampDescPlaceholder},
        {value: 'testid_asc', label: testIdAscPlaceholder},
        {value: 'testid_desc', label: testIdDescPlaceholder},
        {value: 'title_asc', label: titleAscPlaceholder},
        {value: 'title_desc', label: titleDescPlaceholder},
        {value: 'result_asc', label: resultAscPlaceholder},
        {value: 'result_desc', label: resultDescPlaceholder}
      ]
      let routes = [
        {
          msgId: 'TestBatchDetail',
          to: '/testbatchdetail?testbatchuid=' + testBatch.uid
        },
        {
          msgId: 'TestBatchTestResults',
          disable: true
        }
      ]

      return (
        <div className='container-fluid'>
          <Breadcrumbs routes={routes} />
          <div className='row'>
            <div className='col-xs-12 col-sm-12 col-md-12 col-lg-12'>
              <h2>
                <FormattedMessage
                  id='testBatchTestResults.TestResults'
                  defaultMessage='Test Results'
                />
                {' '}
                <small>({testBatch.friendly_name}) ({testBatch.uid})</small>
              </h2>
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
                  id='general.Search'
                  defaultMessage='Search'
                />
              </LaddaButton>
            </div>
          </div>
          {(() => {
            let testResults = testbatchtestresults.testResults

            if (testResults.length) {
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
                          <Panel header={screenshotPlaceholder}>
                            {(() => {
                              if (testResult.screenshot_path !== '') {
                                return (
                                  <a href={testResult.screenshot_path} target='_blank'>
                                    <img className='img-responsive' src={testResult.screenshot_path} />
                                  </a>
                                )
                              } else {
                                return (
                                  <small>
                                    <FormattedMessage
                                      id='testBatchTestResults.NoScreenshot'
                                      defaultMessage='No screenshot'
                                    />
                                  </small>
                                )
                              }
                            })()}
                          </Panel>
                          <Panel header={videoCapturePlaceholder}>
                            {(() => {
                              if (testResult.video_capture_path !== '') {
                                return (
                                  <VideoPlayer src={testResult.video_capture_path} currentTime={testResult.video_capture_current_time} />
                                )
                              } else {
                                return (
                                  <small>
                                    <FormattedMessage
                                      id='testBatchTestResults.NoVideoCapture'
                                      defaultMessage='No video capture'
                                    />
                                  </small>
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
            } else {
              return (
                <div className='row' style={{marginBottom: '15px'}}>
                  <div className='col-xs-12 col-sm-12 col-md-3 col-lg-3 col-md-offset-5 col-lg-offset-5'>
                    <h2>
                      <FormattedMessage
                        id='testBatchTestResults.NoTestResult'
                        defaultMessage='No Test Result'
                      />
                    </h2>
                  </div>
                </div>
              )
            }
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

module.exports = injectIntl(TestBatchTestResults)
