import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { matchesApi, teamsApi, tournamentsApi } from "../services/api";
import MatchCard from "../components/MatchCard";
import Pagination from "../components/Pagination";

export default function Matches() {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "manager";

  const [matches, setMatches] = useState([]);
  const [teams, setTeams] = useState([]);
  const [tournaments, setTournaments] = useState([]);
  const [meta, setMeta] = useState({ page: 1, total_pages: 1 });
  const [statusFilter, setStatusFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    tournament_id: "", home_team_id: "", away_team_id: "", match_date: "", venue: "",
  });
  const [error, setError] = useState("");

  const load = (page = 1, status = statusFilter) => {
    setLoading(true);
    matchesApi
      .list({ page, per_page: 8, ...(status ? { status } : {}) })
      .then((res) => {
        setMatches(res.data.data);
        setMeta(res.data);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load(1);
    teamsApi.list({ per_page: 100 }).then((res) => setTeams(res.data.data));
    tournamentsApi.list({ per_page: 100 }).then((res) => setTournaments(res.data.data));
  }, []);

  const handleFilter = (status) => {
    setStatusFilter(status);
    load(1, status);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await matchesApi.create({
        ...form,
        tournament_id: Number(form.tournament_id),
        home_team_id: Number(form.home_team_id),
        away_team_id: Number(form.away_team_id),
        match_date: new Date(form.match_date).toISOString(),
      });
      setShowForm(false);
      setForm({ tournament_id: "", home_team_id: "", away_team_id: "", match_date: "", venue: "" });
      load(1);
    } catch (err) {
      setError(err.response?.data?.errors ? JSON.stringify(err.response.data.errors) : (err.response?.data?.message || "Could not create fixture."));
    }
  };

  return (
    <div className="page container">
      <div className="page-head">
        <div>
          <p className="eyebrow">Kickoff schedule</p>
          <h1>Fixtures</h1>
        </div>
        {canManage && (
          <button className="btn btn-primary" onClick={() => setShowForm((v) => !v)}>
            {showForm ? "Cancel" : "+ Schedule fixture"}
          </button>
        )}
      </div>

      <div className="row" style={{ marginBottom: 24 }}>
        {["", "scheduled", "live", "completed"].map((s) => (
          <button
            key={s || "all"}
            className={`btn btn-sm ${statusFilter === s ? "btn-primary" : "btn-outline"}`}
            onClick={() => handleFilter(s)}
          >
            {s || "All"}
          </button>
        ))}
      </div>

      {showForm && (
        <form className="card stack" onSubmit={handleCreate} style={{ marginBottom: 28 }}>
          <div className="grid-2">
            <div className="field">
              <label>Tournament</label>
              <select required value={form.tournament_id} onChange={(e) => setForm({ ...form, tournament_id: e.target.value })}>
                <option value="">Select tournament</option>
                {tournaments.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
              </select>
            </div>
            <div className="field">
              <label>Venue</label>
              <input value={form.venue} onChange={(e) => setForm({ ...form, venue: e.target.value })} />
            </div>
            <div className="field">
              <label>Home team</label>
              <select required value={form.home_team_id} onChange={(e) => setForm({ ...form, home_team_id: e.target.value })}>
                <option value="">Select team</option>
                {teams.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
              </select>
            </div>
            <div className="field">
              <label>Away team</label>
              <select required value={form.away_team_id} onChange={(e) => setForm({ ...form, away_team_id: e.target.value })}>
                <option value="">Select team</option>
                {teams.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
              </select>
            </div>
            <div className="field">
              <label>Kickoff date &amp; time</label>
              <input type="datetime-local" required value={form.match_date} onChange={(e) => setForm({ ...form, match_date: e.target.value })} />
            </div>
          </div>
          {error && <p className="error-text">{error}</p>}
          <button className="btn btn-primary" type="submit" style={{ alignSelf: "flex-start" }}>
            Save fixture
          </button>
        </form>
      )}

      {loading ? (
        <div className="loading-state">Loading fixtures…</div>
      ) : matches.length === 0 ? (
        <div className="empty-state card">
          <h3>No fixtures found</h3>
        </div>
      ) : (
        <>
          <div className="grid-2">
            {matches.map((m) => <MatchCard key={m.id} match={m} />)}
          </div>
          <Pagination page={meta.page} totalPages={meta.total_pages} onChange={(p) => load(p)} />
        </>
      )}
    </div>
  );
}
