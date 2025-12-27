// src/services/api.js
import axios from "axios"

const api = axios.create({
  baseURL: "https://lifepulse.omchat.ovh/api/v1",
})

api.interceptors.request.use((config) => {
  // ✅ MUST MATCH auth store
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
