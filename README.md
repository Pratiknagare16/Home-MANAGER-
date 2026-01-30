# Home Manager Web App

Full-stack home management: **user + home (household)**, **expenses** (categories, payment method, paid-by), **tasks** (assign, priority, status), **notes**. Roles: owner / member / guest. Flask + SQLAlchemy + Bootstrap.

## Quick start

```bash
cd home_manager
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python init_db.py
python app.py
```

Open http://127.0.0.1:5000 → **Sign up** (name, email, password) → **Create your home** → Dashboard.

> **Schema change:** App now uses **email** (not username) for login and requires a **home** for dashboard/expenses/tasks. If you had an old database, delete `database.db` and run `python init_db.py` again.

## Routes

| Route | Description |
|-------|--------------|
| `/login` | Login (email + password) |
| `/signup` | Sign up |
| `/forgot-password` | Forgot password (stub; wire Flask-Mail for real emails) |
| `/create-home` | Create home (after signup) |
| `/dashboard` | Overview: total expenses, pending tasks, notes count, recent items |
| `/expenses` | Expenses: add (category, payment), list, delete (owner/member) |
| `/tasks` | Tasks: add, toggle, delete (owner/member); guest view-only |
| `/notes` | Notes: personal notes CRUD |
| `/home` | Home settings + members (owner only) |
| `/home/invite` | Invite member by email (stub; owner only) |

## Roles & permissions

| Role | Expenses | Tasks | Settings |
|------|----------|-------|----------|
| Owner | Full | Full | Full (invite, members) |
| Member | Add/View | Add/View | No |
| Guest | View only | View | No |

## Project layout

- `app.py` – Flask app, blueprints, login manager
- `config.py` – SECRET_KEY, DATABASE_URL (env-ready)
- `models/` – User, Home, Expense, ExpenseCategory, ExpenseSplit, Task, Note, Income, Budget
- `routes/` – auth, dashboard, homes, expenses, tasks, notes
- `utils/` – permissions, scope (home vs personal)
- `templates/` – Bootstrap 5; base, login, signup, create_home, forgot_password, dashboard, expenses, tasks, notes, home_settings, home_invite
- **ROADMAP.md** – 360° master plan (all features, status, next steps)

## Production

- Set `SECRET_KEY` and `DATABASE_URL` (e.g. PostgreSQL on Render/Railway).
- Use Gunicorn: `gunicorn -w 4 "app:app"`.
- Turn off `debug`.
- Configure Flask-Mail for forgot-password and invite emails.

## Roadmap

See **ROADMAP.md** for the full feature list: income, budgeting, split expenses, notifications, API, tests, CI/CD, and future ideas (AI categorization, WhatsApp, apps).
