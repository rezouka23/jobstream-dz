from jobstreamdz.sheets import fetch_sheet_rows


def test_public_feed_omits_descriptions_and_preserves_sparse_rows_and_headers():
    headers = ["title", "company_name", "sector", "location", "contract_type",
               "education_level", "experience_years", "job_level", "profession",
               "open_positions", "work_mode", "published_date", "published_time_utc",
               "job_alias", "job_id", "job_url"]
    calls = []

    class Fake:
        def spreadsheets(self):
            return self

        def values(self):
            return self

        def batchGet(self, **kwargs):
            calls.append(kwargs)
            return self

        def execute(self):
            return {"valueRanges": [
                {"values": [headers, ["Sparse job"], ["Other job"]]},
                {"values": [["source", "provider_job_id", "added_at"],
                            ["linkedin", "linkedin:1", "2026-10-16T00:00:00Z"]]},
            ]}

    rows = fetch_sheet_rows(Fake(), "test-sheet", "jobs", None, "Z", public_only=True)
    assert calls[0]["ranges"] == ["jobs!A1:P", "jobs!R1:Z"]
    assert len(rows) == 2
    assert rows[0]["title"] == "Sparse job"
    assert rows[0]["source"] == "linkedin"
    assert rows[0]["added_at"] == "2026-10-16T00:00:00Z"
    assert rows[1]["added_at"] == ""
    assert "description" not in rows[0]
