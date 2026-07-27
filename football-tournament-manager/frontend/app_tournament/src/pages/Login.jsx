import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/auth.css";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(form.username, form.password);
      const dest = location.state?.from?.pathname || "/";
      navigate(dest, { replace: true });
    } catch (err) {
      setError(err.response?.data?.message || "Invalid username or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-shell">
      <div className="auth-visual">
        <div className="auth-visual-content">
          <p className="auth-kicker">Pitchline</p>
          <h1 className="auth-headline">Run your tournament like matchday depends on it.</h1>
          <p className="auth-sub">
            Teams, coaches, fixtures and standings in one place — built for managers who
            don't have time to chase spreadsheets.
          </p>
        </div>
        <div className="auth-stats">
          <div>
            <div className="auth-stat-num mono">12+</div>
            <div className="auth-stat-label">Teams tracked</div>
          </div>
          <div>
            <div className="auth-stat-num mono">4</div>
            <div className="auth-stat-label">Active tournaments</div>
          </div>
          <div>
            <div className="auth-stat-num mono">30+</div>
            <div className="auth-stat-label">Fixtures scheduled</div>
          </div>
        </div>
      </div>

      <div className="auth-panel">
        <form className="auth-form" onSubmit={handleSubmit}>
          <h2>Welcome back</h2>
          <p className="form-sub">Log in to manage your tournaments.</p>

          <div className="stack">
            <div className="field">
              <label htmlFor="username">Username or email</label>
              <input
                id="username"
                type="text"
                required
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                autoComplete="username"
              />
            </div>
            <div className="field">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                required
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                autoComplete="current-password"
              />
            </div>
          </div>

          {error && <p className="error-text" style={{ marginBottom: 16 }}>{error}</p>}

          <button className="btn btn-primary" type="submit" disabled={loading} style={{ width: "100%" }}>
            {loading ? "Logging in…" : "Log in"}
          </button>

          <p className="auth-switch">
            New to Pitchline? <Link to="/register">Create an account</Link>
          </p>
          <p className="auth-switch" style={{ marginTop: 8, fontSize: 12 }}>
            Demo: admin / admin123 · manager / manager123
          </p>
        </form>
      </div>
    </div>
  );
}
