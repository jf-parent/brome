import React from 'react'
import { FormattedMessage } from 'react-intl'

import BaseComponent from 'core/BaseComponent'
import HomeStyle from 'components/HomeStyle.postcss'

class Home extends BaseComponent {

  render () {
    return (
      <div className='container-fluid'>
        <div className='row'>
          <div className='col-xs-12 col-sm-12 col-md-12 col-lg-12 col-md-offset-3 col-lg-offset-3'>
            <h2>
              <FormattedMessage
                id='home.BromeTitle'
                defaultMessage='Brome - Python Selenium Framework'
              />
            </h2>
          </div>
        </div>
        <div className='row'>
          <div className='col-xs-12 col-sm-12 col-md-4  col-lg-4'>
            <div className={HomeStyle['badge-service']}>
              <center>
                <h3>
                  <i className='fa fa-file-code-o' aria-hidden='true'></i>
                  {' '}
                  <a href='https://github.com/jf-parent/brome/tree/release/example' target='_blank'>
                    <FormattedMessage
                      id='home.BromeExample'
                      defaultMessage='See Project Example'
                    />
                  </a>
                </h3>
              </center>
            </div>
          </div>
          <div className='col-xs-12 col-sm-12 col-md-4  col-lg-4'>
            <div className={HomeStyle['badge-service']}>
              <center>
                <h3>
                  <i className='fa fa-github' aria-hidden='true'></i>
                  {' '}
                  <a href='https://github.com/jf-parent/brome' target='_blank'>
                    <FormattedMessage
                      id='home.BromeRepo'
                      defaultMessage='See Github Repo'
                    />
                  </a>
                </h3>
              </center>
            </div>
          </div>
          <div className='col-xs-12 col-sm-12 col-md-4  col-lg-4'>
            <div className={HomeStyle['badge-service']}>
              <center>
                <h3>
                  <i className='fa fa-book' aria-hidden='true'></i>
                  {' '}
                  <a href='https://brome.readthedocs.io/en/release/' target='_blank'>
                    <FormattedMessage
                      id='home.BromeDocumentation'
                      defaultMessage='See Documentation'
                    />
                  </a>
                </h3>
              </center>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Home
