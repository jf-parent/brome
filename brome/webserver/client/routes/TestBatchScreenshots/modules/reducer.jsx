import axios from 'axios'

// ====================================
// Constants
// ====================================

export const LOADING_TEST_BATCH_SCREENSHOTS = 'LOADING_TEST_BATCH_SCREENSHOTS'
export const LOADED_TEST_BATCH_SCREENSHOTS_SUCCESS = 'LOADED_TEST_BATCH_SCREENSHOTS_SUCCESS'
export const LOADED_TEST_BATCH_SCREENSHOTS_ERROR = 'LOADED_TEST_BATCH_SCREENSHOTS_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestBatchScreenshots')
logger.setLevel(__LOGLEVEL__)

export function doFetchScreenshots (data) {
  return dispatch => {
    dispatch({type: LOADING_TEST_BATCH_SCREENSHOTS})

    axios.post('/api/crud', data)
      .then((response) => {
        logger.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          dispatch(loadedTestBatchScreenshotSuccess(response.data))
        } else {
          dispatch(loadedTestBatchScreenshotError(response.data.results[0].error))
        }
      })
  }
}

function loadedTestBatchScreenshotSuccess (data) {
  return {
    type: LOADED_TEST_BATCH_SCREENSHOTS_SUCCESS,
    data
  }
}

function loadedTestBatchScreenshotError (error) {
  return {
    type: LOADED_TEST_BATCH_SCREENSHOTS_ERROR,
    error
  }
}

export const actions = {
  doFetchScreenshots
}

// ====================================
// Reducers
// ====================================

// TODO support infinite loading
const initialState = {
  screenshots: [],
  testBatch: null,
  error: null,
  loading: true
}

export default function testbatchscreenshots (state = initialState, action) {
  switch (action.type) {
    case LOADING_TEST_BATCH_SCREENSHOTS:
      return Object.assign({},
        initialState,
        {
          loading: true
        }
      )

    case LOADED_TEST_BATCH_SCREENSHOTS_SUCCESS:
      return Object.assign({},
        initialState,
        {
          screenshots: action.data.results[0].results,
          testBatch: action.data.results[1].results[0],
          loading: false
        }
      )

    case LOADED_TEST_BATCH_SCREENSHOTS_ERROR:
      return Object.assign({},
        initialState,
        {
          loading: false,
          error: action.error
        }
      )

    default:
      return state
  }
}

