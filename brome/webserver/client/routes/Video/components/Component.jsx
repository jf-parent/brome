import React from 'react'
import 'react-html5video/src/assets/video.css'
// import { FormattedMessage } from 'react-intl'

// import ComponentStyle from './ComponentStyle.postcss'
import VideoPlayer from 'components/ux/VideoPlayer'
import BaseComponent from 'core/BaseComponent'

class Video extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'getVideoSource'
    )

    this.state = {
      videoSrc: this.getVideoSource()
    }
  }

  getVideoSource () {
    return this.props.location.query['videosrc']
  }

  render () {
    return (
      <VideoPlayer src={this.getVideoSource()} />
    )
  }
}

module.exports = Video
