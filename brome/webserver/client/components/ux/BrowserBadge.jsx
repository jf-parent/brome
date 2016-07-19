import React, { Component, PropTypes } from 'react'
import 'font-awesome-webpack'

// import BrowserBadgeStyle from './BrowserBadgeStyle.postcss'

class BrowserBadge extends Component {

  static propTypes = {
    browserName: PropTypes.string.isRequired,
    browserVersion: PropTypes.string,
    browserIcon: PropTypes.string,
    platform: PropTypes.string
  }

  title (string) {
    return string.charAt(0).toUpperCase() + string.slice(1)
  }

  render () {
    return (
      <span>
        {' '}
        {(() => {
          // Browser Icon
          if (this.props.browserIcon) {
            return (
              <i className={'fa fa-' + this.props.browserIcon} aria-hidden='true'></i>
            )
          } else {
            return null
          }
        })()}
        <small>{' '}{this.title(this.props.browserName)}</small>
        {(() => {
          // Browser Version
          if (this.props.browserVersion) {
            return (
              <i>{' '}{this.props.browserVersion}</i>
            )
          } else {
            return null
          }
        })()}
        {(() => {
          // Platform
          if (this.props.platform) {
            return (
              <b>{' - '}{this.props.platform}</b>
            )
          } else {
            return null
          }
        })()}
      </span>
    )
  }
}

export default BrowserBadge
