import axios from 'axios'

// ====================================
// Constants
// ====================================

export const TEST_BATCH_DETAIL_LOADING_SUCCESS = 'TEST_BATCH_DETAIL_LOADING_SUCCESS'
export const TEST_BATCH_DETAIL_LOADING_ERROR = 'TEST_BATCH_DETAIL_LOADING_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestBatchDetail')
logger.setLevel(__LOGLEVEL__)

export function loadTestBatchDetail (session, testBatchUid) {
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
          dispatch(testBatchDetailLoadingSuccess(response.data))
        } else {
          dispatch(testBatchDetailLoadingError(response.error))
        }
      })
  }
}

function testBatchDetailLoadingSuccess (data) {
  return {
    type: TEST_BATCH_DETAIL_LOADING_SUCCESS,
    data
  }
}

function testBatchDetailLoadingError (error) {
  return {
    type: TEST_BATCH_DETAIL_LOADING_SUCCESS,
    error
  }
}

export const actions = {
  loadTestBatchDetail
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
    case TEST_BATCH_DETAIL_LOADING_SUCCESS:
      let testBatch = state.testBatch
      testBatch[action.data.results[0].uid] = action.data.results[0]
      return Object.assign({},
        state,
        {
          testBatch
        }
      )

    case TEST_BATCH_DETAIL_LOADING_ERROR:
      return Object.assign({},
        state,
        {
          error: action.data.error
        }
      )

    default:
      return state
  }
}
