import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { teamsApi, coachesApi } from "../services/api";
import TeamCard from "../components/TeamCard";
import Pagination from "../components/Pagination";

export default function Teams() {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "manager";

  const [teams, setTeams] = useState([]);
  const [coaches, setCoaches] = useState([]);
  const [meta, setMeta] = useState({ page: 1, total_pages: 1 });
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: "", short_code: "", city: "", founded_year: "", coach_id: "" });
  const [error, setError] = useState("");

  const loadTeams = (page = 1) => {
    setLoading(true);
    teamsApi
      .list({ page, per_page: 8 })
      .then((res) => {
        setTeams(res.data.data);
        setMeta(res.data);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadTeams(1);
    coachesApi.list({ per_page: 100 }).then((res) => setCoaches(res.data.data));
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await teamsApi.create({
        ...form,
        founded_year: form.founded_year ? Number(form.founded_year) : null,
        coach_id: form.coach_id ? Number(form.coach_id) : null,
      });
      setShowForm(false);
      setForm({ name: "", short_code: "", city: "", founded_year: "", coach_id: "" });
      loadTeams(1);
    } catch (err) {
      setError(err.response?.data?.errors ? JSON.stringify(err.response.data.errors) : "Could not create team.");
    }
  };

  return (
    <div className="page container">
      <div className="page-head">
        <div>
          <p className="eyebrow">Squad registry</p>
          <h1>Teams</h1>
        </div>
        {canManage && (
          <button className="btn btn-primary" onClick={() => setShowForm((v) => !v)}>
            {showForm ? "Cancel" : "+ Add team"}
          </button>
        )}
      </div>

      {showForm && (
        <form className="card stack" onSubmit={handleCreate} style={{ marginBottom: 28 }}>
          <div className="grid-2">
            <div className="field">
              <label>Team name</label>
              <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>
            <div className="field">
              <label>Short code</label>
              <input value={form.short_code} onChange={(e) => setForm({ ...form, short_code: e.target.value })} maxLength={10} />
            </div>
            <div className="field">
              <label>City</label>
              <input value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
            </div>
            <div className="field">
              <label>Founded year</label>
              <input type="number" value={form.founded_year} onChange={(e) => setForm({ ...form, founded_year: e.target.value })} />
            </div>
            <div className="field">
              <label>Coach</label>
              <select value={form.coach_id} onChange={(e) => setForm({ ...form, coach_id: e.target.value })}>
                <option value="">Unassigned</option>
                {coaches.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          </div>
          {error && <p className="error-text">{error}</p>}
          <button className="btn btn-primary" type="submit" style={{ alignSelf: "flex-start" }}>
            Save team
          </button>
        </form>
      )}

      {loading ? (
        <div className="loading-state">Loading teams…</div>
      ) : teams.length === 0 ? (
        <div className="empty-state card">
          <h3>No teams yet</h3>
          <p>Add your first team to get started.</p>
        </div>
      ) : (
        <>
          <div className="grid-2">
            {teams.map((t) => <TeamCard key={t.id} team={t} />)}
          </div>
          <Pagination page={meta.page} totalPages={meta.total_pages} onChange={loadTeams} />
        </>
      )}
    </div>
  );
}
