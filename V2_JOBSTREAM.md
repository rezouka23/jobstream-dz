# JobStream DZ V2: Personalized Alerts

## Summary

Add personalized job alerts as the next major product feature. Users configure preferences on the website, connect via Telegram deep link, and receive private Telegram digests when enough matching published jobs accumulate.

## Key Changes

- Add a website preference flow for keywords, preferred locations, and whether remote work is acceptable.
- Use Telegram deep links to bind website preferences to a Telegram chat/user.
- Store subscriptions and sent-alert state in SQLite.
- Match only against jobs already published in trusted public digests.
- Deliver private Telegram alert digests when 3-5 matching unseen jobs accumulate for a user.
- Keep public channel publishing unchanged.

## Public Interfaces

- Add subscription endpoints to create/update preferences, generate Telegram connect links, and read subscription status.
- Add Telegram bot handling for `/start <token>` to confirm the user connection.
- Add a background matcher that scans published digest history and queues/sends personalized digests.

## Test Plan

- Preference creation and update.
- Telegram deep-link token confirmation.
- Keyword, location, and remote matching.
- No duplicate personalized sends to the same user.
- Partial match batches wait until threshold.
- Published-channel flow remains unchanged.

## Assumptions

- SQLite is acceptable for v1.
- Personalized alerts are private Telegram messages, not new public channel posts.
- Alert matching uses published digest history only.
- Demo/fallback jobs should not be used for personalized alerts.
