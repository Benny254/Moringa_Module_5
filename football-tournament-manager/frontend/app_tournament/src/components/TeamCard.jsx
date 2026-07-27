import { Link } from "react-router-dom";
import "../styles/cards.css";

export default function TeamCard({ team }) {
  return (
    <Link to={`/teams/${team.id}`} className="ticket-card">
      <div className="ticket-main">
        <p className="eyebrow">{team.short_code || "TEAM"}</p>
        <h3 className="ticket-name">{team.name}</h3>
        <p className="ticket-meta">
          {team.city || "Unknown city"} {team.founded_year ? `· Est. ${team.founded_year}` : ""}
        </p>
      </div>
      <div className="ticket-perforation" aria-hidden="true">
        {Array.from({ length: 8 }).map((_, i) => (
          <span key={i} className="ticket-dot" />
        ))}
      </div>
      <div className="ticket-stub">
        <p className="eyebrow">Coach</p>
        <p className="ticket-coach">{team.coach?.name || "Unassigned"}</p>
      </div>
    </Link>
  );
}
