import React, { Component, PropTypes } from 'react'
import Video from 'react-html5video'
import 'react-html5video/src/assets/video.css'

const SUPPORTED_VIDEO_TYPE = [
  'mp4',
  'webm',
  'ogg'
]

class VideoPlayer extends Component {

  constructor (props) {
    super(props)

    this.onReady = this.onReady.bind(this)
  }

  static propTypes = {
    src: PropTypes.string.isRequired,
    currentTime: PropTypes.number
  }

  static defaultProps = {
    currentTime: 0
  }

  getVideoType () {
    let videoSrc = this.props.src
    let videoType = videoSrc.substr(videoSrc.lastIndexOf('.') + 1)

    if (!SUPPORTED_VIDEO_TYPE.includes(videoType)) {
      throw new Error('Unsupported video type: ' + videoType)
    }

    return videoType
  }

  onReady () {
    if (this.props.currentTime) {
      this.refs.video.seek(this.props.currentTime)
    }
  }

  render () {
    return (
      <div className='embed-responsive embed-responsive-16by9'>
        <Video
          ref='video'
          className='embed-responsive-item'
          controls
          muted
          onLoadStart={this.onReady}
        >
          <source src={this.props.src} type={'video/' + this.getVideoType()} />
        </Video>
      </div>
    )
  }
}

module.exports = VideoPlayer
