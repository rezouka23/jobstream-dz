from __future__ import annotations

import pytest

from jobstream.cv_parser import CVParseError, extract_cv_text


def test_extract_txt_normalizes_whitespace() -> None:
    assert extract_cv_text(
        filename="resume.TXT", data=b"Jane Doe\n\n  Python   FastAPI  "
    ) == "Jane Doe\nPython FastAPI"


def test_extract_txt_supports_utf16() -> None:
    assert extract_cv_text(filename="resume.txt", data="Developpeur".encode("utf-16")) == "Developpeur"


def test_extract_rejects_unsupported_or_empty_files() -> None:
    with pytest.raises(CVParseError, match="Unsupported CV format"):
        extract_cv_text(filename="resume.rtf", data=b"text")
    with pytest.raises(CVParseError, match="could not be read"):
        extract_cv_text(filename="resume.txt", data=b"  \n")
