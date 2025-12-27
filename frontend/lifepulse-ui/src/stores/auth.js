import { defineStore } from "pinia"
import api from "../services/api"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    userId: localStorage.getItem("userId") || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email, password) {
      const res = await api.post("/auth/login", { email, password })

      this.token = res.data.access_token
      localStorage.setItem("token", this.token)

      // Decode JWT
      const payload = JSON.parse(atob(this.token.split(".")[1]))
      this.userId = payload.sub
      localStorage.setItem("userId", this.userId)
    },

    logout() {
      this.token = null
      this.userId = null
      localStorage.removeItem("token")
      localStorage.removeItem("userId")
    },
  },
})
