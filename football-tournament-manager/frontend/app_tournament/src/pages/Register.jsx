import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/auth.css";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", full_name: "", password: "" });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setLoading(true);
    try {
      await register(form);
      navigate("/", { replace: true });
    } catch (err) {
      const data = err.response?.data;
      if (data?.errors) {
        const flat = {};
        Object.entries(data.errors).forEach(([k, v]) => (flat[k] = Array.isArray(v) ? v[0] : v));
        setErrors(flat);
      } else {
        setErrors({ general: data?.message || "Registration failed." });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-shell">
      <div className="auth-visual">
        <div className="auth-visual-content">
          <p className="auth-kicker">Pitchline</p>
          <h1 className="auth-headline">Join the touchline.</h1>
          <p className="auth-sub">
            Register a player account to follow your team's fixtures, standings, and
            tournament progress in real time.
          </p>
        </div>
      </div>

      <div className="auth-panel">
        <form className="auth-form" onSubmit={handleSubmit}>
          <h2>Create your account</h2>
          <p className="form-sub">Takes less than a minute.</p>

          <div className="stack">
            <div className="field">
              <label htmlFor="full_name">Full name</label>
              <input
                id="full_name"
                type="text"
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
              />
            </div>
            <div className="field">
              <label htmlFor="reg-username">Username</label>
              <input
                id="reg-username"
                type="text"
                required
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
              />
              {errors.username && <span className="error-text">{errors.username}</span>}
            </div>
            <div className="field">
              <label htmlFor="reg-email">Email</label>
              <input
                id="reg-email"
                type="email"
                required
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
              {errors.email && <span className="error-text">{errors.email}</span>}
            </div>
            <div className="field">
              <label htmlFor="reg-password">Password</label>
              <input
                id="reg-password"
                type="password"
                required
                minLength={6}
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
              />
              {errors.password && <span className="error-text">{errors.password}</span>}
            </div>
          </div>

          {errors.general && <p className="error-text" style={{ marginBottom: 16 }}>{errors.general}</p>}

          <button className="btn btn-primary" type="submit" disabled={loading} style={{ width: "100%" }}>
            {loading ? "Creating account…" : "Create account"}
          </button>

          <p className="auth-switch">
            Already have an account? <Link to="/login">Log in</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
