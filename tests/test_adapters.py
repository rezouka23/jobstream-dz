import unittest
from datetime import datetime, timezone

from jobstream.scraper.sources.emploitic import EmploiticAdapter
from jobstream.scraper.sources.jobindz import JobindzAdapter
from jobstream.scraper.sources.linkedin import LinkedInAdapter
from jobstream.scraper.sources.naukrigulf import NaukriGulfAdapter
from jobstream.scraper.sources.ouedkniss import OuedknissAdapter


class AdapterNormalizationTests(unittest.TestCase):
    def test_emploitic_normalization(self):
        job = EmploiticAdapter.normalize({
            "arn": "arn:emploitic:job:abc123",
            "title": "Backend Engineer",
            "alias": "backend-engineer",
            "publishedAt": "2026-09-01T08:15:00Z",
            "description": "<p>Python</p>",
            "company": {
                "name": "Example",
                "alias": "example",
                "sector": {"label": "Information Technology"},
            },
            "criteria": {
                "location": [{"label": "Alger"}, {"label": "Remote"}],
                "contractType": [{"label": "CDI"}],
            },
        })

        self.assertEqual(job.provider_job_id, "emploitic:abc123")
        self.assertEqual(job.location, "Alger | Remote")
        self.assertEqual(job.contract_type, "CDI")
        self.assertEqual(job.published_time_utc, "08:15:00")
        self.assertIn("information-technology/backend-engineer", job.job_url)

    def test_naukrigulf_normalization(self):
        job = NaukriGulfAdapter.normalize({
            "jobId": 99,
            "designation": "QA Engineer",
            "company": {"name": "Quality Co"},
            "location": "Algeria",
            "experience": {"min": 2, "max": 4},
            "latestPostedDate": 1788249600000,
            "jdURL": "/qa-engineer-jobs-99",
            "description": "<b>Test software</b>",
        })

        self.assertEqual(job.provider_job_id, "naukrigulf:99")
        self.assertEqual(job.experience_years, "2-4 years")
        self.assertEqual(job.job_url, "https://www.naukrigulf.com/qa-engineer-jobs-99")

    def test_jobindz_page_parser(self):
        html = """
        <a href="/offre/data-analyst-321" class="offer-card">
          <h3 class="offer-title">Data Analyst</h3>
          <div class="offer-company">-</div>
          <div class="offer-date">Publié le 01/09/2026</div>
          <div class="meta-item"><i class="fa fa-map-marker-alt"></i><span>Oran</span></div>
          <div class="meta-item"><i class="fa fa-briefcase"></i><span>Data</span></div>
          <div class="meta-item"><i class="fa fa-file-contract"></i><span>CDI</span></div>
          <div class="meta-item"><i class="fa fa-users"></i><span>2 postes</span></div>
        </a>
        <a href="/offres?page=3">3</a>
        """
        jobs, pages = JobindzAdapter.parse_page(html)

        self.assertEqual(pages, 3)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].company_name, "Anonymous employer")
        self.assertEqual(jobs[0].provider_job_id, "jobindz:321")
        self.assertEqual(jobs[0].open_positions, "2")

    def test_ouedkniss_normalization(self):
        job = OuedknissAdapter.normalize({
            "id": "88",
            "title": "Commercial",
            "slug": "commercial-alger",
            "createdAt": "2026-09-01T09:10:11+01:00",
            "description": "Vente",
            "cities": [{"name": "Alger"}, {"name": "Blida"}],
            "store": {"name": "Store DZ"},
            "category": {"slug": "emploi_offres-commerce"},
        })

        self.assertEqual(job.location, "Alger | Blida")
        self.assertEqual(job.sector, "commerce")
        self.assertEqual(job.published_time_utc, "08:10:11")
        self.assertTrue(job.job_url.endswith("commercial-alger-d88"))

    def test_linkedin_normalization_without_jobspy(self):
        job = LinkedInAdapter.normalize({
            "title": "Support Agent",
            "company": "Help Co",
            "location": "Algeria",
            "job_url": "https://www.linkedin.com/jobs/view/123456?trk=feed",
            "date_posted": datetime(2026, 9, 1, tzinfo=timezone.utc),
            "is_remote": True,
        })

        self.assertEqual(job.provider_job_id, "linkedin:123456")
        self.assertEqual(job.work_mode, "Remote")
        self.assertNotIn("trk=", job.job_url)

    def test_linkedin_missing_urls_do_not_collapse_distinct_jobs(self):
        first = LinkedInAdapter.normalize({"title": "Role A", "company": "One"})
        second = LinkedInAdapter.normalize({"title": "Role B", "company": "Two"})

        self.assertNotEqual(first.provider_job_id, second.provider_job_id)


if __name__ == "__main__":
    unittest.main()
