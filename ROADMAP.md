# Home Manager – 360° Feature + Logic + Design Master Plan

Phased roadmap aligned to your spec. **Bold** = done or in progress.

---

## 1️⃣ Core modules (foundation)

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 1.1 | Signup / Login | **Done** | Email + password |
| 1.2 | Password hashing | **Done** | Werkzeug |
| 1.3 | Forgot password | **Done** | UI + stub; wire Flask-Mail for real emails |
| 1.4 | Email verification | Roadmap | Token + verified_at on User; send link on signup |
| 1.5 | Multi-device login | Roadmap | Sessions table; list/revoke |
| 1.6 | Session management | Roadmap | Flask-Login session; optional DB sessions |
| 1.7 | Logout from all devices | Roadmap | Invalidate all sessions for user |
| 1.8 | User model | **Done** | name, email, role, home_id, created_at |
| 1.9 | Home model | **Done** | home_name, owner_id |
| 1.10 | Create home | **Done** | Post-signup flow |
| 1.11 | Invite members | **Done** | UI + stub; add invite token + email later |
| 1.12 | Roles & permissions | **Done** | owner/member/guest + permission matrix |
| 1.13 | Switch homes | Roadmap | home_id → current_home_id; multi-home join |

**Permission matrix (implemented):**

| Role   | Expenses   | Tasks      | Settings   |
|--------|------------|------------|------------|
| Owner  | Full       | Full       | Full       |
| Member | Add/View   | Add/View   | No         |
| Guest  | View only  | View       | No         |

---

## 2️⃣ Financial management

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 2.1 | Add / edit / delete expenses | **Done** | Home-scoped |
| 2.2 | Categories (Food, Rent, Travel) | **Done** | ExpenseCategory; default seed |
| 2.3 | Payment method (Cash, UPI, Card) | **Done** | On Expense |
| 2.4 | Paid by whom | **Done** | paid_by_user_id |
| 2.5 | Split expenses | Model done | ExpenseSplit; UI + algorithm next |
| 2.6 | Monthly summaries | Roadmap | Filter by month; aggregate by category |
| 2.7 | Filters & search | Roadmap | Query params; category, date range |
| 2.8 | Recurring expenses | **Done** | is_recurring on Expense; scheduler later |
| 2.9 | Income tracking | **Done** | Income model; add routes + UI |
| 2.10 | Monthly net balance | Roadmap | Income − expenses per month |
| 2.11 | Budgeting engine | **Done** | Budget model; add routes + alert logic |
| 2.12 | Budget alerts | Roadmap | if spent > limit → notify |
| 2.13 | Savings goals | Roadmap | Goal model + progress |

---

## 3️⃣ Task & life management

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 3.1 | Add tasks | **Done** | Home-scoped |
| 3.2 | Assign to member | **Done** | assigned_to_user_id; add dropdown in UI |
| 3.3 | Due dates | **Done** | due_date on Task; add input in UI |
| 3.4 | Priority | **Done** | priority (low/medium/high) |
| 3.5 | Status (todo / in-progress / done) | **Done** | status + toggle |
| 3.6 | Repeating chores | **Done** | is_repeating; scheduler later |
| 3.7 | Smart chore rotation | Roadmap | Assign to least-loaded member |

---

## 4️⃣ Notes, documents & assets

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 4.1 | Personal notes | **Done** | Notes per user |
| 4.2 | Shared notes | Roadmap | home_id + shared flag on Note |
| 4.3 | Rich text | Roadmap | WYSIWYG or Markdown |
| 4.4 | Tags & search | Roadmap | NoteTag; search by title/content |
| 4.5 | Document vault | Roadmap | Document model (file_path, expiry_date) |
| 4.6 | Upload PDFs/images | Roadmap | Storage (local/S3); secure access |
| 4.7 | Expiry reminders | Roadmap | Cron; notify before expiry |

---

## 5️⃣ Smart automation

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 5.1 | Notifications: budget exceeded | Roadmap | Trigger + channel (email/push/in-app) |
| 5.2 | Notifications: task overdue | Roadmap | Daily job; check due_date |
| 5.3 | Notifications: bill due | Roadmap | Document expiry + recurring bills |
| 5.4 | Notifications: new expense | Roadmap | Optional in-app/email |
| 5.5 | Channels: Email / Push / In-app | Roadmap | Flask-Mail; Web Push; in-app list |
| 5.6 | Recurring job scheduler | Roadmap | Celery or APScheduler/cron |
| 5.7 | Monthly rent / electricity / weekly cleaning | Roadmap | Recurring expense + task jobs |

---

## 6️⃣ Analytics & insights

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 6.1 | Dashboard KPIs | **Done** | Total spend, pending tasks, notes count |
| 6.2 | Monthly spend | Roadmap | Per-month total |
| 6.3 | Category-wise pie chart | Roadmap | Chart.js or similar |
| 6.4 | Savings rate | Roadmap | (Income − expenses) / Income |
| 6.5 | Task completion % | Roadmap | done / total per period |
| 6.6 | Predictive analytics | Roadmap | next_month_estimate = avg(last_3_months) |
| 6.7 | Budget suggestion | Roadmap | From history |

---

## 7️⃣ Security & reliability

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 7.1 | Password hashing | **Done** | Werkzeug (consider bcrypt later) |
| 7.2 | CSRF protection | Roadmap | Flask-WTF CSRF on forms |
| 7.3 | Rate limiting | Roadmap | Flask-Limiter on login/API |
| 7.4 | Role-based access control | **Done** | utils/permissions.py |
| 7.5 | Audit logs | Roadmap | AuditLog model: who, what, when, old/new |

---

## 8️⃣ Architecture upgrades

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 8.1 | RESTful APIs | Roadmap | /api/v1/expenses etc. |
| 8.2 | JWT authentication | Roadmap | For API + mobile |
| 8.3 | API versioning | Roadmap | /api/v1/ |
| 8.4 | Indexing & FKs | **Done** | FKs on models; add DB indexes for filters |
| 8.5 | Soft deletes | Roadmap | deleted_at on key models |
| 8.6 | Migrations | Roadmap | Flask-Migrate (Alembic) |
| 8.7 | Caching (Redis) | Roadmap | Cache dashboard metrics |

---

## 9️⃣ UI/UX improvements

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 9.1 | Dark mode | Roadmap | CSS vars + toggle |
| 9.2 | Mobile-first | Roadmap | Bootstrap already responsive |
| 9.3 | Keyboard shortcuts | Roadmap | e.g. N = new expense |
| 9.4 | Inline edits | Roadmap | Edit expense/task in place |
| 9.5 | Bulk actions | Roadmap | Select multiple; delete/mark done |
| 9.6 | Accessibility | Roadmap | ARIA, contrast, keyboard nav |

---

## 🔟 Monetization (optional)

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 10.1 | Free tier | — | Current scope |
| 10.2 | Premium analytics | Roadmap | Paywall on advanced charts |
| 10.3 | Family plans | Roadmap | Billing + seats |

---

## 1️⃣1️⃣ DevOps & quality

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 11.1 | Unit tests | Roadmap | pytest; models + permissions |
| 11.2 | Integration tests | Roadmap | Client; auth + CRUD |
| 11.3 | API tests | Roadmap | When API exists |
| 11.4 | CI/CD (GitHub Actions) | Roadmap | Lint, test, deploy on push |
| 11.5 | Logging & monitoring | Roadmap | Struct log; errors; metrics |

---

## 1️⃣2️⃣ Future tech

| # | Feature | Status | Notes |
|---|--------|--------|--------|
| 12.1 | AI expense categorization | Idea | ML or rules on title |
| 12.2 | Voice input | Idea | Alexa-style |
| 12.3 | WhatsApp bot | Idea | Twilio / API |
| 12.4 | Android / iOS apps | Idea | React Native / Flutter + API |
| 12.5 | Offline-first sync | Idea | PWA + sync |
| 12.6 | Blockchain audit | Idea | Overkill but cool |

---

## Implementation order (suggested)

1. **Done:** Core (User, Home, roles, permissions, expenses with category/payment, tasks with status/priority, notes).
2. **Next:** Income routes + UI; Budget routes + UI; budget alert (e.g. on dashboard when over).
3. **Then:** Split-expense UI + algorithm; monthly summaries + filters; dashboard charts.
4. **Then:** Notifications (email); recurring scheduler; invite-by-email.
5. **Then:** API + JWT; migrations; tests; CI/CD.

Use this file as the single source of truth for scope and status.
