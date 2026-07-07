# Placement Portal Application

Flask + Vue 3 + Bootstrap 5 + SQLite, with Redis caching and Celery (worker + beat) for background jobs.

## Prerequisites

- Python 3.12+
- Node.js 18+
- **Redis** — Windows has no official Redis build, so run it via **WSL2**:
  - `wsl --install -d Ubuntu-22.04` (one-time, if you don't already have a WSL distro)
  - Inside WSL: `sudo apt install redis-server` (skip if already installed — check with `redis-server --version`)
  - If you're on Mac/Linux natively, just `brew install redis` / `apt install redis-server` and skip the WSL wrapper commands below.

---

## 1. One-time setup

### Backend

```powershell
cd backend
python -m venv venv
venv\Scripts\pip install -r requirements.txt
copy .env.example .env
```

Open `backend/.env` and fill in the `MAIL_*` values — see **[SMTP setup](#smtp--email-setup)** below. Everything else in `.env.example` has sane local-dev defaults.

```powershell
set FLASK_APP=run.py
venv\Scripts\python -m flask db upgrade
venv\Scripts\python seed.py
```

This creates `instance/placement.db` and the default admin:
`admin@placement.com` / `admin123`

### Frontend

```powershell
cd frontend
npm install
copy .env.example .env
```

---

## 2. Running everything (5 processes, in order)

Open 5 terminals.

### Terminal 1 — Redis

```powershell
wsl -d Ubuntu-22.04 -e redis-server --port 6380 --bind 0.0.0.0 --protected-mode no
```

Leave this running. It binds to all interfaces on port 6380 so Windows processes (Flask, Celery) can reach it at `localhost:6380` — this project's `.env` is already pointed at that port to avoid clashing with WSL's own default Redis service on 6379, if you have one running.

> If you're on native Mac/Linux instead of WSL: just run `redis-server` normally and change `REDIS_URL` / `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` in `.env` to port `6379`.

### Terminal 2 — Backend (Flask API)

```powershell
cd backend
venv\Scripts\python run.py
```

Runs on `http://localhost:5000`. Health check: `http://localhost:5000/api/v1/health`

### Terminal 3 — Celery worker

```powershell
cd backend
venv\Scripts\celery -A celery_worker.celery worker --loglevel=info --pool=solo
```

`--pool=solo` is required on Windows (no `fork()` support). This process executes the background jobs: daily reminders, monthly report, async CSV export.

### Terminal 4 — Celery beat (scheduler)

```powershell
cd backend
venv\Scripts\celery -A celery_worker.celery beat --loglevel=info
```

Beat is what actually fires the scheduled jobs on time (daily reminders at 9:00 AM, monthly report on the 1st at 8:00 AM). Celery's embedded-beat flag (`-B`) doesn't work on Windows, which is why this runs as its own process, separate from the worker.

### Terminal 5 — Frontend

```powershell
cd frontend
npm run dev
```

Runs on `http://localhost:5173`. Open this in your browser.

---

## 3. Testing the scheduled jobs on demand

Beat only fires jobs on their real schedule (daily 9 AM / monthly on the 1st), which isn't convenient for a demo. To trigger a job immediately (with the worker from Terminal 3 already running), open a 6th terminal:

```powershell
cd backend
venv\Scripts\python
```

```python
from celery_worker import celery
from app.tasks.reminder_tasks import send_daily_deadline_reminders
from app.tasks.report_tasks import send_monthly_activity_report

send_daily_deadline_reminders.delay()
send_monthly_activity_report.delay()
```

Watch Terminal 3 (the worker) — you'll see the task received and its result logged there. Reminders also show up as in-app notifications (bell icon) for affected students regardless of whether SMTP is configured; the monthly report is email-only (goes to the admin's email).

The async CSV export (student dashboard → My Applications → Export CSV) works the same way — it's triggered from the UI, not manually.

---

## 4. SMTP / Email Setup

Two of the three background jobs send real email (daily deadline reminders, monthly admin report). Without SMTP configured, `EmailService` just logs what it *would have* sent — the app still works, you just won't get real emails. Pick one of these:

### Option A — Mailtrap (recommended for demo/viva)

Free email **sandbox** — nothing gets sent to real inboxes, so you can't accidentally spam anyone while testing, and you get a nice web UI to show the examiner the actual email content.

1. Sign up free at [mailtrap.io](https://mailtrap.io)
2. Go to **Email Testing → Inboxes → My Inbox**
3. Click **SMTP Settings**, choose "Flask" or just read the raw values
4. Copy into `backend/.env`:
   ```
   MAIL_SERVER=sandbox.smtp.mailtrap.io
   MAIL_PORT=2525
   MAIL_USE_TLS=true
   MAIL_USERNAME=<your mailtrap username>
   MAIL_PASSWORD=<your mailtrap password>
   MAIL_DEFAULT_SENDER=placements@example.com
   ```
5. Restart the backend + Celery worker. Every "sent" email now appears in your Mailtrap inbox instantly.

### Option B — Gmail App Password (real delivery)

Use this if you want the monthly report to actually land in your real inbox.

1. Your Google account needs **2-Step Verification** turned on first: [myaccount.google.com/security](https://myaccount.google.com/security)
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Create an app password — name it "Placement Portal", app type "Mail"
4. Google gives you a 16-character password (spaces don't matter, e.g. `abcd efgh ijkl mnop`)
5. Copy into `backend/.env`:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=youraddress@gmail.com
   MAIL_PASSWORD=abcdefghijklmnop
   MAIL_DEFAULT_SENDER=youraddress@gmail.com
   ```
   (Your normal Gmail login password will **not** work here — Google blocks that for SMTP. It has to be an App Password.)

### Option C — Brevo (formerly Sendinblue) free tier

Real delivery, 300 emails/day free, no sandbox limitation like Mailtrap.

1. Sign up free at [brevo.com](https://www.brevo.com)
2. Go to **SMTP & API → SMTP**
3. Copy the host (`smtp-relay.brevo.com`), port `587`, your login email, and the generated **SMTP key** (not your account password)
4. Same `.env` shape as above, with those values.

Any standard SMTP provider works the same way — the app just needs `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD` in `.env`.

---

## 5. Ports reference

| Service | Port |
|---|---|
| Frontend (Vite) | 5173 |
| Backend (Flask) | 5000 |
| Redis | 6380 (local WSL setup) |

## 6. Default admin

```
Email: admin@placement.com
Password: admin123
```
