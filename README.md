# JobStream DZ Telegram Wrapper

This wrapper polls your existing Google Sheet and publishes fresh job digests to your Telegram channel.

Behavior implemented for your requested flow:
- publish in digest mode (one message containing exactly 5 jobs)
- main feed every 3 minutes + remote feed every 15 minutes
- avoid duplicate Telegram posts using local persisted state
- on startup, each feed publishes only if at least 5 unseen, link-eligible jobs exist

## How it works

1. Reads the freshest rows from configured sheet tabs (`SHEET_NAME` and `REMOTE_SHEET_NAME`).
2. Builds a stable fingerprint per job (`job_url` first, fallback hash of `source + title + company + location`).
3. Compares against local Telegram state (`seen_telegram_jobs.json`).
4. If unseen jobs with usable apply URLs count is at least 5, sends one digest with exactly 5 jobs.
5. Main and remote feeds have independent cadences and digest templates.
6. Persists each successful digest as immutable JSON plus a feed-specific latest snapshot.
7. Saves sent fingerprints so the same jobs are never reposted.

Remote digest format:
- Header: `🏠 Télétravail: nouvelles opportunités`
- Subheader: `Remote & flexible roles (posted every 15 minutes)`
- Per job: `🌍 Remote or 🏠 Télétravail`, title, company, location, apply link

## Requirements

- Python 3.10+
- A Telegram bot token (from BotFather)
- Bot added as admin in the target channel
- Google service account JSON (file path or JSON string)
- Google Sheet shared with service-account email

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure

Copy `.env.example` to `.env` and set your values.

Required variables:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `SPREADSHEET_ID`
- `OPENAI_API_KEY` (required only for CV matching)
- one of:
  - `GOOGLE_SERVICE_ACCOUNT_FILE`
  - `GOOGLE_SERVICE_ACCOUNT_JSON`

Recommended defaults are already set for:
- `SHEET_NAME=emploitic_jobs_all_algeria_clean`
- `POLL_SECONDS=180`
- `POST_LIMIT=5`
- `REQUIRE_FULL_BATCH=true`
- `REMOTE_ENABLED=true`
- `REMOTE_SHEET_NAME=remote`
- `REMOTE_POLL_SECONDS=900`
- `REMOTE_POST_LIMIT=5`
- `REMOTE_REQUIRE_FULL_BATCH=true`
- `REMOTE_DIGESTS_DIR=digest_history/remote`
- `REMOTE_LATEST_DIGEST_FILE=latest_remote_digest.json`
- `DIGESTS_DIR=digest_history`
- `LATEST_DIGEST_FILE=latest_digest.json`
- `CV_MATCH_MODEL=gpt-4o-mini`
- `CV_MATCH_DAYS=7`
- `CV_MATCH_MAX_ROWS=1000`
- `CV_MATCH_LIMIT=20`
- `CV_MATCH_MAX_FILE_MB=5`
- `CV_MATCH_TEXT_CHAR_LIMIT=12000`
- `CV_MATCH_RATE_LIMIT_REQUESTS=3`
- `CV_MATCH_RATE_LIMIT_WINDOW_SECONDS=3600`

## Run

```bash
source .venv/bin/activate
python main.py
```

Single cycle test:

```bash
SINGLE_RUN=true python main.py
```

## Run public API

Expose the latest persisted digest for the landing page:

```bash
source .venv/bin/activate
uvicorn jobstreamdz.api:app --host 0.0.0.0 --port 8000
```

Endpoints:
- `GET /healthz`
- `GET /api/feed/latest`
- `GET /api/jobs/today`
- `POST /api/cv/match`

`/api/feed/latest` reads `LATEST_DIGEST_FILE` (default: `latest_digest.json`) and returns the latest publishable digest (must contain exactly 5 jobs).

Landing page is also served by the same FastAPI app (same-origin API calls):
- `GET /` (redirects to `/landing/`)
- `GET /landing/`
- `GET /jobs-today/`
- `GET /cv-match/`

`/api/jobs/today` reads the main Google Sheet directly and returns jobs for
the Algeria-local day. It uses `added_at` / `scraped_at` when present and falls
back to `published_date` for older rows.

Pass `days=1..7` to return a recent Algeria-local window for frontend recency
filters, for example `/api/jobs/today?days=7`.

`/api/cv/match` accepts a multipart CV upload field named `cv` (`.pdf`,
`.docx`, or `.txt`, default 5 MB max). It extracts CV text server-side, uses
OpenAI to produce a structured candidate profile, and ranks matching offers from
the main sheet over the last 7 Algeria-local days. Uploaded CV files and raw CV
text are not stored. The endpoint is rate-limited per client IP before expensive
processing starts; by default each IP can make 3 requests per 3600-second window.
Set `CV_MATCH_RATE_LIMIT_REQUESTS=0` to disable the limiter.

## Deploy changed files

After the first server setup, deploy feature changes with rsync instead of
uploading the whole project again:

```bash
scripts/deploy-changed.sh
```

The default mode is a dry run. To apply the listed changes:

```bash
SSHPASS='server-password' scripts/deploy-changed.sh --apply
```

The script compares local files against `/opt/jobstreamdz` on
`45.154.98.205`, transfers only changed files, excludes secrets and runtime
state (`.env`, Google credentials, digest history, latest digest snapshots,
and Telegram state), skips local docs/agent skill metadata, and restarts PM2
only when Python code or dependencies changed.

## Telegram setup tips

- Public channel: use `@channel_username` as `TELEGRAM_CHAT_ID`
- Private channel: use numeric `-100...` id
- Ensure bot has posting permission in the channel

## Notes

- State is stored in `seen_telegram_jobs.json` by default.
- Main successful digest records are stored under `digest_history/` and mirrored to `latest_digest.json`.
- Remote successful digest records are stored under `digest_history/remote/` and mirrored to `latest_remote_digest.json`.
- Rows without a usable apply URL are skipped for Telegram publishing and landing-feed persistence.
- If you delete state file, old jobs can be posted again.
- Keep secrets in `.env`; do not commit credentials.
