import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { teamsApi, matchesApi, registrationsApi } from "../services/api";
import MatchCard from "../components/MatchCard";

export default function TeamDetail() {
  const { id } = useParams();
  const [team, setTeam] = useState(null);
  const [matches, setMatches] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      teamsApi.get(id),
      matchesApi.list({ team_id: id, per_page: 6 }),
      registrationsApi.list({ team_id: id, per_page: 20 }),
    ])
      .then(([t, m, r]) => {
        setTeam(t.data);
        setMatches(m.data.data);
        setRegistrations(r.data.data);
      })
      .finally(() => setLoading(false));
  }, [id]);

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
