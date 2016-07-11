import React from 'react'
// import { FormattedMessage } from 'react-intl'
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

  getActionToolbelt () {
    if (this.props.state.testbatchdetail.testBatch.terminated) {
      return (
        <div className={'row ' + CoreLayoutStyle['no-gutter']}>
          <div className='pull-right'>
            <a className='btn btn-default btn-link'>
              <i className='fa fa-trash-o' aria-hidden='true'></i>
              {' '}
              Delete
            </a>
          </div>
        </div>
      )
    } else {
      return (
        <div className={'row ' + CoreLayoutStyle['no-gutter']}>
          <div className='pull-right'>
            <a className='btn btn-default btn-link'>
              <i className='fa fa-plug' aria-hidden='true'></i>
              {' '}
              Terminate
            </a>
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
    return (
      <h3>Test Results</h3>
    )
  }

  getCrashes () {
    return (
      <h3>Crashes</h3>
    )
  }

  getMilestone () {
    return (
      <h3>Milestone</h3>
    )
  }

  getTool (path, label, icon, enabled) {
    // TODO fix style issue
    return (
      <div className='col-xs-12 col-sm-12 col-md-2 col-lg-2'>
        <div className={ComponentStyle['feature-box']}>
          <Link className='btn btn-default btn-link' to={path + '?testbatchuid=' + this.props.state.testbatchdetail.testBatch.uid} disabled={!enabled}>
            <i className={'fa fa-' + icon} aria-hidden='true'></i>
            {' '}
            {label}
          </Link>
        </div>
      </div>
    )
  }

  getToolbelt () {
    let testBatchFeatures = this.props.state.testbatchdetail.testBatch.features
    let sessionVideoCapture = this.getTool(
      'sessionvideocapture',
      'Video Capture',
      'television',
      testBatchFeatures['session_video_capture']
    )
    let networkCapture = this.getTool(
      'networkcapture',
      'Network Capture',
      'cubes',
      testBatchFeatures['network_capture']
    )
    let botDiaries = this.getTool(
      'botdiaries',
      'Bot Diaries',
      'pencil',
      testBatchFeatures['bot_diaries']
    )
    let testResults = this.getTool(
      'testresults',
      'Test Results',
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
      'screenshots',
      'Screenshots',
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
      'testinstanceslogs',
      'Instances Logs',
      'newspaper-o',
      true
    )
    let runnerLog = this.getTool(
      'runnerlog',
      'Runner log',
      'file-text-o',
      true
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
      </div>
    )
  }

  fetchTestBachDetail (testBatchUid) {
    this.props.actions.loadTestBatchDetail(
      this.props.state.session,
      testBatchUid
    )
  }

  componentWillMount () {
    let testBatchUid = this.props.location.query['uid']
    this.fetchTestBachDetail(testBatchUid)
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')
  }

  render () {
    let testBatch = this.props.state.testbatchdetail.testBatch

    if (testBatch) {
      return (
        <div className='container-fluid'>
          {this.getActionToolbelt()}
          <p className='text-center'>
            Test Batch Detail <small> ({testBatch.uid})</small>
          </p>
          {this.getProgress()}
          {this.getToolbelt()}
          {this.getTestResults()}
          {this.getCrashes()}
          {this.getMilestone()}
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
