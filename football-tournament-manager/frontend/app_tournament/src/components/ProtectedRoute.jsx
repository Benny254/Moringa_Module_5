import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children, roles }) {
  const { user, loading, isAuthenticated } = useAuth();
  const location = useLocation();

  if (loading) {
    return <div className="loading-state">Loading…</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (roles && !roles.includes(user.role)) {
    return (
      <div className="page container">
        <div className="empty-state card">
          <h3>Restricted area</h3>
          <p>Your account doesn't have permission to view this page.</p>
        </div>
      </div>
    );
  }

  return children;
}
