# Pitchline — Football Tournament Manager

Full-stack tournament management app: Flask + PostgreSQL REST API on the backend,
React (Vite) on the frontend. JWT auth, role-based access control, pagination,
and five advanced reporting queries.

```
football-tournament-manager/
├── backend/     Flask REST API
├── frontend/    React (Vite) SPA
└── README.md    You are here
```

---

## 1. Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL 14+ running locally (or a connection string to a hosted instance)
- git

---

## 2. Backend setup

Open a terminal in the project root, then:

```bash
cd backend

# create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# create your local Postgres database (run once, using psql or a GUI)
createdb tournament_db

# configure environment variables
cp .env.example .env
# then edit .env and set DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY

# initialize migrations and create tables
flask --app app db init
flask --app app db migrate -m "Initial migration"
flask --app app db upgrade

# seed the database with realistic sample data
python seed.py

# run the dev server
python app.py
```

The API will be live at `http://localhost:5000`. Health check:
`curl http://localhost:5000/api/health`

**Seeded logins:**
| username | password    | role    |
|----------|-------------|---------|
| admin    | admin123    | admin   |
| manager  | manager123  | manager |

Any other seeded user has password `password123` (role: player).

### Re-running migrations after model changes

```bash
flask --app app db migrate -m "Describe your change"
flask --app app db upgrade
```

---

## 3. Frontend setup

Open a **second terminal**, also in the project root:

```bash
cd frontend

# install dependencies
npm install

# configure the API URL
cp .env.example .env
# edit .env if your backend isn't on localhost:5000

# run the dev server
npm run dev
```

The app will be live at `http://localhost:5173` (Vite's default).

### Building for production

```bash
npm run build      # outputs to frontend/dist
npm run preview     # serve the production build locally to smoke-test it
```

---

## 4. Running both together

You need **two terminals** open at once:

```bash
# terminal 1
cd backend && source venv/bin/activate && python app.py

# terminal 2
cd frontend && npm run dev
```

Then visit `http://localhost:5173` and log in.

---

## 5. Git branches

The repo is initialized with `main` plus feature branches so you can track
work in isolation and merge as you go:

```bash
git branch
#   feature/backend-auth-rbac
#   feature/backend-models
#   feature/backend-reports
#   feature/frontend-pages
#   feature/frontend-scaffold
# * main
```

Typical workflow for your own changes:

```bash
git checkout feature/backend-models      # or any branch above
# ... make changes ...
git add -A
git commit -m "Describe your change"
git checkout main
git merge feature/backend-models
```

---

## 6. API reference (quick summary)

All endpoints are prefixed `/api`. Protected endpoints require
`Authorization: Bearer <token>` from `/auth/login` or `/auth/register`.

| Method | Path | Access | Description |
|---|---|---|---|
| POST | `/auth/register` | public | Create account, returns token |
| POST | `/auth/login` | public | Log in, returns token |
| GET/PUT | `/auth/me` | authenticated | View/update own profile |
| GET | `/teams` | public | Paginated team list |
| POST/PUT/DELETE | `/teams` | manager/admin | Manage teams |
| GET | `/coaches` | public | Paginated coach list |
| GET | `/tournaments` | public | Paginated tournament list |
| GET | `/registrations` | public | Filter by `team_id` / `tournament_id` |
| GET | `/matches` | public | Filter by `team_id` / `tournament_id` / `status` |
| GET | `/users` | admin | Paginated user list |
| GET | `/reports/tournaments/<id>/teams` | public | Teams in a tournament, by points |
| GET | `/reports/biggest-tournament` | public | Tournaments ranked by team count |
| GET | `/reports/busy-coaches?min_teams=1` | public | Coaches managing multiple teams |
| GET | `/reports/top-teams?limit=10` | public | Teams ranked by total points |
| GET | `/reports/recent-registrations?limit=10` | public | Most recent registrations |

Pagination params on list endpoints: `?page=1&per_page=10`.

---

## 7. Design notes

The frontend uses a football-specific visual identity rather than generic
defaults: a pitch-green/floodlight-gold palette, condensed athletic display
type (Oswald) paired with Inter for body text and JetBrains Mono for
scoreboard digits, ticket-stub team cards, and dark scoreboard-style match
cards. Fully responsive from mobile (with a slide-down nav drawer) through
desktop.
