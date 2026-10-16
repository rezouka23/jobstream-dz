from __future__ import annotations

from jobstreamdz.config import load_settings
from jobstreamdz.publisher import run


def _load_dotenv_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return
    load_dotenv()


def main() -> None:
    _load_dotenv_if_available()
    settings = load_settings()
    run(settings)


if __name__ == "__main__":
    main()
