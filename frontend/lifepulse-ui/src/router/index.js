import { createRouter, createWebHistory } from "vue-router"
import Dashboard from "../views/Dashboard.vue"
import Login from "../views/Login.vue"
import { useAuthStore } from "../stores/auth"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: Login,
    },
    {
      path: "/",
      name: "dashboard",
      component: Dashboard,
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  // Not logged in → force login
  if (!auth.isAuthenticated && to.name !== "login") {
    return { name: "login" }
  }

  // Logged in → prevent going back to login
  if (auth.isAuthenticated && to.name === "login") {
    return { name: "dashboard" }
  }
})

export default router
