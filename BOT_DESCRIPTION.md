# JobStream DZ Bot - Multilingual Description, Features, and Frontend Plan

## 1) Bot Description (3 Languages)

### English
JobStream DZ Bot is an automated Telegram publishing bot that reads fresh job listings from a Google Sheet and posts them to the `@jobstream_dz` channel. It is designed to keep the channel clean, timely, and useful by publishing jobs in digest format, avoiding duplicates, and running continuously on a schedule.

### Francais
JobStream DZ Bot est un bot Telegram automatise qui lit les nouvelles offres d'emploi depuis une feuille Google Sheets et les publie dans le canal `@jobstream_dz`. Il est concu pour garder le canal propre, a jour et utile, grace a un format digest, une protection contre les doublons et une execution continue selon une frequence definie.

### العربية
بوت JobStream DZ هو بوت تيليجرام آلي يقرأ أحدث عروض العمل من Google Sheets وينشرها في قناة `@jobstream_dz`.
تم تصميمه ليحافظ على القناة منظمة ومحدثة ومفيدة عبر النشر بصيغة ملخص، ومنع التكرار، والعمل بشكل مستمر وفق جدول زمني.

---

## 2) Current Features

- Google Sheets integration using a service account (read-only scope for the wrapper).
- Multi-feed polling loop with configurable per-feed intervals (`POLL_SECONDS` for main, `REMOTE_POLL_SECONDS` for remote).
- Digest mode: one Telegram message containing exactly 5 jobs per batch.
- Full-batch mode (`REQUIRE_FULL_BATCH=true`): waits until at least 5 unseen jobs are available.
- Publish eligibility requires a usable apply URL (rows without a valid apply link are skipped).
- Dedicated remote digest template (`🏠 Télétravail: nouvelles opportunités`) sourced from the `remote` sheet tab and posted every 15 minutes.
- Duplicate prevention with persistent local state (`seen_telegram_jobs.json`).
- Fingerprint strategy for dedupe:
  - primary key from normalized `job_url`
  - fallback SHA1 hash from source, title, company, and location
- Successful Telegram publishes are persisted locally as immutable digest JSON files plus a latest snapshot file.
- Startup cycle support (`SINGLE_RUN=true` for one-shot testing).
- HTML-formatted Telegram messages with emojis and apply links.
- Retry handling for Telegram API failures and 429 rate limits.
- PM2-compatible runtime for process supervision and auto-restart.
- Public FastAPI feed endpoint (`GET /api/feed/latest`) backed by local digest snapshot storage.

---

## 3) Frontend Creation Plan

## Goal
Build a lightweight web dashboard to monitor bot activity, inspect queued/new jobs, and control basic operations safely.

## Phase 1 - MVP Dashboard (1-2 weeks)

### Scope
- Read-only operational dashboard.
- No direct editing of secrets from UI.

### Pages
1. Overview
   - Bot status (online/offline)
   - Last run time
   - Next run ETA
   - Last digest result (posted count)
2. Recent Digests
   - List of sent digest batches
   - Sent timestamps
   - Included job titles/links
3. Job Queue Insight
   - Fresh unseen jobs currently detected
   - Count until next publish threshold (e.g., 5 required)
4. Logs
   - Read recent runtime logs
   - Filter by level (INFO/WARN/ERROR)

### Suggested Stack
- Frontend: Next.js (React + TypeScript)
- Backend API: FastAPI (Python)
- Storage:
  - Keep existing `seen_telegram_jobs.json`
  - Use `digest_history/` immutable files + `latest_digest.json` snapshot for dashboard visibility

## Phase 2 - Control Features (1 week)

### Add actions
- Trigger one immediate cycle
- Pause/resume publishing
- Dry-run preview (show digest message without sending)

### Safety
- Simple admin authentication (password or SSO)
- CSRF protection and rate limiting for action endpoints
- Server-side validation for every action

## Phase 3 - Product Polish (1-2 weeks)

### UX and analytics
- Source distribution chart (jobs by source)
- Posting success rate and error trend
- Localized UI language toggle (EN/FR/AR)
- Mobile-first responsive layout

### Reliability upgrades
- Healthcheck endpoint for uptime monitoring
- Structured logs (JSON mode optional)
- Alerting hooks (Telegram admin alerts for repeated failures)

---

## 4) API Contract Needed for Frontend

To support the dashboard, expose these backend endpoints:

- `GET /api/status`
  - Returns process health, last cycle time, next cycle ETA, current config summary.
- `GET /api/digests?limit=20`
  - Returns recent digest batches with sent jobs.
- `GET /api/queue`
  - Returns unseen jobs count and sample rows.
- `GET /api/logs?lines=200`
  - Returns recent sanitized runtime logs.
- `POST /api/run-once`
  - Triggers one cycle manually.
- `POST /api/pause` and `POST /api/resume`
  - Toggles publish loop state.

---

## 5) Non-Functional Requirements

- Security: never expose bot token or service account private key in frontend responses.
- Performance: dashboard API should answer status endpoints in under 500 ms for normal load.
- Observability: every publish attempt should be traceable with timestamp and outcome.
- Recoverability: preserve dedupe and digest history across restarts.

---

## 6) Definition of Done for Frontend MVP

- Dashboard shows live status and latest digest information.
- Operator can see how many unseen jobs are pending.
- Operator can manually trigger one cycle from UI.
- All sensitive values remain server-side only.
- System is deployable with PM2 and includes startup documentation.
