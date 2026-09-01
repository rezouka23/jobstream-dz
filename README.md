# JobStream DZ

JobStream DZ is a self-hosted job aggregation and CV matching application focused on Algeria. It collects listings from several job boards, normalizes and deduplicates them in Google Sheets, exposes a FastAPI service, and serves multilingual landing and CV Match interfaces.

## Features

- Scrapers for Emploitic, NaukriGulf, Jobindz, and Ouedkniss
- Optional LinkedIn collection through `python-jobspy`
- Stable job normalization and local deduplication state
- Google Sheets storage with environment-only credentials
- Recent-jobs API and multilingual live-feed frontend
- PDF, DOCX, and TXT CV parsing
- Optional OpenAI profile extraction with deterministic local job ranking
- In-memory CV processing and per-IP rate limiting

## Architecture

```text
jobstream/scraper/  Source adapters, normalization, deduplication, Sheets writer
jobstream/api.py    FastAPI routes and static frontend mounts
jobstream/sheets.py Read-only Sheets integration used by the API
landing/            Multilingual landing page and live job feed
cv-match/           Multilingual CV upload and matching interface
tests/              Unit and route tests
```

The scraper writes normalized rows to a Google Sheet. The API reads recent rows from that sheet for `/api/feed/latest`, `/api/jobs/today`, and `/api/cv/match`. The frontend is served directly by FastAPI.

## Requirements

- Python 3.11 or newer
- A Google Cloud service account with access to a Google Sheet
- An OpenAI API key only if CV Match is enabled

Respect each source website's terms, robots policy, and rate limits when running scrapers.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Share the target Google Sheet with the service-account email, then fill in `.env`. Use exactly one credential source:

```dotenv
GOOGLE_SERVICE_ACCOUNT_FILE=/absolute/path/to/service-account.json
```

or:

```dotenv
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

The API and scraper currently use separate variable names for the same Sheet. Set `SPREADSHEET_ID` and `GOOGLE_SPREADSHEET_ID` to the same value, and do the same for `SHEET_NAME` and `GOOGLE_SHEET_NAME`.

## Run The Scraper

Run one collection cycle:

```bash
python -m jobstream.scraper --once
```

Run continuously using `SCRAPER_INTERVAL_SECONDS`:

```bash
python -m jobstream.scraper --loop
```

The default sources are `emploitic,naukrigulf,jobindz,ouedkniss`. To enable LinkedIn, install the optional dependency and configure it:

```bash
pip install "python-jobspy>=1.1.80,<2"
```

```dotenv
SCRAPER_ENABLE_LINKEDIN=true
LINKEDIN_SEARCH_TERMS=software developer,customer support,marketing,finance
```

## Run The App

```bash
uvicorn jobstream.api:app --reload
```

Open `http://127.0.0.1:8000/`. Useful endpoints:

- `GET /healthz`
- `GET /api/feed/latest`
- `GET /api/jobs/today?days=1`
- `POST /api/cv/match` with a multipart field named `cv`
- `GET /docs` for OpenAPI documentation

CV Match requires `OPENAI_API_KEY`. Uploaded files are parsed in memory and are not persisted by this application.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
python -m compileall -q jobstream
node --check landing/script.js
node --check cv-match/script.js
```

## Security

- Never commit `.env` or service-account JSON files.
- Use a dedicated, least-privilege Google service account.
- Restrict and rotate API keys according to your provider's guidance.
- Put the API behind a trusted reverse proxy and configure forwarded-client-IP handling before relying on IP rate limits in production.
- Review CV processing and data-protection requirements applicable to your deployment.

See [`docs/design.md`](docs/design.md) for more implementation detail.

## License

MIT. See [`LICENSE`](LICENSE).
