import axios from 'axios'

// ====================================
// Constants
// ====================================

export const TEST_BATCH_LIST_LOADING = 'TEST_BATCH_LIST_LOADING'
export const TEST_BATCH_LIST_LOADED = 'TEST_BATCH_LIST_LOADED'
export const TEST_BATCH_LIST_LOADING_ERROR = 'TEST_BATCH_LIST_LOADING_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestBatchList')
logger.setLevel(__LOGLEVEL__)

export function loadTestBatch (session, skip, limit) {
  return dispatch => {
    dispatch({type: TEST_BATCH_LIST_LOADING})

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
            testBatchListLoaded(
              response.data,
              skip,
              limit
            )
          )
        } else {
          dispatch(testBatchListLoadingError(response.error))
        }
      })
  }
}

function testBatchListLoaded (data, skip, limit) {
  data.skip = skip
  data.limit = limit
  return {
    type: TEST_BATCH_LIST_LOADED,
    data
  }
}

function testBatchListLoadingError (error) {
  return {
    type: TEST_BATCH_LIST_LOADING_ERROR,
    error
  }
}

export const actions = {
  loadTestBatch
}

// ====================================
// Reducers
// ====================================

const initialState = {
  loading: false,
  testBatchList: [],
  totalTestBatch: 0,
  error: null
}

export default function testbatchlist (state = initialState, action) {
  switch (action.type) {
    case TEST_BATCH_LIST_LOADING:
      return Object.assign({},
        initialState,
        {
          loading: true
        }
      )

    case TEST_BATCH_LIST_LOADED:
      return Object.assign({},
        initialState,
        {
          testBatchList: action.data.results,
          totalTestBatch: action.data.total,
          limit: action.data.limit,
          skip: action.data.skip
        }
      )

    case TEST_BATCH_LIST_LOADING_ERROR:
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
