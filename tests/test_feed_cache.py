from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest

from jobstreamdz.feed_cache import FeedUnavailable, PublicFeedCache


def payload(title="Initial"):
    return {
        "date": "2026-10-16", "generated_at": "2026-10-16T00:00:00Z",
        "jobs": [{"title": title, "arrival_at": "2026-10-16T00:00:00Z"}],
        "meta": {"skipped_outside_window": 0},
    }


def test_stale_feed_returns_without_waiting_and_deduplicates_refreshes():
    clock = [1000.0]
    started, release = Event(), Event()
    calls = []

    def load():
        calls.append(True)
        if len(calls) == 1:
            return payload()
        started.set()
        assert release.wait(3)
        return payload("Updated")

    cache = PublicFeedCache(load, clock=lambda: clock[0], ttl=10)
    assert cache.get()["jobs"][0]["title"] == "Initial"
    clock[0] += 11
    with ThreadPoolExecutor(max_workers=1) as pool:
        assert pool.submit(cache.get).result(timeout=0.5)["jobs"][0]["title"] == "Initial"
        assert started.wait(1)
        for _ in range(10):
            assert cache.get()["jobs"][0]["title"] == "Initial"
        assert len(calls) == 2
        release.set()
        # Refresh uses the same single-flight lock, so waiting here observes the
        # completed background refresh without another provider request.
        assert pool.submit(cache.refresh).result(timeout=2)["jobs"][0]["title"] == "Updated"
    assert len(calls) == 2


def test_snapshot_restores_after_restart_without_calling_provider(tmp_path):
    clock = [1000.0]
    path = tmp_path / "private" / "feed.json"
    cache = PublicFeedCache(lambda: payload(), snapshot_path=path, namespace="sheet-a", clock=lambda: clock[0])
    cache.refresh()
    assert path.stat().st_mode & 0o777 == 0o600

    def forbidden():
        raise AssertionError("Provider should not be called on a warm restart")

    restarted = PublicFeedCache(forbidden, snapshot_path=path, namespace="sheet-a", clock=lambda: clock[0])
    assert restarted.get() == payload()
    other_sheet = PublicFeedCache(forbidden, snapshot_path=path, namespace="sheet-b", clock=lambda: clock[0])
    with pytest.raises(FeedUnavailable):
        other_sheet.get()


def test_failed_refresh_preserves_data_but_does_not_serve_it_indefinitely():
    clock = [1000.0]
    fail = [False]
    calls = []

    def load():
        calls.append(True)
        if fail[0]:
            raise RuntimeError("Provider unavailable")
        return payload()

    cache = PublicFeedCache(load, clock=lambda: clock[0], ttl=10, max_stale=30)
    cache.refresh()
    fail[0] = True
    clock[0] += 11
    with pytest.raises(FeedUnavailable):
        cache.refresh()
    assert cache.get() == payload()
    assert len(calls) == 2
    clock[0] += 20
    with pytest.raises(FeedUnavailable):
        cache.get()


def test_invalid_snapshot_is_ignored(tmp_path):
    path = tmp_path / "feed.json"
    path.write_text('{"broken":true}')
    cache = PublicFeedCache(lambda: payload("Recovered"), snapshot_path=path)
    assert cache.get()["jobs"][0]["title"] == "Recovered"


def test_warmer_refreshes_without_waiting_for_a_visitor():
    first, second = Event(), Event()
    calls = []

    def load():
        calls.append(True)
        (first if len(calls) == 1 else second).set()
        return payload()

    cache = PublicFeedCache(load, ttl=0.03)
    try:
        cache.start()
        assert first.wait(1)
        assert second.wait(1)
        assert len(calls) >= 2
    finally:
        cache.stop()
