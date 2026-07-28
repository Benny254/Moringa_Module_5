import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// ---------- Auth ----------
export const authApi = {
  login: (credentials) => api.post("/auth/login", credentials),
  register: (data) => api.post("/auth/register", data),
  me: () => api.get("/auth/me"),
  updateProfile: (data) => api.put("/auth/me", data),
};

// ---------- Users ----------
export const usersApi = {
  list: (params) => api.get("/users", { params }),
  get: (id) => api.get(`/users/${id}`),
  create: (data) => api.post("/users", data),
  update: (id, data) => api.put(`/users/${id}`, data),
  remove: (id) => api.delete(`/users/${id}`),
};

// ---------- Teams ----------
export const teamsApi = {
  list: (params) => api.get("/teams", { params }),
  get: (id) => api.get(`/teams/${id}`),
  create: (data) => api.post("/teams", data),
  update: (id, data) => api.put(`/teams/${id}`, data),
  remove: (id) => api.delete(`/teams/${id}`),
};

// ---------- Coaches ----------
export const coachesApi = {
  list: (params) => api.get("/coaches", { params }),
  get: (id) => api.get(`/coaches/${id}`),
  create: (data) => api.post("/coaches", data),
  update: (id, data) => api.put(`/coaches/${id}`, data),
  remove: (id) => api.delete(`/coaches/${id}`),
};

// ---------- Tournaments ----------
export const tournamentsApi = {
  list: (params) => api.get("/tournaments", { params }),
  get: (id) => api.get(`/tournaments/${id}`),
  create: (data) => api.post("/tournaments", data),
  update: (id, data) => api.put(`/tournaments/${id}`, data),
  remove: (id) => api.delete(`/tournaments/${id}`),
};

// ---------- Matches ----------
export const matchesApi = {
  list: (params) => api.get("/matches", { params }),
  get: (id) => api.get(`/matches/${id}`),
  create: (data) => api.post("/matches", data),
  update: (id, data) => api.put(`/matches/${id}`, data),
  remove: (id) => api.delete(`/matches/${id}`),
};

// ---------- Registrations ----------
export const registrationsApi = {
  list: (params) => api.get("/registrations", { params }),
  get: (id) => api.get(`/registrations/${id}`),
  create: (data) => api.post("/registrations", data),
  update: (id, data) => api.put(`/registrations/${id}`, data),
  remove: (id) => api.delete(`/registrations/${id}`),
};

// ---------- Reports ----------
export const reportsApi = {
  topTeams: (limit) => api.get("/reports/top-teams", { params: { limit } }),
  busyCoaches: (limit) => api.get("/reports/busy-coaches", { params: { limit } }),
  teamsInTournament: (tournamentId) => api.get(`/reports/tournaments/${tournamentId}/teams`),
};

export default api;