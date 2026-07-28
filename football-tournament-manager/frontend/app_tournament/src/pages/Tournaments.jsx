import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { tournamentsApi } from "../services/api";
import Pagination from "../components/Pagination";

export default function Tournaments() {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "manager";

  const [tournaments, setTournaments] = useState([]);
  const [meta, setMeta] = useState({ page: 1, total_pages: 1 });
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: "", season: "", location: "", start_date: "", end_date: "", status: "upcoming" });
  const [error, setError] = useState("");

  const load = (page = 1) => {
    setLoading(true);
    tournamentsApi.list({ page, per_page: 8 }).then((res) => {
      setTournaments(res.data.data);
      setMeta(res.data);
    }).finally(() => setLoading(false));
  };

  useEffect(() => { load(1); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await tournamentsApi.create(form);
      setShowForm(false);
      setForm({ name: "", season: "", location: "", start_date: "", end_date: "", status: "upcoming" });
      load(1);
    } catch (err) {
      setError(err.response?.data?.errors ? JSON.stringify(err.response.data.errors) : "Could not create tournament.");
    }
  };

  return (
    <div className="page container">
      <div className="page-head">
        <div>
          <p className="eyebrow">Competitions</p>
          <h1>Tournaments</h1>
        </div>
        {canManage && (
          <button className="btn btn-primary" onClick={() => setShowForm((v) => !v)}>
            {showForm ? "Cancel" : "+ New tournament"}
          </button>
        )}
      </div>

      {showForm && (
        <form className="card stack" onSubmit={handleCreate} style={{ marginBottom: 28 }}>
          <div className="grid-2">
            <div className="field">
              <label>Name</label>
              <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>
            <div className="field">
              <label>Season</label>
              <input value={form.season} onChange={(e) => setForm({ ...form, season: e.target.value })} placeholder="2026" />
            </div>
            <div className="field">
              <label>Location</label>
              <input value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} />
            </div>
            <div className="field">
              <label>Status</label>
              <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                <option value="upcoming">Upcoming</option>
                <option value="ongoing">Ongoing</option>
                <option value="completed">Completed</option>
              </select>
            </div>
            <div className="field">
              <label>Start date</label>
              <input type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} />
            </div>
            <div className="field">
              <label>End date</label>
              <input type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} />
            </div>
          </div>
          {error && <p className="error-text">{error}</p>}
          <button className="btn btn-primary" type="submit" style={{ alignSelf: "flex-start" }}>
            Save tournament
          </button>
        </form>
      )}

      {loading ? (
        <div className="loading-state">Loading tournaments…</div>
      ) : tournaments.length === 0 ? (
        <div className="empty-state card">
          <h3>No tournaments yet</h3>
        </div>
      ) : (
        <>
          <div className="grid">
            {tournaments.map((t) => (
              <Link key={t.id} to={`/tournaments/${t.id}`} className="card" style={{ display: "block" }}>
                <span className={`badge badge-${t.status}`}>{t.status}</span>
                <h3 style={{ margin: "12px 0 4px", fontSize: 18 }}>{t.name}</h3>
                <p style={{ color: "var(--ink-soft)", fontSize: 13 }}>{t.season} · {t.location}</p>
              </Link>
            ))}
          </div>
          <Pagination page={meta.page} totalPages={meta.total_pages} onChange={load} />
        </>
      )}
    </div>
  );
}
