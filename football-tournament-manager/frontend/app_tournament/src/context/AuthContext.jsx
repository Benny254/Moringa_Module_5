import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { authApi } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("pitchline_user");
    return stored ? JSON.parse(stored) : null;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("pitchline_token");
    if (!token) {
      setLoading(false);
      return;
    }
    authApi
      .me()
      .then((res) => {
        setUser(res.data);
        localStorage.setItem("pitchline_user", JSON.stringify(res.data));
      })
      .catch(() => {
        localStorage.removeItem("pitchline_token");
        localStorage.removeItem("pitchline_user");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (username, password) => {
    const res = await authApi.login({ username, password });
    localStorage.setItem("pitchline_token", res.data.access_token);
    localStorage.setItem("pitchline_user", JSON.stringify(res.data.user));
    setUser(res.data.user);
    return res.data.user;
  }, []);

  const register = useCallback(async (payload) => {
    const res = await authApi.register(payload);
    localStorage.setItem("pitchline_token", res.data.access_token);
    localStorage.setItem("pitchline_user", JSON.stringify(res.data.user));
    setUser(res.data.user);
    return res.data.user;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("pitchline_token");
    localStorage.removeItem("pitchline_user");
    setUser(null);
  }, []);

  const refreshUser = useCallback(async () => {
    const res = await authApi.me();
    setUser(res.data);
    localStorage.setItem("pitchline_user", JSON.stringify(res.data));
    return res.data;
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, loading, login, register, logout, refreshUser, isAuthenticated: !!user }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
