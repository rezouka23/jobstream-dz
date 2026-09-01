"""Google Sheets authentication and normalized row writer."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

from .schema import Job

SCOPES = ("https://www.googleapis.com/auth/spreadsheets",)


def credentials_from_env() -> Any:
    try:
        from google.oauth2.service_account import Credentials
    except ImportError as exc:
        raise RuntimeError("Google Sheets dependencies are not installed") from exc

    json_value = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    file_value = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "").strip()
    if bool(json_value) == bool(file_value):
        raise ValueError(
            "Set exactly one of GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_SERVICE_ACCOUNT_FILE"
        )
    if json_value:
        try:
            info = json.loads(json_value)
        except json.JSONDecodeError as exc:
            raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON") from exc
        if not isinstance(info, dict):
            raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON must contain an object")
        return Credentials.from_service_account_info(info, scopes=SCOPES)

    credential_path = Path(file_value).expanduser()
    if not credential_path.is_file():
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_FILE does not point to a readable file")
    return Credentials.from_service_account_file(str(credential_path), scopes=SCOPES)


def build_sheets_service() -> Any:
    try:
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise RuntimeError("Google Sheets dependencies are not installed") from exc
    return build("sheets", "v4", credentials=credentials_from_env(), cache_discovery=False)


def _quote_sheet_name(name: str) -> str:
    return "'" + name.replace("'", "''") + "'"


class GoogleSheetsWriter:
    def __init__(self, service: Any, spreadsheet_id: str, sheet_name: str):
        if not spreadsheet_id:
            raise ValueError("spreadsheet_id is required")
        self.service = service
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name

    def ensure_sheet(self) -> int:
        resource = self.service.spreadsheets()
        metadata = resource.get(
            spreadsheetId=self.spreadsheet_id,
            fields="sheets.properties(sheetId,title)",
        ).execute()
        for sheet in metadata.get("sheets", []):
            properties = sheet.get("properties", {})
            if properties.get("title") == self.sheet_name:
                sheet_id = int(properties["sheetId"])
                break
        else:
            created = resource.batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={"requests": [{"addSheet": {"properties": {"title": self.sheet_name}}}]},
            ).execute()
            sheet_id = int(created["replies"][0]["addSheet"]["properties"]["sheetId"])
        self._ensure_header()
        return sheet_id

    def _ensure_header(self) -> None:
        range_name = f"{_quote_sheet_name(self.sheet_name)}!1:1"
        values_resource = self.service.spreadsheets().values()
        result = values_resource.get(
            spreadsheetId=self.spreadsheet_id, range=range_name
        ).execute()
        existing = (result.get("values") or [[]])[0]
        expected = list(Job.HEADERS)
        if existing and existing != expected:
            raise RuntimeError(
                f"Sheet {self.sheet_name!r} has an incompatible header; refusing to overwrite it"
            )
        if not existing:
            values_resource.update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{_quote_sheet_name(self.sheet_name)}!A1",
                valueInputOption="RAW",
                body={"values": [expected]},
            ).execute()

    def write(self, jobs: Iterable[Job]) -> int:
        materialized = [job.with_added_at() for job in jobs]
        if not materialized:
            return 0
        sheet_id = self.ensure_sheet()
        rows = [
            {"values": [{"userEnteredValue": {"stringValue": value}} for value in job.as_row()]}
            for job in materialized
        ]
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={"requests": [
                {"insertDimension": {"range": {
                    "sheetId": sheet_id, "dimension": "ROWS",
                    "startIndex": 1, "endIndex": 1 + len(rows),
                }, "inheritFromBefore": False}},
                {"updateCells": {
                    "start": {"sheetId": sheet_id, "rowIndex": 1, "columnIndex": 0},
                    "rows": rows,
                    "fields": "userEnteredValue",
                }},
            ]},
        ).execute()
        return len(rows)
