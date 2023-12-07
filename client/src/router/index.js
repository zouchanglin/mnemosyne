import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login'
import Home from '../components/Home'
import Main from '../components/Main'
import Me from '../components/Me'
import Notify from '../components/Notify'

import WordList from '@/components/WordList.vue'
import AIReading from '@/components/MainChild/AIReading.vue'
import WordStudy from '@/components/MainChild/WordStudy.vue'
import WordRevise from '@/components/MainChild/WordRevise.vue'
import AccountSetting from '@/components/MeChild/AccountSetting'
import StudyCalendar from '@/components/MeChild/StudyCalendar'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/home',
    component: Home,
    redirect: '/main',
    children: [
      { path: '/main', component: Main },
      { path: '/me', component: Me },
      { path: '/word-list', component: WordList }
    ]
  },
  {
    path: '/calendar',
    component: StudyCalendar
  },
  {
    path: '/account-setting',
    component: AccountSetting
  },
  {
    path: '/ai-reading',
    component: AIReading
  },
  {
    path: '/word-study',
    component: WordStudy
  },
  {
    path: '/word-revise',
    component: WordRevise
  },
  {
    path: '/none',
    component: Notify
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

// 挂载路由导航守卫
router.beforeEach((to, from, next) => {
  // to 将要访问的路径
  // from 代表从哪个路径跳转过来
  // next 是一个函数，表示放行
  // next() 放行、next('/login')强制跳转
  if (to.path === '/login') return next()
  // 获取token
  const token = window.localStorage.getItem('token')
  if (!token) return next('/login')
  next()
})
export default router
