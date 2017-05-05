import React from 'react'
import axios from 'axios'
import 'react-html5video/src/assets/video.css'

// import ComponentStyle from './ComponentStyle.postcss'
import BrowserBadge from 'components/ux/BrowserBadge'
import Breadcrumbs from 'components/ux/Breadcrumbs'
import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
import VideoPlayer from 'components/ux/VideoPlayer'
import BaseComponent from 'core/BaseComponent'

class Video extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()

    this._bind(
      'fetchData'
    )

    this.state = {
      testInstance: null,
      loading: true,
      error: null,
      videoSrc: null
    }
  }

  componentWillMount () {
    let testInstanceUid = this.props.location.query['testinstanceuid']

    this.fetchData(testInstanceUid)
  }

  fetchData (testInstanceUid) {
    let data = {
      token: this.props.state.session.token,
      actions: {
        action: 'read',
        model: 'testinstance',
        uid: testInstanceUid
      }
    }

    axios.post('/api/crud', data)
      .then((response) => {
        this.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          this.setState({
            testInstance: response.data.results[0],
            loading: false,
            videoSrc: response.data.results[0].video_capture_path
          })
        } else {
          this.setState({
            loading: false,
            error: response.data.error
          })
        }
      })
  }

  render () {
    if (this.state.loading) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else if (this.state.error) {
      return <ErrorMsg msgId={this.state.error} />
    } else {
      let testBatchUid = this.state.testInstance.test_batch_id
      let routes = [
        {
          msgId: 'TestBatchDetail',
          to: '/testbatchdetail?testbatchuid=' + testBatchUid
        },
        {
          msgId: 'TestInstanceList',
          to: 'testinstancelist?path=testinstancevideo&testbatchuid=' + testBatchUid
        },
        {
          msgId: 'TestInstanceVideo',
          disable: true
        }
      ]

      let browserBadge = <BrowserBadge
        browserName={this.state.testInstance.browser_capabilities.browserName}
        browserIcon={this.state.testInstance.browser_capabilities.browserName}
        browserVersion={this.state.testInstance.browser_capabilities.version}
        platform={this.state.testInstance.browser_capabilities.platform}
      />
      return (
        <div className='container-fluid'>
          <Breadcrumbs routes={routes} />
          <div className='row'>
            <h2>{this.state.testInstance.name} <small>({browserBadge} - {this.state.testInstance.test_batch_id})</small></h2>
          </div>
          <div className='row'>
            <VideoPlayer src={this.state.videoSrc} />
          </div>
        </div>
      )
    }
  }
}

module.exports = Video
