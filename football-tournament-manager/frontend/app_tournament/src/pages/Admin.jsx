import { useEffect, useState } from "react";
import { usersApi } from "../services/api";
import Pagination from "../components/Pagination";

export default function Admin() {
  const [users, setUsers] = useState([]);
  const [meta, setMeta] = useState({ page: 1, total_pages: 1 });
  const [loading, setLoading] = useState(true);

  const load = (page = 1) => {
    setLoading(true);
    usersApi.list({ page, per_page: 10 }).then((res) => {
      setUsers(res.data.data);
      setMeta(res.data);
    }).finally(() => setLoading(false));
  };

  useEffect(() => { load(1); }, []);

  const handleRoleChange = async (id, role) => {
    await usersApi.update(id, { role });
    load(meta.page);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this user? This cannot be undone.")) return;
    await usersApi.remove(id);
    load(meta.page);
  };

  return (
    <div className="page container">
      <div className="page-head">
        <div>
          <p className="eyebrow">Administration</p>
          <h1>User management</h1>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading users…</div>
      ) : (
        <>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Username</th><th>Email</th><th>Role</th><th>Actions</th></tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id}>
                    <td>{u.username}</td>
                    <td>{u.email}</td>
                    <td>
                      <select value={u.role} onChange={(e) => handleRoleChange(u.id, e.target.value)}>
                        <option value="player">player</option>
                        <option value="manager">manager</option>
                        <option value="admin">admin</option>
                      </select>
                    </td>
                    <td>
                      <button className="btn btn-danger btn-sm" onClick={() => handleDelete(u.id)}>
                        Delete
                      </button>
                    </td>
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
