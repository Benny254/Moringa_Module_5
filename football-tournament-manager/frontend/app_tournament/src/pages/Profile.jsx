import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { authApi } from "../services/api";

export default function Profile() {
  const { user, refreshUser } = useAuth();
  const [form, setForm] = useState({
    full_name: user?.profile?.full_name || "",
    bio: user?.profile?.bio || "",
    phone: user?.profile?.phone || "",
    country: user?.profile?.country || "",
  });
  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSaved(false);
    try {
      await authApi.updateProfile(form);
      await refreshUser();
      setSaved(true);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="page container" style={{ maxWidth: 640 }}>
      <div className="page-head">
        <div>
          <p className="eyebrow">Account</p>
          <h1>Your profile</h1>
        </div>
        <span className="badge badge-approved">{user?.role}</span>
      </div>

      <form className="card stack" onSubmit={handleSubmit}>
        <div className="field">
          <label>Username</label>
          <input value={user?.username} disabled />
        </div>
        <div className="field">
          <label>Email</label>
          <input value={user?.email} disabled />
        </div>
        <div className="field">
          <label>Full name</label>
          <input value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
        </div>
        <div className="field">
          <label>Bio</label>
          <textarea rows={3} value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })} />
        </div>
        <div className="grid-2">
          <div className="field">
            <label>Phone</label>
            <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          </div>
          <div className="field">
            <label>Country</label>
            <input value={form.country} onChange={(e) => setForm({ ...form, country: e.target.value })} />
          </div>
        </div>
        {saved && <p style={{ color: "var(--pitch-700)", fontSize: 14 }}>Profile updated.</p>}
        <button className="btn btn-primary" type="submit" disabled={saving} style={{ alignSelf: "flex-start" }}>
          {saving ? "Saving…" : "Save changes"}
        </button>
      </form>
    </div>
  );
}
