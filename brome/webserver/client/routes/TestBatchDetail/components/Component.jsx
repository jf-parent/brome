import React from 'react'
import { FormattedMessage } from 'react-intl'
import { Link } from 'react-router'
import 'font-awesome-webpack'
import { Line } from 'rc-progress'

import Loading from 'components/ux/Loading'
import ComponentStyle from './ComponentStyle.postcss'
import CoreLayoutStyle from 'layouts/CoreLayout/CoreLayoutStyle.postcss'
import BaseComponent from 'core/BaseComponent'

class TestBatchDetail extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'fetchTestBachDetail',
      'getToolbelt',
      'getTool',
      'getActionToolbelt',
      'getProgress',
      'getTestResults',
      'getCrashes',
      'getMilestone'
    )
  }

  componentWillMount () {
    let testBatchUid = this.props.location.query['testbatchuid']

    this._interval = setInterval(
      () => {
        this.fetchTestBachDetail(testBatchUid)
      },
      2000
    )
  }

  componentWillReceiveProps () {
    let testBatch = this.props.state.testbatchdetail.testBatch

    // Clear interval on terminated testbatch
    if (testBatch) {
      if (testBatch.terminated) {
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

  getActionToolbelt () {
    if (this.props.state.testbatchdetail.testBatch.terminated) {
      return (
        <div className={'row ' + CoreLayoutStyle['no-gutter']}>
          <div className='pull-right'>
            <button className='btn btn-default'>
              <i className='fa fa-trash-o' aria-hidden='true'></i>
              {' '}
              Delete
            </button>
          </div>
        </div>
      )
    } else {
      return (
        <div className={'row ' + CoreLayoutStyle['no-gutter']}>
          <div className='pull-right'>
            <button className='btn btn-default'>
              <i className='fa fa-plug' aria-hidden='true'></i>
              {' '}
              Terminate
            </button>
          </div>
        </div>
      )
    }
  }

  getProgress () {
    if (this.props.state.testbatchdetail.testBatch.terminated) {
      return null
    } else {
      let testBatch = this.props.state.testbatchdetail.testBatch
      let totalTests = testBatch.total_tests
      let totalExecutingTests = testBatch.total_executing_tests
      let totalExecutedTests = testBatch.total_executed_tests
      let percent = parseInt(
        (totalExecutedTests / totalTests) * 100
      )
      return (
        <center>
          <span>
            <small>
              Total Tests: <b>{totalTests}</b> ~ {' '}
            </small>
          </span>
          <span>
            <small>
              Total Executed Tests: <b>{totalExecutedTests}</b> ~ {' '}
            </small>
          </span>
          <span>
            <small>
              Total Executing Tests: <b>{totalExecutingTests}</b>
            </small>
          </span>
          <Line percent={percent} strokeWidth='2' strokeColor='#87D0E8' />
        </center>
      )
    }
  }

  getTestResults () {
    let testResults = this.props.state.testbatchdetail.testBatch.test_results
    let nbFailedTest = testResults['nb_failed_test']
    let nbSucceededTest = testResults['nb_succeeded_test']
    let failedTests = testResults['failed_tests']
    return (
      <div>
        <h3 className={ComponentStyle['section-header']}>
          Test Results
          {' '}
          {(() => {
            if (nbFailedTest) {
              return (<span style={{color: 'red'}}>({nbFailedTest})</span>)
            } else {
              return null
            }
          })()}
          {' '}
          {(() => {
            if (nbSucceededTest) {
              return (<span style={{color: 'green'}}>({nbSucceededTest})</span>)
            } else {
              return null
            }
          })()}
        </h3>
        <ul>
          {(() => {
            return failedTests.map((value, index) => {
              return (
                <li key={index}>
                  <small>
                    {value.title}
                  </small>
                </li>
              )
            })
          })()}
        </ul>
      </div>
    )
  }

  getCrashes () {
    let testCrashes = this.props.state.testbatchdetail.testBatch.test_crashes
    let nbOfCrashes = testCrashes.length || 0
    let nbOfCrashesStyle = {color: 'green'}
    if (nbOfCrashes) {
      nbOfCrashesStyle = {color: 'red'}
    }
    return (
      <div>
        <h3 className={ComponentStyle['section-header']}>
          Crashes (<span style={nbOfCrashesStyle}>{nbOfCrashes}</span>):
        </h3>
        <ul>
          {
            testCrashes.map((value, index) => {
              return (
                <li key={index}>
                  <small>{value['title']}</small>
                </li>
              )
            })
          }
        </ul>
      </div>
    )
  }

  getMilestone () {
    let runnerMetadata = this.props.state.testbatchdetail.testBatch.runner_metadata
    return (
      <div>
        <h3 className={ComponentStyle['section-header']}>
          Milestone:
        </h3>
        <ul>
          {(() => {
            if (Object.keys(runnerMetadata).length) {
              return Object.keys(runnerMetadata).map((key, index) => {
                return (
                  <li>
                    <small>
                      <FormattedMessage
                        id={'testBatchDetail.' + key}
                        defaultMessage={key}
                      />
                    </small>
                  </li>
                )
              })
            } else {
              return (
                <li>
                  <small>
                    No milestone
                  </small>
                </li>
              )
            }
          })()}
        </ul>
      </div>
    )
  }

  getTool (
    path,
    label,
    icon,
    enabled,
    className = 'col-xs-12 col-sm-12 col-md-2 col-lg-2'
  ) {
    return (
      <div className={className}>
        <Link className='btn btn-default btn-link' to={path + '?testbatchuid=' + this.props.state.testbatchdetail.testBatch.uid} disabled={!enabled}>
          <i className={'fa fa-' + icon} aria-hidden='true'></i>
          {' '}
          {label}
        </Link>
      </div>
    )
  }

  getToolbelt () {
    let testBatchFeatures = this.props.state.testbatchdetail.testBatch.features
    let sessionVideoCapture = this.getTool(
      'sessionvideocapture',
      'Video Capture',
      'video-camera',
      testBatchFeatures['session_video_capture']
    )
    let networkCapture = this.getTool(
      'networkcapture',
      'Network Capture',
      'cubes',
      testBatchFeatures['network_capture']
    )
    let testResults = this.getTool(
      'testresults',
      'Test Results (' + this.props.state.testbatchdetail.testBatch.test_results.nb_test_result + ')',
      'bar-chart',
      true
    )
    let testInstances = this.getTool(
      'testinstances',
      'Test Instances',
      'list',
      true
    )
    let screenshots = this.getTool(
      'testbatchscreenshots',
      'Screenshots (' + this.props.state.testbatchdetail.testBatch.nb_screenshot + ')',
      'file-image-o',
      testBatchFeatures['screenshots']
    )
    let crashReports = this.getTool(
      'crashreports',
      'Crash reports',
      'exclamation-triangle',
      true
    )
    let testInstancesLogs = this.getTool(
      'testinstanceloglist',
      'Instances Logs',
      'newspaper-o',
      true
    )
    let runnerLog = this.getTool(
      'testbatchrunnerlog',
      'Runner log',
      'file-text-o',
      true
    )
    let botDiaries = this.getTool(
      'botdiaries',
      'Bot Diaries',
      'pencil',
      testBatchFeatures['bot_diaries']
    )
    let instanceVnc = this.getTool(
      'instancevnc',
      'Instance VNC',
      'desktop',
      testBatchFeatures['instance_vnc']
    )
    let styleQuality = this.getTool(
      'stylequality',
      'Style Quality',
      'eye',
      testBatchFeatures['style_quality']
    )
    return (
      <div className={'row ' + CoreLayoutStyle['no-gutter']}>
        {testResults}
        {crashReports}
        {runnerLog}
        {testInstancesLogs}
        {testInstances}
        {sessionVideoCapture}
        {screenshots}
        {networkCapture}
        {botDiaries}
        {instanceVnc}
        {styleQuality}
      </div>
    )
  }

  fetchTestBachDetail (testBatchUid) {
    this.props.actions.loadTestBatchDetail(
      this.props.state.session,
      testBatchUid
    )
  }

  render () {
    let testBatch = this.props.state.testbatchdetail.testBatch

    if (testBatch) {
      return (
        <div className='container-fluid'>
          {this.getActionToolbelt()}
          <h2 className='text-center'>
            Test Batch Detail <small> ({testBatch.uid})</small>
          </h2>
          {this.getProgress()}
          {this.getToolbelt()}
          {this.getTestResults()}
          {this.getMilestone()}
          {this.getCrashes()}
        </div>
      )
    } else {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    }
  }
}

module.exports = TestBatchDetail
