import unittest
from datetime import datetime, timezone

from jobstream.scraper.schema import Job
from jobstream.scraper.text import canonical_url, utc_parts


class SchemaTests(unittest.TestCase):
    def test_job_normalizes_text_html_url_and_provider_id(self):
        job = Job.create(
            source=" Emploitic ",
            job_id="42",
            title="  Python\nDeveloper ",
            company_name="Example &amp; Co",
            location="Algiers",
            job_url="HTTPS://Example.COM/jobs/42/?utm_source=test&trkInfo=private#details",
            description="<p>Build &amp; ship</p>",
        )

        self.assertEqual(job.title, "Python Developer")
        self.assertEqual(job.company_name, "Example & Co")
        self.assertEqual(job.job_url, "https://example.com/jobs/42")
        self.assertEqual(job.description, "Build & ship")
        self.assertEqual(job.provider_job_id, "emploitic:42")

    def test_missing_provider_id_uses_stable_fingerprint(self):
        values = {
            "source": "test",
            "title": "Analyst",
            "company_name": "ACME",
            "location": "Oran",
            "job_url": "https://example.test/job?utm_campaign=x",
        }
        first = Job.create(**values)
        second = Job.create(**values)

        self.assertEqual(first.provider_job_id, second.provider_job_id)
        self.assertTrue(first.provider_job_id.startswith("test:"))

    def test_row_has_fixed_header_order_and_utc_added_at(self):
        job = Job.create(source="test", job_id="1", title="Role")
        stamped = job.with_added_at(datetime(2026, 9, 1, 12, 30, tzinfo=timezone.utc))

        self.assertEqual(len(stamped.as_row()), len(Job.HEADERS))
        self.assertEqual(stamped.as_row()[Job.HEADERS.index("added_at")], "2026-09-01T12:30:00Z")

    def test_url_and_datetime_reject_invalid_values(self):
        self.assertEqual(canonical_url("javascript:alert(1)"), "")
        self.assertEqual(utc_parts("not-a-date"), ("Not specified", "Not specified"))


if __name__ == "__main__":
    unittest.main()
