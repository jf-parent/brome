import React from 'react'
import { FormattedMessage } from 'react-intl'
import Collapse, { Panel } from 'rc-collapse'
import 'rc-collapse/assets/index.css'
import Formsy from 'formsy-react'
import 'font-awesome-webpack'

// import ComponentStyle from './ComponentStyle.postcss'
import MultiCheckboxSet from 'components/ux/MultiCheckboxSet'
import SecureFormStyle from 'components/ux/SecureFormStyle.postcss'
import SecureForm from 'components/ux/SecureForm'
import LaddaButton from 'components/ux/LaddaButton'
import Loading from 'components/ux/Loading'
import ErrorMsg from 'components/ux/ErrorMsg'
import BaseComponent from 'core/BaseComponent'

Formsy.addValidationRule('requiredOneBrowser', (values, value) => {
  return !!values.browsers.length
})

Formsy.addValidationRule('requiredOneTest', (values, value) => {
  return !!values.tests.length
})

class StartTestBatch extends BaseComponent {
  constructor (props) {
    super(props)

    this._initLogger()
    this._bind(
      'enableButton',
      'uncheckAll',
      'checkAll',
      'disableButton',
      'onSubmit'
    )

    this.state = {
      'selectedTests': []
    }
  }

  componentWillMount () {
    this.props.actions.doLoadBromeConfig()
  }

  uncheckAll () {
    this.setState({selectedTests: []})
  }

  checkAll () {
    this.setState({selectedTests: this.props.state.starttestbatch.tests})
  }

  onSubmit (event) {
    event.preventDefault()
    this.debug('onSubmit()')

    this.props.actions.doStartTestBatch(this.refs.form.getModel(), '/testbatchlist')
  }

  enableButton () {
    this.debug('enableButton')
    this.refs.button.setState({ isDisabled: false })
  }

  disableButton () {
    this.debug('disableButton')
    this.refs.button.setState({ isDisabled: true })
  }

  render () {
    let starttestbatch = this.props.state.starttestbatch

    if (!starttestbatch.bromeConfig) {
      return (
        <div className='container-fluid'>
          <Loading style={{left: '50%'}} />
        </div>
      )
    } else if (starttestbatch.error !== null) {
      return <ErrorMsg msgId={starttestbatch.error} />
    } else {
      let browsers = Object.keys(starttestbatch.bromeConfig['browsers_config']).sort()
      let tests = starttestbatch.tests
      let selectedTests = this.state.selectedTests

      return (
        <div className='container-fluid'>
          <SecureForm ref='form' style={{maxWidth: '100%'}} onValid={this.enableButton} onInvalid={this.disableButton} session={this.props.state.session}>
            <center>
              <h2 className={SecureFormStyle['form-signin-heading']}>
                <FormattedMessage
                  id='starttestbatch.StartTestBatch'
                  defaultMessage='Start Test Batch'
                />
              </h2>
            </center>
            <Collapse activeKey='1'>
              <Panel header='Browsers (select at least one):' key='1'>
                <MultiCheckboxSet
                  value={[]}
                  name='browsers'
                  items={browsers}
                  validations='requiredOneBrowser'
                />
              </Panel>
            </Collapse>
            <Collapse>
              <Panel header='Tests (run all by default):'>
                <a className='btn btn-default btn-link' onClick={this.uncheckAll}>Uncheck All</a>
                {' - '}
                <a className='btn btn-default btn-link' onClick={this.checkAll}>Check All</a>
                <MultiCheckboxSet
                  value={selectedTests}
                  name='tests'
                  items={tests}
                  validations='requiredOneTest'
                />
              </Panel>
            </Collapse>
            <LaddaButton ref='button' style={{'marginTop': '6px'}} isDisabled isLoading={starttestbatch.startingTestBatch} onSubmit={this.onSubmit}>
              <FormattedMessage
                id='startTestBatch.SubmitBtn'
                defaultMessage='Start'
              />
            </LaddaButton>
          </SecureForm>
        </div>
      )
    }
  }
}

module.exports = StartTestBatch
