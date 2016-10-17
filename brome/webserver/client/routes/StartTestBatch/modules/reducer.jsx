import axios from 'axios'
import { routerActions } from 'react-router-redux'

// ====================================
// Constants
// ====================================

export const LOADED_BROME_CONFIG_SUCCESS = 'LOADED_BROME_CONFIG_SUCCESS'
export const LOADED_BROME_CONFIG_ERROR = 'LOADED_BROME_CONFIG_ERROR'
export const STARTING_NEW_TEST_BATCH = 'STARTING_NEW_TEST_BATCH'
export const STARTED_NEW_TEST_BATCH_SUCCESS = 'STARTED_NEW_TEST_BATCH_SUCCESS'
export const STARTED_NEW_TEST_BATCH_ERROR = 'STARTED_NEW_TEST_BATCH_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('StartTestBatch')
logger.setLevel(__LOGLEVEL__)

export function doStartTestBatch (data, nextPath) {
  return dispatch => {
    dispatch({type: STARTING_NEW_TEST_BATCH})

    axios.post('/api/starttestbatch', data)
      .then((response) => {
        logger.debug('/api/getbromeconfig (response)', response)

        if (response.data.success) {
          dispatch(startedNewTestBatchSuccess(response.data))
          dispatch(routerActions.push(nextPath))
        } else {
          dispatch(startedNewTestBatchError(response.data.error))
        }
      })
  }
}

function startedNewTestBatchSuccess (data) {
  return {
    type: STARTED_NEW_TEST_BATCH_SUCCESS,
    data
  }
}

function startedNewTestBatchError (error) {
  return {
    type: STARTED_NEW_TEST_BATCH_ERROR,
    error
  }
}

export function doLoadBromeConfig () {
  return dispatch => {
    axios.get('/api/getbromeconfig')
      .then((response) => {
        logger.debug('/api/getbromeconfig (response)', response)

        if (response.data.success) {
          dispatch(loadedBromeConfigSuccess(response.data))
        } else {
          dispatch(loadedBromeConfigError(response.data.error))
        }
      })
  }
}

function loadedBromeConfigSuccess (data) {
  return {
    type: LOADED_BROME_CONFIG_SUCCESS,
    data
  }
}

function loadedBromeConfigError (error) {
  return {
    type: LOADED_BROME_CONFIG_ERROR,
    error
  }
}

export const actions = {
  doLoadBromeConfig,
  doStartTestBatch
}

// ====================================
// Reducers
// ====================================

const initialState = {
  error: null,
  bromeConfig: null,
  tests: null,
  startingTestBatch: false,
  startedTestBatch: false
}

export default function starttestbatch (state = initialState, action) {
  switch (action.type) {
    case STARTED_NEW_TEST_BATCH_SUCCESS:
      return Object.assign({},
        state,
        {
          error: null,
          startedTestBatch: true,
          startingTestBatch: false
        }
      )

    case STARTED_NEW_TEST_BATCH_ERROR:
      return Object.assign({},
        state,
        {
          error: action.error,
          startedTestBatch: false,
          startingTestBatch: false
        }
      )

    case STARTING_NEW_TEST_BATCH:
      return Object.assign({},
        state,
        {
          error: null,
          startedTestBatch: false,
          startingTestBatch: true
        }
      )

    case LOADED_BROME_CONFIG_SUCCESS:
      return Object.assign({},
        initialState,
        {
          bromeConfig: action.data.config,
          tests: action.data.tests
        }
      )

    case LOADED_BROME_CONFIG_ERROR:
      return Object.assign({},
        initialState,
        {
          error: action.error
        }
      )

    default:
      return state
  }
}

