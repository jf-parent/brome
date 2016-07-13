import React from 'react'
import { Link } from 'react-router'
import { FormattedTime, FormattedDate, FormattedMessage } from 'react-intl'
import moment from 'moment'

import Pager from 'components/ux/Pager'
import ComponentStyle from './ComponentStyle.postcss'
import CoreLayoutStyle from 'layouts/CoreLayout/CoreLayoutStyle.postcss'
import BaseComponent from 'core/BaseComponent'

const TEST_BATCH_LIMIT = 9

class TestBatchList extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'getTestBatchDiv',
      'fetchTestBach',
      'onFirstClick',
      'onPreviousClick',
      'onNextClick',
      'onLastClick',
      'getCurrentPage'
    )
  }

  getCurrentPage () {
    return this.props.state.testbatchlist.skip / this.props.state.testbatchlist.limit
  }

  fetchTestBach (currentPage, loadingContext = true) {
    this.props.actions.loadTestBatch(
      this.props.state.session,
      currentPage,
      TEST_BATCH_LIMIT,
      loadingContext
    )
  }

  componentWillMount () {
    this.fetchTestBach(this.props.state.testbatchlist.skip)
    this._interval = setInterval(
      () => {
        this.fetchTestBach(this.props.state.testbatchlist.skip, false)
      },
      2000
    )
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')
    clearInterval(this._interval)
  }

  onFirstClick () {
    this.debug('onFirstClick')
    this.fetchTestBach(0)
  }

  onLastClick () {
    this.debug('onLastClick')
    let skip = Math.floor(this.props.state.testbatchlist.totalTestBatch / TEST_BATCH_LIMIT) * TEST_BATCH_LIMIT
    this.fetchTestBach(skip)
  }

  onNextClick () {
    this.debug('onNextClick')
    let nextPage = (this.getCurrentPage() + 1) * TEST_BATCH_LIMIT
    this.fetchTestBach(nextPage)
  }

  onPreviousClick () {
    this.debug('onPreviousClick')
    let previousPage = this.props.state.testbatchlist.skip - TEST_BATCH_LIMIT
    this.fetchTestBach(previousPage)
  }

  getTestBatchDiv (testBatch, index) {
    function pad2 (number) {
      return (number < 10 ? '0' : '') + number
    }
    let startingTimestamp = moment(testBatch.starting_timestamp)
    let endingTimestamp
    if (testBatch.ending_timestamp) {
      endingTimestamp = moment(testBatch.ending_timestamp)
    } else {
      endingTimestamp = Date.now()
    }
    let duration = moment.duration(moment(endingTimestamp).diff(startingTimestamp))
    let hours = parseInt(duration.asHours())
    let minutes = parseInt(duration.asMinutes()) - hours * 60
    let seconds = parseInt(duration.asSeconds()) - hours * 60 - minutes * 60
    let runningDuration = pad2(hours) + ':' + pad2(minutes) + ':' + pad2(seconds)
    return (
      <div className='col-xs-12 col-sm-12 col-md-4 col-lg-4'>
        <div className={ComponentStyle['test-batch-container']}>
          <p className='text-center'>
            <Link to={'/testbatchdetail?uid=' + testBatch.uid}>{testBatch.uid}</Link>
          </p>
          <p>
            <small>
              <b>
                <FormattedMessage
                  id='testBatchList.StartedTimestamp'
                  defaultMessage='Started:'
                />
              </b>
              {' '}
              <FormattedDate
                value={startingTimestamp}
                year='numeric'
                month='long'
                day='2-digit'
              />
              {' '}
              <FormattedTime value={startingTimestamp} />
            </small>
          </p>
          {testBatch.ending_timestamp
              ? <div>
                <p>
                  <small>
                    <b>
                      <FormattedMessage
                        id='testBatchList.EndingTimtestamp'
                        defaultMessage='Ended:'
                      />
                    </b>
                    {' '}
                    <FormattedDate
                      value={endingTimestamp}
                      year='numeric'
                      month='long'
                      day='2-digit'
                    />
                    {' '}
                    <FormattedTime value={endingTimestamp} />
                  </small>
                </p>
                <p>
                  <small>
                    <b>
                      <FormattedMessage
                        id='testBatchList.TotalDuration'
                        defaultMessage='Total duration:'
                      />
                    </b>
                    {' '}
                    {runningDuration}
                  </small>
                </p>
              </div>
              : <div>
                <p>
                  <small><i>
                    <FormattedMessage
                      id='testBatchList.IsRunning'
                      defaultMessage='is running...'
                    />
                  </i></small>
                </p>
                <p>
                  <small>
                    <b>
                      <FormattedMessage
                        id='testBatchList.TotalDuration'
                        defaultMessage='Total duration:'
                      />
                    </b>
                    {' '}
                    {runningDuration}
                  </small>
                </p>
              </div>
          }
        </div>
      </div>
    )
  }

  render () {
    let pager = null
    if (this.props.state.testbatchlist.totalTestBatch > TEST_BATCH_LIMIT) {
      let totalPage = parseInt(Math.ceil(this.props.state.testbatchlist.totalTestBatch / TEST_BATCH_LIMIT))
      let currentPage = this.getCurrentPage()
      pager = <Pager totalPage={totalPage} currentPage={currentPage} onFirstClick={this.onFirstClick} onLastClick={this.onLastClick} onNextClick={this.onNextClick} onPreviousClick={this.onPreviousClick} />
    }
    let testBatchList = this.props.state.testbatchlist.testBatchList.map((testBatch, index) => {
      return this.getTestBatchDiv(testBatch, index)
    })
    return (
      <div className='container-fluid'>
        <h1>

          <FormattedMessage
            id='testBatchList.TestBatchListHeader'
            defaultMessage='Test Batch List'
          />
        </h1>
        {pager}
        <div className={'row ' + CoreLayoutStyle['no-gutter']}>
          {testBatchList}
        </div>
        {pager}
      </div>
    )
  }
}

module.exports = TestBatchList
