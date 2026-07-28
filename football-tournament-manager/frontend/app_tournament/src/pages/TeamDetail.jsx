import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { teamsApi, matchesApi, registrationsApi, playersApi } from "../services/api";
import MatchCard from "../components/MatchCard";

export default function TeamDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "manager";

  const [team, setTeam] = useState(null);
  const [matches, setMatches] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);

  const [showPlayerForm, setShowPlayerForm] = useState(false);
  const [playerForm, setPlayerForm] = useState({
    name: "", position: "", jersey_number: "", date_of_birth: "",
  });
  const [playerError, setPlayerError] = useState("");

  const loadPlayers = () => {
    playersApi.list({ team_id: id, per_page: 50 }).then((res) => setPlayers(res.data.data));
  };

  useEffect(() => {
    setLoading(true);
    Promise.all([
      teamsApi.get(id),
      matchesApi.list({ team_id: id, per_page: 6 }),
      registrationsApi.list({ team_id: id, per_page: 20 }),
      playersApi.list({ team_id: id, per_page: 50 }),
    ])
      .then(([t, m, r, p]) => {
        setTeam(t.data);
        setMatches(m.data.data);
        setRegistrations(r.data.data);
        setPlayers(p.data.data);
      })
      .finally(() => setLoading(false));
  }, [id]);

  const handleAddPlayer = async (e) => {
    e.preventDefault();
    setPlayerError("");
    try {
      await playersApi.create({
        ...playerForm,
        team_id: Number(id),
        jersey_number: playerForm.jersey_number ? Number(playerForm.jersey_number) : null,
        date_of_birth: playerForm.date_of_birth || null,
      });
      setShowPlayerForm(false);
      setPlayerForm({ name: "", position: "", jersey_number: "", date_of_birth: "" });
      loadPlayers();
    } catch (err) {
      setPlayerError(
        err.response?.data?.errors
          ? JSON.stringify(err.response.data.errors)
          : err.response?.data?.message || "Could not add player."
      );
    }
  };

  if (loading) return <div className="loading-state">Loading team…</div>;
  if (!team) return <div className="empty-state">Team not found.</div>;

  return (
    <div className="page container">
      <Link to="/teams" className="eyebrow" style={{ display: "inline-block", marginBottom: 12 }}>
        ← Back to teams
      </Link>

      <div className="page-head">
        <div>
          <p className="eyebrow">{team.short_code}</p>
          <h1>{team.name}</h1>
          <p style={{ color: "var(--ink-soft)" }}>
            {team.city} {team.founded_year ? `· Est. ${team.founded_year}` : ""} · Coach: {team.coach?.name || "Unassigned"}
          </p>
        </div>
      </div>

      <section className="stack" style={{ marginBottom: 32 }}>
        <div className="page-head" style={{ marginBottom: 0 }}>
          <h2 style={{ fontSize: 18 }}>Squad</h2>
          {canManage && (
            <button className="btn btn-primary btn-sm" onClick={() => setShowPlayerForm((v) => !v)}>
              {showPlayerForm ? "Cancel" : "+ Add player"}
            </button>
          )}
        </div>

        {showPlayerForm && (
          <form className="card stack" onSubmit={handleAddPlayer} style={{ marginTop: 16 }}>
            <div className="grid-2">
              <div className="field">
                <label>Name</label>
                <input
                  required
                  value={playerForm.name}
                  onChange={(e) => setPlayerForm({ ...playerForm, name: e.target.value })}
                />
              </div>
              <div className="field">
                <label>Position</label>
                <select
                  value={playerForm.position}
                  onChange={(e) => setPlayerForm({ ...playerForm, position: e.target.value })}
                >
                  <option value="">Select position</option>
                  <option value="Goalkeeper">Goalkeeper</option>
                  <option value="Defender">Defender</option>
                  <option value="Midfielder">Midfielder</option>
                  <option value="Forward">Forward</option>
                </select>
              </div>
              <div className="field">
                <label>Jersey number</label>
                <input
                  type="number"
                  value={playerForm.jersey_number}
                  onChange={(e) => setPlayerForm({ ...playerForm, jersey_number: e.target.value })}
                />
              </div>
              <div className="field">
                <label>Date of birth</label>
                <input
                  type="date"
                  value={playerForm.date_of_birth}
                  onChange={(e) => setPlayerForm({ ...playerForm, date_of_birth: e.target.value })}
                />
              </div>
            </div>
            {playerError && <p className="error-text">{playerError}</p>}
            <button className="btn btn-primary" type="submit" style={{ alignSelf: "flex-start" }}>
              Save player
            </button>
          </form>
        )}

        {players.length === 0 ? (
          <p style={{ color: "var(--ink-soft)" }}>No players added yet.</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>#</th><th>Name</th><th>Position</th><th>Date of birth</th></tr>
              </thead>
              <tbody>
                {players.map((p) => (
                  <tr key={p.id}>
                    <td className="mono">{p.jersey_number ?? "—"}</td>
                    <td>{p.name}</td>
                    <td>{p.position || "—"}</td>
                    <td className="mono">{p.date_of_birth || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="stack" style={{ marginBottom: 32 }}>
        <h2 style={{ fontSize: 18 }}>Registrations</h2>
        {registrations.length === 0 ? (
          <p style={{ color: "var(--ink-soft)" }}>Not registered for any tournament yet.</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Tournament</th><th>Status</th><th>Points</th></tr>
              </thead>
              <tbody>
                {registrations.map((r) => (
                  <tr key={r.id}>
                    <td>{r.tournament?.name}</td>
                    <td><span className={`badge badge-${r.status}`}>{r.status}</span></td>
                    <td className="mono">{r.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="stack">
        <h2 style={{ fontSize: 18 }}>Recent &amp; upcoming fixtures</h2>
        {matches.length === 0 ? (
          <p style={{ color: "var(--ink-soft)" }}>No fixtures scheduled.</p>
        ) : (
          <div className="grid-2">
            {matches.map((m) => <MatchCard key={m.id} match={m} />)}
          </div>
        )}
      </section>
    </div>
  );
}
