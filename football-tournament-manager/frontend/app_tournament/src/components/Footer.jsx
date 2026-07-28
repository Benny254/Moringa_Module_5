export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <span>© {new Date().getFullYear()} Pitchline Tournament Manager</span>
        <span className="footer-tag">Built for coaches, captains &amp; commissioners</span>
      </div>
    </footer>
  );
}
