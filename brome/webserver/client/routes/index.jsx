import CoreLayout from 'layouts/CoreLayout/CoreLayout'
import Login from 'routes/Login'
import Logout from 'routes/Logout'
import Profile from 'routes/Profile'
import Video from 'routes/Video'
import ErrorPage from 'routes/ErrorPage'
import Register from 'routes/Register'
import browserIdsList from 'routes/browserIdsList'
import TestBatchList from 'routes/TestBatchList'
import TestBatchDetail from 'routes/TestBatchDetail'
import TestBatchRunnerLog from 'routes/TestBatchRunnerLog'
import TestInstanceList from 'routes/TestInstanceList'
import TestInstanceNetworkCapture from 'routes/TestInstanceNetworkCapture'
import TestInstanceDetailList from 'routes/TestInstanceDetailList'
import TestInstanceLog from 'routes/TestInstanceLog'
import TestBatchScreenshots from 'routes/TestBatchScreenshots'
import TestBatchCrashes from 'routes/TestBatchCrashes'
import TestBatchTestResults from 'routes/TestBatchTestResults'
import StartTestBatch from 'routes/StartTestBatch'

export const createRoutes = (store) => ({
  path: '/',
  component: CoreLayout,
  childRoutes: [
    TestBatchList(store),
    browserIdsList(store),
    StartTestBatch(store),
    TestBatchScreenshots(store),
    TestBatchCrashes(store),
    TestBatchTestResults(store),
    TestBatchDetail(store),
    TestBatchRunnerLog(store),
    TestInstanceLog(store),
    TestInstanceList(store),
    TestInstanceNetworkCapture(store),
    TestInstanceDetailList(store),
    Login(store),
    Profile(store),
    Logout(store),
    Register(store),
    Video(store),
    ErrorPage(store)
  ]
})

export const notAuthRoutes = ['/login', '/register']
