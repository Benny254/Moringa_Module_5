import "../styles/cards.css";

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

function formatTime(iso) {
  const d = new Date(iso);
  return d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

export default function MatchCard({ match }) {
  const played = match.status === "completed";
  const live = match.status === "live";

  return (
    <div className="scoreboard-card">
      <div className="scoreboard-head">
        <span className="eyebrow" style={{ color: "var(--gold)" }}>
          {match.tournament?.name || "Fixture"}
        </span>
        <span className={`badge badge-${match.status}`}>{match.status}</span>
      </div>

      <div className="scoreboard-teams">
        <div className="scoreboard-team">
          <span className="scoreboard-team-name">{match.home_team?.name || "TBD"}</span>
        </div>

        <div className="scoreboard-score mono">
          {played || live ? (
            <>
              <span>{match.home_score ?? 0}</span>
              <span className="scoreboard-sep">:</span>
              <span>{match.away_score ?? 0}</span>
            </>
          ) : (
            <span className="scoreboard-vs">VS</span>
          )}
        </div>

        <div className="scoreboard-team scoreboard-team-away">
          <span className="scoreboard-team-name">{match.away_team?.name || "TBD"}</span>
        </div>
      </div>

      <div className="scoreboard-foot mono">
        <span>{formatDate(match.match_date)}</span>
        <span>{formatTime(match.match_date)}</span>
        <span>{match.venue || "Venue TBA"}</span>
      </div>
    </div>
  );
}
