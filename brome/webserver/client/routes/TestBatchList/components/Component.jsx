import React from 'react'
import { Link } from 'react-router'
import { FormattedTime, FormattedDate, FormattedMessage } from 'react-intl'
import moment from 'moment'

import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
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
      'fetchTestBatch'
    )
  }

  fetchTestBatch (skip) {
    this.props.actions.doLoadTestBatchList(
      this.props.state.session,
      skip,
      TEST_BATCH_LIMIT
    )
  }

  componentWillMount () {
    this.fetchTestBatch(this.props.state.testbatchlist.skip)
    this._interval = setInterval(
      () => {
        this.fetchTestBatch(this.props.state.testbatchlist.skip, false)
      },
      2000
    )
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')
    clearInterval(this._interval)
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
      <div key={index} className='col-xs-12 col-sm-12 col-md-4 col-lg-4'>
        <div className={ComponentStyle['test-batch-container']}>
          <p className='text-center'>
            <small>{testBatch.friendly_name}</small>
          </p>
          <p className='text-center'>
            <Link to={'/testbatchdetail?testbatchuid=' + testBatch.uid}>{testBatch.uid}</Link>
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
    let testbatchlist = this.props.state.testbatchlist

    if (testbatchlist.error) {
      return <ErrorMsg msgId={testbatchlist.error} />
    } else if (testbatchlist.testBatchList === null) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else {
      return (
        <div className='container-fluid'>
          {(() => {
            if (testbatchlist.testBatchList.length) {
              let list = testbatchlist.testBatchList.map((testBatch, index) => {
                return this.getTestBatchDiv(testBatch, index)
              })
              return (
                <div>
                  <h1>
                    <FormattedMessage
                      id='testBatchList.TestBatchListHeader'
                      defaultMessage='Test Batch List'
                    />
                  </h1>
                  <div className={'row ' + CoreLayoutStyle['no-gutter']}>
                    {list}
                  </div>
                </div>
              )
            } else {
              return (
                <div>
                  <div className={'row ' + CoreLayoutStyle['no-gutter']}>
                    <div className='col-xs-1 col-sm-1 col-md-8 col-lg-8 col-md-offset-2 col-lg-offset-2'>
                      <h1>
                        <FormattedMessage
                          id='testBatchList.EmptyTestBatchList'
                          defaultMessage='There is no test batch:/'
                        />
                      </h1>
                    </div>
                  </div>
                  <div className={'row ' + CoreLayoutStyle['no-gutter']}>
                    <div className='col-xs-1 col-sm-1 col-md-2 col-lg-2 col-md-offset-5 col-lg-offset-5'>
                      <Link className='btn btn-default' to='/starttestbatch'>
                        <FormattedMessage
                          id='testBatchList.StartNewTestBatch'
                          defaultMessage='Start Test A New Batch'
                        />
                      </Link>
                    </div>
                  </div>
                </div>
              )
            }
          })()}
          <Pager
            skippedItem={testbatchlist.skip}
            fetchData={this.fetchTestBatch}
            totalItem={testbatchlist.totalTestBatch}
            itemPerPage={TEST_BATCH_LIMIT}
          />
        </div>
      )
    }
  }
}

module.exports = TestBatchList
