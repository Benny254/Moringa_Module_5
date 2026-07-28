import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { tournamentsApi, matchesApi, reportsApi } from "../services/api";
import MatchCard from "../components/MatchCard";

export default function TournamentDetail() {
  const { id } = useParams();
  const [tournament, setTournament] = useState(null);
  const [standings, setStandings] = useState([]);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      tournamentsApi.get(id),
      reportsApi.teamsInTournament(id),
      matchesApi.list({ tournament_id: id, per_page: 12 }),
    ])
      .then(([t, s, m]) => {
        setTournament(t.data);
        setStandings(s.data.teams);
        setMatches(m.data.data);
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="loading-state">Loading tournament…</div>;
  if (!tournament) return <div className="empty-state">Tournament not found.</div>;

  return (
    <div className="page container">
      <Link to="/tournaments" className="eyebrow" style={{ display: "inline-block", marginBottom: 12 }}>
        ← Back to tournaments
      </Link>
      <div className="page-head">
        <div>
          <span className={`badge badge-${tournament.status}`}>{tournament.status}</span>
          <h1 style={{ marginTop: 10 }}>{tournament.name}</h1>
          <p style={{ color: "var(--ink-soft)" }}>{tournament.season} · {tournament.location}</p>
        </div>
      </div>

      <section className="stack" style={{ marginBottom: 32 }}>
        <h2 style={{ fontSize: 18 }}>Standings</h2>
        {standings.length === 0 ? (
          <p style={{ color: "var(--ink-soft)" }}>No teams registered yet.</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>#</th><th>Team</th><th>City</th><th>Status</th><th>Points</th></tr>
              </thead>
              <tbody>
                {standings.map((t, i) => (
                  <tr key={t.id}>
                    <td className="mono">{i + 1}</td>
                    <td>{t.name}</td>
                    <td>{t.city}</td>
                    <td><span className={`badge badge-${t.status}`}>{t.status}</span></td>
                    <td className="mono">{t.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="stack">
        <h2 style={{ fontSize: 18 }}>Fixtures</h2>
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
