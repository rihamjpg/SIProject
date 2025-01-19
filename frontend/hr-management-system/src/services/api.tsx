import axios from "axios";
import Cookies from "js-cookie";
import { ApiError } from "@/types/api";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = Cookies.get("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = Cookies.get("refresh_token");
      try {
        const { data } = await axios.post(
          `${import.meta.env.VITE_API_URL}/token/refresh/`,
          {
            refresh: refreshToken,
          }
        );
        Cookies.set("access_token", data.access);
        api.defaults.headers.Authorization = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        Cookies.remove("access_token");
        Cookies.remove("refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    const apiError: ApiError = {
      message: error.response?.data?.message || "Une erreur est survenue",
      status: error.response?.status || 500,
      errors: error.response?.data?.errors,
    };

    return Promise.reject(apiError);
  }
);

export default api;
