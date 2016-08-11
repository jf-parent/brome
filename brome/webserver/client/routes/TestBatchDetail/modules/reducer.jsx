import axios from 'axios'

// ====================================
// Constants
// ====================================

export const RESET = 'RESET'
export const TERMINATING_TEST_BATCH = 'TERMINATING_TEST_BATCH'
export const TERMINATED_TEST_BATCH_SUCCESS = 'TERMINATED_TEST_BATCH_SUCCESS'
export const TERMINATED_TEST_BATCH_ERROR = 'TERMINATED_TEST_BATCH_ERROR'
export const DELETING_TEST_BATCH = 'DELETING_TEST_BATCH'
export const DELETED_TEST_BATCH_SUCCESS = 'DELETED_TEST_BATCH_SUCCESS'
export const DELETED_TEST_BATCH_ERROR = 'DELETED_TEST_BATCH_ERROR'
export const LOADED_TEST_BATCH_DETAIL_SUCCESS = 'LOADED_TEST_BATCH_DETAIL_SUCCESS'
export const LOADED_TEST_BATCH_DETAIL_ERROR = 'LOADED_TEST_BATCH_DETAIL_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestBatchDetail')
logger.setLevel(__LOGLEVEL__)

export function doReset () {
  return dispatch => {
    dispatch({type: RESET})
  }
}

export function doDelete (data) {
  return dispatch => {
    dispatch({type: DELETING_TEST_BATCH})

    axios.post('/api/crud', data)
      .then((response) => {
        logger.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          dispatch({type: DELETED_TEST_BATCH_SUCCESS})
        } else {
          dispatch({type: DELETED_TEST_BATCH_ERROR})
        }
      })
  }
}

export function doTerminate (data) {
  return dispatch => {
    dispatch({type: TERMINATING_TEST_BATCH})

    axios.post('/api/crud', data)
      .then((response) => {
        logger.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          dispatch({type: TERMINATED_TEST_BATCH_SUCCESS})
        } else {
          dispatch({type: TERMINATED_TEST_BATCH_ERROR})
        }
      })
  }
}

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
  doLoadTestBatchDetail,
  doTerminate,
  doDelete,
  doReset
}

// ====================================
// Reducers
// ====================================

const initialState = {
  testBatch: {},
  deletingTestBatch: false,
  deletedTestBatchSuccess: false,
  deletedTestBatchError: false,
  terminatingTestBatch: false,
  terminatedTestBatchSuccess: false,
  terminatedTestBatchError: false,
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

    case DELETING_TEST_BATCH:
      return Object.assign({},
        state,
        {
          deletingTestBatch: true
        }
      )

    case DELETED_TEST_BATCH_SUCCESS:
      return Object.assign({},
        state,
        {
          deletingTestBatch: false,
          deletedTestBatchSuccess: true
        }
      )

    case DELETED_TEST_BATCH_ERROR:
      return Object.assign({},
        state,
        {
          deletingTestBatch: false,
          deletedTestBatchError: true
        }
      )

    case TERMINATING_TEST_BATCH:
      return Object.assign({},
        state,
        {
          terminatingTestBatch: true
        }
      )

    case TERMINATED_TEST_BATCH_SUCCESS:
      return Object.assign({},
        state,
        {
          terminatingTestBatch: false,
          terminatedTestBatchSuccess: true
        }
      )

    case TERMINATED_TEST_BATCH_ERROR:
      return Object.assign({},
        state,
        {
          terminatingTestBatch: false,
          terminatedTestBatchError: true
        }
      )

    case RESET:
      return Object.assign({},
        state,
        {
          terminatingTestBatch: false,
          terminatedTestBatchSuccess: false,
          terminatedTestBatchError: false,
          deletingTestBatch: false,
          deletedTestBatchSuccess: false,
          deletedTestBatchError: false
        }
      )

    default:
      return state
  }
}
