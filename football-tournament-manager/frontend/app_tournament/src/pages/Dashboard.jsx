import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { matchesApi, tournamentsApi, reportsApi } from "../services/api";
import MatchCard from "../components/MatchCard";

export default function Dashboard() {
  const { user } = useAuth();
  const [matches, setMatches] = useState([]);
  const [tournaments, setTournaments] = useState([]);
  const [topTeams, setTopTeams] = useState([]);
  const [busyCoaches, setBusyCoaches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    Promise.all([
      matchesApi.list({ per_page: 4 }),
      tournamentsApi.list({ per_page: 4 }),
      reportsApi.topTeams(5),
      reportsApi.busyCoaches(1),
    ])
      .then(([m, t, top, busy]) => {
        if (!mounted) return;
        setMatches(m.data.data);
        setTournaments(t.data.data);
        setTopTeams(top.data.teams);
        setBusyCoaches(busy.data.coaches);
      })
      .finally(() => mounted && setLoading(false));
    return () => (mounted = false);
  }, []);

  if (loading) return <div className="loading-state">Loading dashboard…</div>;

  return (
    <div className="page container">
      <div className="page-head">
        <div>
          <p className="eyebrow">Matchday overview</p>
          <h1>Welcome back, {user?.profile?.full_name || user?.username}</h1>
        </div>
        <Link to="/matches" className="btn btn-outline">View all fixtures</Link>
      </div>

      <section className="stack" style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 18 }}>Upcoming &amp; recent fixtures</h2>
        {matches.length === 0 ? (
          <div className="empty-state card">
            <h3>No fixtures yet</h3>
            <p>Once matches are scheduled, they'll show up here.</p>
          </div>
        ) : (
          <div className="grid-2">
            {matches.map((m) => <MatchCard key={m.id} match={m} />)}
          </div>
        )}
      </section>

      <div className="grid-2">
        <section className="card">
          <h2 style={{ fontSize: 16, marginBottom: 16 }}>Top teams by points</h2>
          <table>
            <thead>
              <tr><th>Team</th><th>Points</th></tr>
            </thead>
            <tbody>
              {topTeams.map((t) => (
                <tr key={t.id}>
                  <td>{t.name}</td>
                  <td className="mono">{t.total_points}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="card">
          <h2 style={{ fontSize: 16, marginBottom: 16 }}>Coaches managing multiple teams</h2>
          {busyCoaches.length === 0 ? (
            <p style={{ color: "var(--ink-soft)" }}>No coach currently manages more than one team.</p>
          ) : (
            <table>
              <thead>
                <tr><th>Coach</th><th>Teams</th></tr>
              </thead>
              <tbody>
                {busyCoaches.map((c) => (
                  <tr key={c.id}>
                    <td>{c.name}</td>
                    <td className="mono">{c.team_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </div>

      <section style={{ marginTop: 32 }}>
        <h2 style={{ fontSize: 18, marginBottom: 16 }}>Tournaments</h2>
        <div className="grid">
          {tournaments.map((t) => (
            <Link key={t.id} to={`/tournaments/${t.id}`} className="card" style={{ display: "block" }}>
              <span className={`badge badge-${t.status}`}>{t.status}</span>
              <h3 style={{ margin: "12px 0 4px", fontSize: 18 }}>{t.name}</h3>
              <p style={{ color: "var(--ink-soft)", fontSize: 13 }}>{t.season} · {t.location}</p>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
