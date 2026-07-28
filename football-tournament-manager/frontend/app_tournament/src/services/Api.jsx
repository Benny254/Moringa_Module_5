import axios from "axios";

// Base URL — override in a .env file with VITE_API_URL=http://localhost:5000/api
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT token (if present) to every outgoing request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle expired/invalid tokens globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      // Redirect to login if the token is invalid/expired
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// ---------- Auth ----------
export const authApi = {
  login: (credentials) => api.post("/auth/login", credentials),
  register: (data) => api.post("/auth/register", data),
  logout: () => api.post("/auth/logout"),
  getCurrentUser: () => api.get("/auth/me"),
};

// ---------- Users ----------
export const usersApi = {
  getAll: (params) => api.get("/users", { params }),
  getById: (id) => api.get(`/users/${id}`),
  create: (data) => api.post("/users", data),
  update: (id, data) => api.put(`/users/${id}`, data),
  delete: (id) => api.delete(`/users/${id}`),
};

// ---------- Teams ----------
export const teamsApi = {
  getAll: (params) => api.get("/teams", { params }),
  getById: (id) => api.get(`/teams/${id}`),
  create: (data) => api.post("/teams", data),
  update: (id, data) => api.put(`/teams/${id}`, data),
  delete: (id) => api.delete(`/teams/${id}`),
};

// ---------- Tournaments ----------
export const tournamentsApi = {
  getAll: (params) => api.get("/tournaments", { params }),
  getById: (id) => api.get(`/tournaments/${id}`),
  create: (data) => api.post("/tournaments", data),
  update: (id, data) => api.put(`/tournaments/${id}`, data),
  delete: (id) => api.delete(`/tournaments/${id}`),
};

// ---------- Matches / Fixtures ----------
export const matchesApi = {
  getAll: (params) => api.get("/matches", { params }),
  getById: (id) => api.get(`/matches/${id}`),
  create: (data) => api.post("/matches", data),
  update: (id, data) => api.put(`/matches/${id}`, data),
  delete: (id) => api.delete(`/matches/${id}`),
};

export default api;