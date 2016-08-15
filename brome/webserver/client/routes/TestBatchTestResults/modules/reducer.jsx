import axios from 'axios'

// ====================================
// Constants
// ====================================

export const LOADING_TEST_RESULTS = 'LOADING_TEST_RESULTS'
export const LOADED_TEST_RESULTS_SUCCESS = 'LOADED_TEST_RESULTS_SUCCESS'
export const LOADED_TEST_RESULTS_ERROR = 'LOADED_TEST_RESULTS_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('TestBatchTestResults')
logger.setLevel(__LOGLEVEL__)

export function doLoadTestResults (session, testBatchUid, skip, limit, loading, filterBy, orderBy) {
  return dispatch => {
    if (loading) {
      dispatch({type: LOADING_TEST_RESULTS})
    }

    let data = {
      token: session.token,
      actions: [
        {
          action: 'read',
          model: 'testresult',
          filters: {
            'test_batch_id': testBatchUid
          },
          limit: limit,
          skip: skip
        }, {
          action: 'read',
          model: 'testbatch',
          uid: testBatchUid
        }
      ]
    }

    if (filterBy) {
      data.actions[0]['filters'] = {
        'testid': filterBy
      }
    }

    if (orderBy === 'clear') {
      orderBy = null
    } else if (orderBy) {
      let direction = orderBy.split('_').pop()
      let property = orderBy.substring(0, orderBy.lastIndexOf('_'))

      if (direction === 'asc') {
        data.actions[0]['ascending'] = property
      } else if (direction === 'desc') {
        data.actions[0]['descending'] = property
      } else {
        logger.error('Wrong direction: ' + direction)
      }
    }

    axios.post('/api/crud', data)
      .then((response) => {
        logger.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          dispatch(loadedTestResultsSuccess(response.data, skip, limit, filterBy, orderBy))
        } else {
          dispatch(loadedTestResultsError(response.error))
        }
      })
  }
}

function loadedTestResultsSuccess (data, skip, limit, filterBy, orderBy) {
  data['skip'] = skip
  data['limit'] = limit
  data['filterBy'] = filterBy
  data['orderBy'] = orderBy
  return {
    type: LOADED_TEST_RESULTS_SUCCESS,
    data
  }
}

function loadedTestResultsError (error) {
  return {
    type: LOADED_TEST_RESULTS_ERROR,
    error
  }
}

export const actions = {
  doLoadTestResults
}

// ====================================
// Reducers
// ====================================

const initialState = {
  testResults: [],
  loading: true,
  filterBy: null,
  orderBy: 'result_asc',
  totalTestResults: 0,
  testBatch: null,
  error: null,
  skip: 0,
  limit: 10
}

export default function testbatchtestresults (state = initialState, action) {
  switch (action.type) {
    case LOADING_TEST_RESULTS:
      return Object.assign({},
        initialState,
        {
          loading: true
        }
      )

    case LOADED_TEST_RESULTS_SUCCESS:
      return Object.assign({},
        initialState,
        {
          loading: false,
          testResults: action.data.results[0].results,
          totalTestResults: action.data.results[0].total,
          testBatch: action.data.results[1].results[0],
          orderBy: action.data.orderBy,
          filterBy: action.data.filterBy,
          skip: action.data.skip,
          limit: action.data.limit
        }
      )

    case LOADED_TEST_RESULTS_ERROR:
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
