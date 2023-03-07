import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ShoppingList from '../views/ShoppingList.vue'

const router = createRouter({
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
      component: ShoppingList
    },
    {
      path: "/:catchAll(.*)", // Unrecognized path automatically matches 404
      redirect: '/404',
    },
  ],
  linkActiveClass: 'active',
});

export default router;
