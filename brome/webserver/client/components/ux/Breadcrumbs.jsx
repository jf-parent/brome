import React, { Component, PropTypes } from 'react'
import { FormattedMessage } from 'react-intl'
import { Link } from 'react-router'

class Breadcrumbs extends Component {

  static propTypes = {
    routes: PropTypes.array.isRequired
  }

  render () {
    return (
      <div className='row'>
        <div className='col-xs-12 col-sm-12 col-md-12 col-lg-12'>
          <ol className='breadcrumb'>
          {(() => {
            return this.props.routes.map((route, index) => {
              if (route.disable) {
                return (
                  <li key={index} className='active'>
                    <FormattedMessage
                      id={'nav.' + route.msgId}
                      defaultMessage={route.msgId}
                    />
                  </li>
                )
              } else {
                return (
                  <li key={index}>
                    <Link to={route.to}>
                      <FormattedMessage
                        id={'nav.' + route.msgId}
                        defaultMessage={route.msgId}
                      />
                    </Link>
                  </li>
                )
              }
            })
          })()}
          </ol>
        </div>
      </div>
    )
  }
}

export default Breadcrumbs
