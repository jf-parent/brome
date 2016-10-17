import axios from 'axios'

// ====================================
// Constants
// ====================================

export const LOADING_BROWSER_IDS_LIST = 'LOADING_BROWSER_IDS_LIST'
export const LOADED_BROWSER_IDS_LIST_SUCCESS = 'LOADED_BROWSER_IDS_LIST_SUCCESS'
export const LOADED_BROWSER_IDS_LIST_ERROR = 'LOADED_BROWSER_IDS_LIST_ERROR'

// ====================================
// Actions
// ====================================

const logger = require('loglevel').getLogger('BrowserIdsList')
logger.setLevel(__LOGLEVEL__)

export function doFetchBrowserIds (data, skip, limit) {
  return dispatch => {
    axios.post('/api/crud', data)
      .then((response) => {
        logger.debug('/api/crud (data) (response)', data, response)

        if (response.data.success) {
          dispatch(loadedBrowserIdsSuccess(response.data, skip, limit))
        } else {
          dispatch(loadedBrowserIdsError(response.data.error))
        }
      })
  }
}

function loadedBrowserIdsSuccess (data, skip, limit) {
  data['skip'] = skip
  data['limit'] = limit
  return {
    type: LOADED_BROWSER_IDS_LIST_SUCCESS,
    data
  }
}

function loadedBrowserIdsError (error) {
  return {
    type: LOADED_BROWSER_IDS_LIST_ERROR,
    error
  }
}

export const actions = {
  doFetchBrowserIds
}

// ====================================
// Reducers
// ====================================

const initialState = {
  error: null,
  broswerIds: null,
  testBatch: null,
  loading: true,
  totalBrowserIds: 0,
  skip: 0,
  limit: 0
}

export default function browseridslist (state = initialState, action) {
  switch (action.type) {
    case LOADING_BROWSER_IDS_LIST:
      return Object.assign({},
        initialState,
        {
          loading: true
        }
      )

    case LOADED_BROWSER_IDS_LIST_SUCCESS:
      return Object.assign({},
        initialState,
        {
          browserIdsList: action.data.results[0].browser_ids,
          totalBrowserIds: action.data.results[0].browser_ids.length,
          testBatch: action.data.results[0],
          loading: false,
          limit: action.data.limit,
          skip: action.data.skip
        }
      )

    case LOADED_BROWSER_IDS_LIST_ERROR:
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
