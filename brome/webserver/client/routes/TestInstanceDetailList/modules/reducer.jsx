import axios from 'axios'

// ====================================
// Constants
// ====================================

export const LOADED_TEST_INSTANCE_LIST_DETAIL_SUCCESS = 'LOADED_TEST_INSTANCE_LIST_DETAIL_SUCCESS'
export const LOADED_TEST_INSTANCE_DETAIL_LIST_ERROR = 'LOADED_TEST_INSTANCE_DETAIL_LIST_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestInstanceDetailList')
logger.setLevel(__LOGLEVEL__)

export function doFetchTestInstanceDetailList (session, testBatchUid, skip, limit) {
  return dispatch => {
    let data = {
      token: session.token,
      actions: [
        {
          action: 'read',
          model: 'testinstance',
          skip: skip,
          limit: limit,
          ascending: 'name',
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
          dispatch(loadedTestInstanceDetailListSuccess(response.data, skip, limit))
        } else {
          dispatch(loadedTestInstanceDetailListError(response.data.results[0].error))
        }
      })
  }
}

function loadedTestInstanceDetailListSuccess (data, skip, limit) {
  data['skip'] = skip
  data['limit'] = limit
  return {
    type: LOADED_TEST_INSTANCE_LIST_DETAIL_SUCCESS,
    data
  }
}

function loadedTestInstanceDetailListError (error) {
  return {
    type: LOADED_TEST_INSTANCE_DETAIL_LIST_ERROR,
    error
  }
}

export const actions = {
  doFetchTestInstanceDetailList
}

// ====================================
// Reducers
// ====================================

const initialState = {
  testInstanceDetailList: null,
  error: null,
  totalTestInstance: 0,
  testBatch: null,
  skip: 0,
  limit: 10
}

export default function testinstancedetaillist (state = initialState, action) {
  switch (action.type) {

    case LOADED_TEST_INSTANCE_LIST_DETAIL_SUCCESS:
      return Object.assign({},
        initialState,
        {
          testInstanceDetailList: action.data.results[0].results,
          totalTestInstance: action.data.results[0].total,
          testBatch: action.data.results[1].results[0],
          limit: action.data.limit,
          skip: action.data.skip
        }
      )

    case LOADED_TEST_INSTANCE_DETAIL_LIST_ERROR:
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
