import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { Menu, X, ShieldCheck } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import "../styles/navbar.css";

const links = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/teams", label: "Teams" },
  { to: "/tournaments", label: "Tournaments" },
  { to: "/matches", label: "Fixtures" },
  { to: "/coaches", label: "Coaches" },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    setOpen(false);
    navigate("/login");
  };

  return (
    <header className="navbar">
      <div className="container navbar-inner">
        <NavLink to="/" className="brand" onClick={() => setOpen(false)}>
          <span className="brand-mark" aria-hidden="true" />
          <span className="brand-name">Pitchline</span>
        </NavLink>

        <nav className={`nav-links ${open ? "nav-open" : ""}`}>
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.end}
              className={({ isActive }) => `nav-link ${isActive ? "nav-link-active" : ""}`}
              onClick={() => setOpen(false)}
            >
              {l.label}
            </NavLink>
          ))}
          {user?.role === "admin" && (
            <NavLink
              to="/admin"
              className={({ isActive }) => `nav-link ${isActive ? "nav-link-active" : ""}`}
              onClick={() => setOpen(false)}
            >
              <ShieldCheck size={14} style={{ marginRight: 4, verticalAlign: -2 }} />
              Admin
            </NavLink>
          )}
          <div className="nav-divider" />
          {isAuthenticated ? (
            <>
              <NavLink to="/profile" className="nav-link" onClick={() => setOpen(false)}>
                {user?.username}
              </NavLink>
              <button className="btn btn-outline btn-sm" onClick={handleLogout}>
                Log out
              </button>
            </>
          ) : (
            <NavLink to="/login" className="btn btn-primary btn-sm" onClick={() => setOpen(false)}>
              Log in
            </NavLink>
          )}
        </nav>

        <button
          className="nav-toggle"
          aria-label={open ? "Close menu" : "Open menu"}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>
    </header>
  );
}
