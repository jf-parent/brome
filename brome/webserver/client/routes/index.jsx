import CoreLayout from 'layouts/CoreLayout/CoreLayout'
import Login from 'routes/Login'
import Logout from 'routes/Logout'
import Profile from 'routes/Profile'
import ErrorPage from 'routes/ErrorPage'
import ForgottenPassword from 'routes/ForgottenPassword'
import Register from 'routes/Register'
import Confirmation from 'routes/Confirmation'
import ResetPassword from 'routes/ResetPassword'
import Dashboard from 'routes/Dashboard'
import TestBatchList from 'routes/TestBatchList'
import TestBatchDetail from 'routes/TestBatchDetail'

export const createRoutes = (store) => ({
  path: '/',
  component: CoreLayout,
  childRoutes: [
    Dashboard(store),
    TestBatchList(store),
    TestBatchDetail(store),
    ResetPassword(store),
    Login(store),
    Profile(store),
    ForgottenPassword(store),
    Logout(store),
    Register(store),
    Confirmation(store),
    ErrorPage(store)
  ]
})

export const notAuthRoutes = ['/login', '/register', '/forgottenpassword']
