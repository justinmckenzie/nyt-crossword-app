import { createRouter, createWebHashHistory } from "vue-router";

// Views
import Home from "../views/Home.vue";
import Leaderboard from "../views/Leaderboard.vue";
import LeaderboardAverages from "../views/LeaderboardAverages";

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/leaderboard",
      name: "leaderboard",
      component: Leaderboard,
    },
    {
      path: "/leaderboard-averages",
      name: "leaderboard averages",
      component: LeaderboardAverages,
    },
    {
      path: "/:catchAll(.*)", // Unrecognized path automatically matches 404
      redirect: "/404",
    },
  ],
  linkActiveClass: "active",
});
