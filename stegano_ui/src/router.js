import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Signup from './views/Signup.vue'
import NewMessage from './views/NewMessage.vue'
import Inbox from './views/Inbox.vue'
import Outbox from './views/Outbox.vue'

Vue.use(Router)

var router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    }, {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { public: true }
    }, {
      path: '/signup',
      name: 'signup',
      component: Signup,
      meta: { public: true }
    }, {
      path: '/new',
      name: 'new',
      component: NewMessage
    }, {
      path: '/inbox',
      name: 'inbox',
      component: Inbox
    }, {
      path: '/outbox',
      name: 'outbox',
      component: Outbox
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    }
  ]
})

// goto login page if user is not autheroized
router.beforeEach(function (to, from, next) {
  if (!to.meta.public && !router.app.$auth.isAuthenticated()) {
    next('/login')
  } else {
    next()
  }
})
export default router
