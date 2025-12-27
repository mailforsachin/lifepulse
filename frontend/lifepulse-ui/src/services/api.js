// src/services/api.js
import axios from "axios"

const api = axios.create({
  baseURL: "https://lifepulse.omchat.ovh/api/v1",
  withCredentials: true,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token") // ✅ FIXED
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
