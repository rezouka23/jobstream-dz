# JobStream DZ Open-Source Design

## Scope
JobStream DZ is a self-hosted Algeria-focused job aggregation project. It includes multi-source scraping, normalized Google Sheets storage, a FastAPI read API, a public landing page, and optional OpenAI-powered CV matching.

## Architecture
- `jobstream/scraper/`: source adapters, normalization, deduplication, Sheets writer, and scheduler.
- `jobstream/api.py`: health, recent feed, jobs, and CV Match endpoints.
- `jobstream/sheets.py`: shared Google Sheets authentication, reads, writes, URL normalization, and fingerprints.
- `landing/`: multilingual public landing and live job feed.
- `cv-match/`: multilingual CV upload and ranked match results.

## Data Flow
1. Scraper adapters fetch jobs from supported public sources.
2. Jobs normalize to one schema and deduplicate using stable provider IDs.
3. New rows are written to a configured Google Sheet.
4. FastAPI reads recent rows from that sheet.
5. Landing renders recent jobs from `/api/feed/latest`.
6. CV Match extracts a candidate profile with OpenAI and ranks recent sheet jobs locally.

## Security
- No credentials, production identifiers, uploaded CVs, or runtime state are committed.
- Google credentials load from `GOOGLE_SERVICE_ACCOUNT_FILE` or `GOOGLE_SERVICE_ACCOUNT_JSON`.
- OpenAI credentials load from `OPENAI_API_KEY`.
- CV uploads are processed in memory and rate-limited per client IP.
- Secret scanning is required before publication.

## Exclusions
- Telegram bot, client, publisher, digest persistence, and Telegram configuration.
- Production deployment scripts, server addresses, logs, snapshots, and private operational documentation.
- Generated media and local AI-agent configuration.

## Verification
- Unit tests for normalization, deduplication, date filtering, URL handling, and rate limiting.
- FastAPI route tests with external services mocked.
- JavaScript syntax checks for frontend assets.
- Compile checks for Python modules.
- Repository-wide secret pattern and tracked-file audits before push.
