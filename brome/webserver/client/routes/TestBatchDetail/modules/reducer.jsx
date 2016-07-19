import axios from 'axios'

// ====================================
// Constants
// ====================================

export const LOADED_TEST_BATCH_DETAIL_SUCCESS = 'LOADED_TEST_BATCH_DETAIL_SUCCESS'
export const LOADED_TEST_BATCH_DETAIL_ERROR = 'LOADED_TEST_BATCH_DETAIL_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestBatchDetail')
logger.setLevel(__LOGLEVEL__)

export function doLoadTestBatchDetail (session, testBatchUid) {
  let data = {
    token: session.token,
    actions: {
      action: 'read',
      model: 'testbatch',
      uid: testBatchUid
    }
  }
  return dispatch => {
    axios.post('/api/crud', data)
      .then((response) => {
        logger.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          dispatch(loadedTestBatchDetailSuccess(response.data))
        } else {
          dispatch(loadedTestBatchDetailError(response.data.error))
        }
      })
  }
}

function loadedTestBatchDetailSuccess (data) {
  return {
    type: LOADED_TEST_BATCH_DETAIL_SUCCESS,
    data
  }
}

function loadedTestBatchDetailError (error) {
  return {
    type: LOADED_TEST_BATCH_DETAIL_ERROR,
    error
  }
}

export const actions = {
  doLoadTestBatchDetail
}

// ====================================
// Reducers
// ====================================

const initialState = {
  testBatch: {},
  error: null
}

export default function testbatchdetail (state = initialState, action) {
  switch (action.type) {
    case LOADED_TEST_BATCH_DETAIL_SUCCESS:
      let testBatch = state.testBatch
      testBatch[action.data.results[0].uid] = action.data.results[0]
      return Object.assign({},
        state,
        {
          testBatch
        }
      )

    case LOADED_TEST_BATCH_DETAIL_ERROR:
      return Object.assign({},
        state,
        {
          error: action.error
        }
      )

    default:
      return state
  }
}
