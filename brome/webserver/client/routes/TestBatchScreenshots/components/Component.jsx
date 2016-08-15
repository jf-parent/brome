import React from 'react'
// import { FormattedMessage } from 'react-intl'
import ImageGallery from 'react-image-gallery'
import 'react-image-gallery/build/image-gallery.css'

import Breadcrumbs from 'components/ux/Breadcrumbs'
import BrowserBadge from 'components/ux/BrowserBadge'
import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
import ComponentStyle from './ComponentStyle.postcss'
import BaseComponent from 'core/BaseComponent'

class TestBatchScreenshots extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'getBrowserId',
      'getBrowserIcon',
      'getBrowserName',
      'getBrowserVersion',
      'getPlatform',
      'fetchScreenshots',
      'fullScreen',
      'playSlider',
      'pauseSlider',
      'handleInputChange',
      'handleCheckboxChange'
    )

    this.state = {
      isPlaying: false,
      infinite: true,
      showIndex: true,
      slideOnThumbnailHover: false,
      showBullets: true,
      showThumbnails: true,
      showNav: true,
      slideInterval: 2000,
      fullscreen: false
    }
  }

  componentWillMount () {
    let testBatchUid = this.props.location.query['testbatchuid']

    // TODO set interval
    this.fetchScreenshots(testBatchUid)
  }

  componentWillUnmount () {
    this.debug('componentWillUnmount')
  }

  fetchScreenshots (testBatchUid) {
    let browserId = this.getBrowserId()
    let data = {
      token: this.props.state.session.token,
      actions: [
        {
          action: 'read',
          model: 'testscreenshot',
          filters: {
            test_batch_id: testBatchUid,
            browser_id: browserId
          }
        }, {
          action: 'read',
          model: 'testbatch',
          uid: testBatchUid
        }
      ]
    }

    this.props.actions.doFetchScreenshots(data)
  }

  getBrowserId () {
    return this.props.location.query['browserId']
  }

  getBrowserName () {
    return this.props.location.query['browserName']
  }

  getBrowserIcon () {
    return this.props.location.query['browserIcon']
  }

  getBrowserVersion () {
    return this.props.location.query['browserVersion']
  }

  getPlatform () {
    return this.props.location.query['platform']
  }

  pauseSlider () {
    this.refs.imageGallery.pause()
    this.setState({isPlaying: false})
  }

  playSlider () {
    this.refs.imageGallery.play()
    this.setState({isPlaying: true})
  }

  fullScreen () {
    this.refs.imageGallery.fullScreen()
  }

  onImageClick () {
    this.debug('onImageClick')
  }

  onImageLoad () {
    this.debug('onImageLoad')
  }

  onSlide () {
    this.debug('onSlide')
  }

  onPause () {
    this.debug('onPause')
  }

  onPlay () {
    this.debug('onPlay')
  }

  handleInputChange (event) {
    this.setState({[event.target.dataset.action]: event.target.value})
  }

  handleCheckboxChange (event) {
    this.setState({[event.target.dataset.action]: event.target.checked})
  }

  render () {
    let testBatchScreenshots = this.props.state.testbatchscreenshots

    if (testBatchScreenshots.loading) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else if (testBatchScreenshots.error) {
      return <ErrorMsg msgId={testBatchScreenshots.error} />
    } else {
      let items = []
      testBatchScreenshots.screenshots.map((value, index) => {
        items.push({
          original: value.file_path,
          description: value.title,
          thumbnail: value.file_path
        })
      })
      let routes = [
        {
          msgId: 'TestBatchDetail',
          to: '/testbatchdetail?testbatchuid=' + testBatchScreenshots.testBatch.uid
        },
        {
          msgId: 'BrowserIdsList',
          to: '/browseridslist?path=testbatchscreenshots&testbatchuid=' + testBatchScreenshots.testBatch.uid
        },
        {
          msgId: 'TestBatchScreenshots',
          disable: true
        }
      ]

      return (
        <div className='container-fluid'>
          <Breadcrumbs routes={routes} />
          <h2>
            Test Batch Screenshots
            {' - '}
            <small>
              ({testBatchScreenshots.testBatch.friendly_name}) ({testBatchScreenshots.testBatch.uid})
            </small>
            {' - '}
            <small>
              <BrowserBadge
                browserName={this.getBrowserName()}
                browserIcon={this.getBrowserIcon()}
                browserVersion={this.getBrowserVersion()}
                platform={this.getPlatform()}
              />
            </small>
          </h2>
          <ImageGallery
            ref='imageGallery'
            items={items}
            lazyLoad={false}
            infinite={this.state.infinite}
            showBullets={this.state.showBullets}
            showThumbnails={this.state.showThumbnails}
            showIndex={this.state.showIndex}
            showNav={this.state.showNav}
            slideInterval={parseInt(this.state.slideInterval)}
            autoPlay={this.state.isPlaying}
            slideOnThumbnailHover={this.state.slideOnThumbnailHover}
          />
          <ul className={'nav nav-pills ' + ComponentStyle['toolbox']}>
            <li>
              <button
                className={'btn ' + (this.state.isPlaying ? 'btn-primary' : 'btn-default')}
                onClick={this.playSlider}>
                Play
              </button>
            </li>
            <li>
              <button
                className={'btn ' + (!this.state.isPlaying ? 'btn-primary' : 'btn-default')}
                onClick={this.pauseSlider}>
                Pause
              </button>
            </li>
            <li>
              <button
                className='btn btn-default'
                onClick={this.fullScreen}>
                Full Screen
              </button>
            </li>
          </ul>
          <div>
            <ul className='list-unstyled'>
              <li>
                <div className='checkbox'>
                  <label>
                    <input
                      id='infinite'
                      type='checkbox'
                      data-action='infinite'
                      onChange={this.handleCheckboxChange}
                      checked={this.state.infinite}
                    />
                    Infinite sliding
                  </label>
                </div>
              </li>
              <li>
                <div className='checkbox'>
                  <label>
                    <input
                      id='show_bullets'
                      data-action='showBullets'
                      type='checkbox'
                      onChange={this.handleCheckboxChange}
                      checked={this.state.showBullets}
                    />
                    Show bullets
                  </label>
                </div>
              </li>
              <li>
                <div className='checkbox'>
                  <label>
                    <input
                      id='show_thumbnails'
                      type='checkbox'
                      data-action='showThumbnails'
                      onChange={this.handleCheckboxChange}
                      checked={this.state.showThumbnails}
                    />
                    Show thumbnails
                  </label>
                </div>
              </li>
              <li>
                <div className='checkbox'>
                  <label>
                    <input
                      id='show_navigation'
                      type='checkbox'
                      data-action='showNav'
                      onChange={this.handleCheckboxChange}
                      checked={this.state.showNav}
                    />
                    Show navigation
                  </label>
                </div>
              </li>
              <li>
                <div className='checkbox'>
                  <label>
                    <input
                      id='show_index'
                      type='checkbox'
                      data-action='showIndex'
                      onChange={this.handleCheckboxChange}
                      checked={this.state.showIndex}
                    />
                    Show index
                  </label>
                </div>
              </li>
              <li>
                <div className='checkbox'>
                  <label>
                    <input
                      id='slide_on_thumbnail_hover'
                      type='checkbox'
                      data-action='slideOnThumbnailHover'
                      onChange={this.handleCheckboxChange}
                      checked={this.state.slideOnThumbnailHover}
                    />
                    Slide on thumbnail hover (desktop)
                  </label>
                </div>
              </li>
            </ul>
          </div>
        </div>
      )
    }
  }
}

module.exports = TestBatchScreenshots
