import axios from "axios";
import Cookies from "js-cookie";
import { LoginRequest, AuthResponse } from "@/types/auth";

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
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = Cookies.get("refresh_token");
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/token/refresh/`,
          {
            refresh: refreshToken,
          }
        );
        const { access } = response.data;
        Cookies.set("access_token", access);
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (error) {
        Cookies.remove("access_token");
        Cookies.remove("refresh_token");
        window.location.href = "/login";
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

export const authService = {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await api.post("/login/", credentials);
    const { access, refresh, user_type } = response.data;
    Cookies.set("access_token", access);
    Cookies.set("refresh_token", refresh);
    Cookies.set("user_type", user_type);
    return response.data;
  },

  async register(data: any) {
    const response = await api.post("/register/", data);
    return response.data;
  },

  logout() {
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    Cookies.remove("user_type");
    window.location.href = "/login";
  },

  isAuthenticated(): boolean {
    return !!Cookies.get("access_token");
  },

  getUserType(): string | undefined {
    return Cookies.get("user_type");
  },
};

export default api;
