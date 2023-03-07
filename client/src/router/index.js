import { createRouter, createWebHashHistory } from 'vue-router';

// Views
import Home from '../views/Home.vue'
import Leaderboard from '../views/Leaderboard.vue'

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: Leaderboard
    },
    {
      path: "/:catchAll(.*)", // Unrecognized path automatically matches 404
      redirect: '/404',
    },
  ],
  linkActiveClass: 'active',
});
