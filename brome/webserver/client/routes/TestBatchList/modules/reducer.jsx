import axios from 'axios'

// ====================================
// Constants
// ====================================

export const LOADED_TEST_BATCH_LIST_SUCCESS = 'LOADED_TEST_BATCH_LIST_SUCCESS'
export const LOADED_TEST_BATCH_LIST_ERROR = 'LOADED_TEST_BATCH_LIST_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestBatchList')
logger.setLevel(__LOGLEVEL__)

export function doLoadTestBatchList (session, skip, limit) {
  return dispatch => {
    let data = {
      actions: {
        action: 'read',
        model: 'testbatch',
        descending: 'starting_timestamp',
        limit: limit,
        skip: skip
      },
      token: session.token
    }

    axios.post('/api/crud', data)
      .then((response) => {
        logger.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          dispatch(
            loadedTestBatchListSuccess(
              response.data,
              skip,
              limit
            )
          )
        } else {
          dispatch(loadedTestBatchListError(response.data.error))
        }
      })
  }
}

function loadedTestBatchListSuccess (data, skip, limit) {
  data.skip = skip
  data.limit = limit
  return {
    type: LOADED_TEST_BATCH_LIST_SUCCESS,
    data
  }
}

function loadedTestBatchListError (error) {
  return {
    type: LOADED_TEST_BATCH_LIST_ERROR,
    error
  }
}

export const actions = {
  doLoadTestBatchList
}

// ====================================
// Reducers
// ====================================

const initialState = {
  testBatchList: null,
  totalTestBatch: 0,
  limit: 0,
  skip: 0,
  error: null
}

export default function testbatchlist (state = initialState, action) {
  switch (action.type) {
    case LOADED_TEST_BATCH_LIST_SUCCESS:
      return Object.assign({},
        initialState,
        {
          testBatchList: action.data.results,
          totalTestBatch: action.data.total,
          limit: action.data.limit,
          skip: action.data.skip
        }
      )

    case LOADED_TEST_BATCH_LIST_ERROR:
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
