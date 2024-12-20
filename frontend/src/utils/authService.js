import axios from "axios";
import api from "../api";

// const API_URL = "http://localhost:8000/api/auth/";
// baseURL: import.meta.env.VITE_API_URL,
export const login = async (username, password) => {
  const response = await api.post("/api/token/", { username, password });
  if (response.data.access) {
    localStorage.setItem("access", response.data.access);
    localStorage.setItem("refresh", response.data.refresh);
  }
  return response.data;
};

export const refreshToken = async () => {
  const refresh = localStorage.getItem("refresh");
  const response = await api.post("/api/token/refresh/", { refresh });
  if (response.data.access) {
    localStorage.setItem("access", response.data.access);
  }
  return response.data;
};

export const getPermissions = async () => {
  const access = localStorage.getItem("access");
  const response = await api.get("/api/user-permissions/", {
    headers: { Authorization: `Bearer ${access}` },
  });
  return response.data.permissions;
};
