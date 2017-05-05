import axios from 'axios'

// ====================================
// Constants
// ====================================

export const LOADED_TEST_INSTANCE_LIST_SUCCESS = 'LOADED_TEST_INSTANCE_LIST_SUCCESS'
export const LOADED_TEST_INSTANCE_LIST_ERROR = 'LOADED_TEST_INSTANCE_LIST_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestInstanceList')
logger.setLevel(__LOGLEVEL__)

export function doFetchTestInstance (session, testBatchUid, skip, limit, searchText) {
  return dispatch => {
    let data = {
      token: session.token,
      actions: [
        {
          action: 'read',
          model: 'testinstance',
          filters: {
            test_batch_id: testBatchUid
          },
          ascending: 'name',
          limit: limit,
          skip: skip
        }, {
          action: 'read',
          model: 'testbatch',
          uid: testBatchUid
        }
      ]
    }

    if (searchText !== '') {
      data.actions[0].filters_wildcard = {
        name: searchText
      }
    }

    axios.post('/api/crud', data)
      .then((response) => {
        logger.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          dispatch(loadedTestInstanceListSuccess(response.data, skip, limit))
        } else {
          dispatch(loadedTestInstanceListError(response.data.response[0].error))
        }
      })
  }
}

function loadedTestInstanceListSuccess (data, skip, limit) {
  data['skip'] = skip
  data['limit'] = limit
  return {
    type: LOADED_TEST_INSTANCE_LIST_SUCCESS,
    data
  }
}

function loadedTestInstanceListError (error) {
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
  testInstanceList: null,
  testBatch: null,
  totalTestInstance: 0,
  skip: 0,
  limit: 0
}

export default function testinstancelist (state = initialState, action) {
  switch (action.type) {
    case LOADED_TEST_INSTANCE_LIST_SUCCESS:
      return Object.assign({},
        initialState,
        {
          testInstanceList: action.data.results[0].results,
          totalTestInstance: action.data.results[0].total,
          testBatch: action.data.results[1].results[0],
          limit: action.data.limit,
          skip: action.data.skip
        }
      )

    case LOADED_TEST_INSTANCE_LIST_ERROR:
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
