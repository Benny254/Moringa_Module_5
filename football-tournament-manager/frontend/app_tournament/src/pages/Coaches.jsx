import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { coachesApi } from "../services/api";
import Pagination from "../components/Pagination";

export default function Coaches() {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "manager";

  const [coaches, setCoaches] = useState([]);
  const [meta, setMeta] = useState({ page: 1, total_pages: 1 });
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: "", license_level: "", years_experience: "" });
  const [error, setError] = useState("");

  const load = (page = 1) => {
    setLoading(true);
    coachesApi.list({ page, per_page: 8 }).then((res) => {
      setCoaches(res.data.data);
      setMeta(res.data);
    }).finally(() => setLoading(false));
  };

  useEffect(() => { load(1); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await coachesApi.create({
        ...form,
        years_experience: form.years_experience ? Number(form.years_experience) : 0,
      });
      setShowForm(false);
      setForm({ name: "", license_level: "", years_experience: "" });
      load(1);
    } catch (err) {
      setError(err.response?.data?.errors ? JSON.stringify(err.response.data.errors) : "Could not add coach.");
    }
  };

  return (
    <div className="page container">
      <div className="page-head">
        <div>
          <p className="eyebrow">Touchline staff</p>
          <h1>Coaches</h1>
        </div>
        {canManage && (
          <button className="btn btn-primary" onClick={() => setShowForm((v) => !v)}>
            {showForm ? "Cancel" : "+ Add coach"}
          </button>
        )}
      </div>

      {showForm && (
        <form className="card stack" onSubmit={handleCreate} style={{ marginBottom: 28 }}>
          <div className="grid-2">
            <div className="field">
              <label>Name</label>
              <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>
            <div className="field">
              <label>License level</label>
              <input value={form.license_level} onChange={(e) => setForm({ ...form, license_level: e.target.value })} placeholder="UEFA A" />
            </div>
            <div className="field">
              <label>Years experience</label>
              <input type="number" value={form.years_experience} onChange={(e) => setForm({ ...form, years_experience: e.target.value })} />
            </div>
          </div>
          {error && <p className="error-text">{error}</p>}
          <button className="btn btn-primary" type="submit" style={{ alignSelf: "flex-start" }}>
            Save coach
          </button>
        </form>
      )}

      {loading ? (
        <div className="loading-state">Loading coaches…</div>
      ) : coaches.length === 0 ? (
        <div className="empty-state card"><h3>No coaches yet</h3></div>
      ) : (
        <>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Name</th><th>License</th><th>Experience</th><th>Teams</th></tr>
              </thead>
              <tbody>
                {coaches.map((c) => (
                  <tr key={c.id}>
                    <td>{c.name}</td>
                    <td>{c.license_level || "—"}</td>
                    <td className="mono">{c.years_experience} yrs</td>
                    <td>{c.teams?.map((t) => t.name).join(", ") || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <Pagination page={meta.page} totalPages={meta.total_pages} onChange={load} />
        </>
      )}
    </div>
  );
}
