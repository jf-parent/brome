import React, { PropTypes } from 'react'
import Formsy from 'formsy-react'

function contains (container, item) {
  for (const it of container) {
    if (it === item) {
      return true
    }
  }
  return false
}

const MultiCheckboxSet = React.createClass({
  mixins: [Formsy.Mixin],

  propTypes: {
    name: PropTypes.string.isRequired,
    items: PropTypes.array.isRequired,
    value: PropTypes.array.isRequired,
    className: PropTypes.string
  },

  getInitialState () {
    return { value: [] }
  },

  componentDidMount () {
    const value = this.props.value
    this.setValue(value)
    this.setState({
      value: value
    })
  },

  changeValue (event) {
    const item = event.target.dataset.item
    const checked = event.currentTarget.checked

    let newValue = []
    if (checked) {
      newValue = this.state.value.concat(item)
    } else {
      newValue = this.state.value.filter(it => it !== item)
    }

    this.setValue(newValue)
    this.setState({ value: newValue })
  },

  render () {
    const className = 'form-group' + (this.props.className || ' ') +
      (this.showRequired() ? 'required' : this.showError() ? 'error' : '')
    const errorMessage = this.getErrorMessage()

    const { name, items } = this.props
    const itemStyle = {
      marginLeft: '6px'
    }
    return (
      <div className={className}>
        {(() => {
          return items.map((item, i) => {
            return (
              <div key={i}>
                <input
                  type='checkbox'
                  data-item={item}
                  name={name}
                  onChange={this.changeValue}
                  checked={contains(this.state._value, item)}
                />
                <span style={itemStyle}>{item}</span>
              </div>
            )
          })
        })()}
        <span className='validation-error'>{errorMessage}</span>
      </div>
    )
  }

})

export default MultiCheckboxSet
