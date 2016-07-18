import axios from 'axios'

// ====================================
// Constants
// ====================================

export const LOADING_TEST_INSTANCE_LIST = 'LOADING_TEST_INSTANCE_LIST'
export const LOADED_TEST_INSTANCE_LIST_SUCCESS = 'LOADED_TEST_INSTANCE_LIST_SUCCESS'
export const LOADED_TEST_INSTANCE_LIST_ERROR = 'LOADED_TEST_INSTANCE_LIST_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestInstanceLogList')
logger.setLevel(__LOGLEVEL__)

export function doFetchTestInstance (data) {
  return dispatch => {
    dispatch({type: LOADING_TEST_INSTANCE_LIST})

    axios.post('/api/testbatch', data)
      .then((response) => {
        logger.debug('/api/testbatch (data) (response)', data, response)

        if (response.data.success) {
          dispatch(loadTestInstanceSuccess(response.data))
        } else {
          dispatch(loadTestInstanceError(response.error))
        }
      })
  }
}

function loadTestInstanceSuccess (data) {
  return {
    type: LOADED_TEST_INSTANCE_LIST_SUCCESS,
    data
  }
}

function loadTestInstanceError (error) {
  return {
    type: LOADED_TEST_INSTANCE_LIST_ERROR,
    error
  }
}

export const actions = {
  doFetchTestInstance
}

// ====================================
// Reducers
// ====================================

const initialState = {
  error: null,
  loading: true,
  testInstanceList: [],
  testBatch: null,
  totalTestInstance: 0,
  skip: 0,
  limit: 10
}

export default function testinstanceloglist (state = initialState, action) {
  switch (action.type) {
    case LOADING_TEST_INSTANCE_LIST:
      return Object.assign({},
        initialState,
        {
          loading: true
        }
      )

    case LOADED_TEST_INSTANCE_LIST_SUCCESS:
      return Object.assign({},
        initialState,
        {
          loading: false,
          testInstanceList: action.data.results,
          totalTestInstance: action.data.total,
          testBatch: action.data.parent
        }
      )

    case LOADED_TEST_INSTANCE_LIST_ERROR:
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

