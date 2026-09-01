import tempfile
import unittest
from pathlib import Path

from jobstream.scraper.config import ScraperConfig
from jobstream.scraper.runner import run_once
from jobstream.scraper.schema import Job
from jobstream.scraper.state import JsonDedupState


def config(state_file: Path) -> ScraperConfig:
    return ScraperConfig(
        spreadsheet_id="unused-in-injected-test",
        sheet_name="jobs",
        state_file=state_file,
        interval_seconds=60,
        request_timeout=10,
        request_delay=0,
        sources=(),
        linkedin_search_terms=(),
        linkedin_hours_old=24,
        linkedin_results_wanted=10,
        linkedin_remote_only=False,
    )


class FakeAdapter:
    name = "fake"

    def __init__(self, jobs):
        self.jobs = jobs

    def fetch(self):
        return self.jobs


class FakeWriter:
    def __init__(self, fail=False):
        self.fail = fail
        self.jobs = []

    def write(self, jobs):
        self.jobs = list(jobs)
        if self.fail:
            raise RuntimeError("write failed")
        return len(self.jobs)


class StateAndRunnerTests(unittest.TestCase):
    def test_state_round_trip_merges_and_sorts_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            state = JsonDedupState(Path(directory) / "state.json")
            state.add(["source:2", "source:1"])
            state.add(["source:2", "source:3"])

            self.assertEqual(state.load(), {"source:1", "source:2", "source:3"})
            self.assertFalse(list(Path(directory).glob(".state.json.*")))

    def test_runner_deduplicates_state_and_current_cycle(self):
        with tempfile.TemporaryDirectory() as directory:
            state = JsonDedupState(Path(directory) / "state.json")
            state.add(["fake:old"])
            old = Job.create(source="fake", job_id="old", title="Old")
            new = Job.create(source="fake", job_id="new", title="New")
            writer = FakeWriter()

            result = run_once(
                config(state.path),
                adapters=[FakeAdapter([old, new, new])],
                writer=writer,
                state=state,
            )

            self.assertEqual(result.inserted, 1)
            self.assertEqual(result.duplicates, 2)
            self.assertEqual(writer.jobs, [new])
            self.assertEqual(state.load(), {"fake:old", "fake:new"})

    def test_failed_write_does_not_advance_state(self):
        with tempfile.TemporaryDirectory() as directory:
            state = JsonDedupState(Path(directory) / "state.json")
            job = Job.create(source="fake", job_id="new", title="New")

            with self.assertRaisesRegex(RuntimeError, "write failed"):
                run_once(
                    config(state.path),
                    adapters=[FakeAdapter([job])],
                    writer=FakeWriter(fail=True),
                    state=state,
                )

            self.assertEqual(state.load(), set())


if __name__ == "__main__":
    unittest.main()
