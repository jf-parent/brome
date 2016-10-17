import axios from 'axios'

// ====================================
// Constants
// ====================================

export const LOADED_TEST_INSTANCE_NETWORK_CAPTURE_SUCCESS = 'LOADED_TEST_INSTANCE_NETWORK_CAPTURE_SUCCESS'
export const LOADED_TEST_INSTANCE_NETWORK_CAPTURE_ERROR = 'LOADED_TEST_INSTANCE_NETWORK_CAPTURE_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestInstanceNetworkCapture')
logger.setLevel(__LOGLEVEL__)

export function doFetchTestInstanceNetworkCapture (session, testBatchUid, skip, limit) {
  return dispatch => {
    let data = {
      token: session.token,
      actions: [
        {
          action: 'read',
          model: 'testinstance',
          ascending: 'name',
          limit: limit,
          skip: skip,
          filters: {
            test_batch_id: testBatchUid
          }
        }, {
          action: 'read',
          model: 'testbatch',
          uid: testBatchUid
        }
      ]
    }
    axios.post('/api/crud', data)
      .then((response) => {
        logger.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          dispatch(loadedTestInstanceNetworkCaptureSuccess(response.data, skip, limit))
        } else {
          dispatch(loadedTestInstanceNetworkCaptureError(response.data.results[0].error))
        }
      })
  }
}

function loadedTestInstanceNetworkCaptureSuccess (data, skip, limit) {
  data['skip'] = skip
  data['limit'] = limit
  return {
    type: LOADED_TEST_INSTANCE_NETWORK_CAPTURE_SUCCESS,
    data
  }
}

function loadedTestInstanceNetworkCaptureError (error) {
  return {
    type: LOADED_TEST_INSTANCE_NETWORK_CAPTURE_ERROR,
    error
  }
}

export const actions = {
  doFetchTestInstanceNetworkCapture
}

// ====================================
// Reducers
// ====================================

const initialState = {
  testInstanceNetworkCaptureList: null,
  error: null,
  totalTestInstanceNetworkCapture: 0,
  testBatch: null,
  skip: 0,
  limit: 10
}

export default function testinstancenetworkcapture (state = initialState, action) {
  switch (action.type) {

    case LOADED_TEST_INSTANCE_NETWORK_CAPTURE_SUCCESS:
      return Object.assign({},
        initialState,
        {
          testInstanceNetworkCaptureList: action.data.results[0].results,
          totalTestInstanceNetworkCapture: action.data.total,
          testBatch: action.data.results[1].results[0],
          limit: action.data.limit,
          skip: action.data.skip
        }
      )

    case LOADED_TEST_INSTANCE_NETWORK_CAPTURE_ERROR:
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
