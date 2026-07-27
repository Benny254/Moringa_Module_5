export default function Pagination({ page, totalPages, onChange }) {
  if (totalPages <= 1) return null;

  const pages = [];
  const start = Math.max(1, page - 2);
  const end = Math.min(totalPages, start + 4);

  for (let p = start; p <= end; p++) pages.push(p);

  return (
    <div className="pagination">
      <button onClick={() => onChange(page - 1)} disabled={page <= 1} aria-label="Previous page">
        ‹
      </button>
      {start > 1 && <span>…</span>}
      {pages.map((p) => (
        <button key={p} className={p === page ? "active" : ""} onClick={() => onChange(p)}>
          {p}
        </button>
      ))}
      {end < totalPages && <span>…</span>}
      <button onClick={() => onChange(page + 1)} disabled={page >= totalPages} aria-label="Next page">
        ›
      </button>
    </div>
  );
}
