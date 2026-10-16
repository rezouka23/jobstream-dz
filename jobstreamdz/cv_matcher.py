from __future__ import annotations

import json
import math
import re
import unicodedata
from typing import Any


PROFILE_FIELDS = (
    "target_titles",
    "skills",
    "languages",
    "locations",
    "education",
    "industries",
    "keywords",
)


class CVProfileError(RuntimeError):
    pass


def extract_candidate_profile(*, cv_text: str, api_key: str, model: str, text_char_limit: int) -> dict[str, Any]:
    if not api_key:
        raise CVProfileError("OPENAI_API_KEY is not configured")

    prompt_text = cv_text[:text_char_limit]
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, timeout=30)
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract a concise job-search profile from a CV. Return only JSON. "
                        "Do not invent missing facts. Use lowercase strings where practical."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Return JSON with keys: target_titles, skills, languages, locations, "
                        "experience_years, education, industries, keywords. Arrays must contain short strings. "
                        "experience_years must be a number or null. CV:\n\n"
                        f"{prompt_text}"
                    ),
                },
            ],
        )
    except Exception as exc:
        raise CVProfileError("OpenAI profile extraction failed") from exc

    content = response.choices[0].message.content if response.choices else ""
    try:
        raw_profile = json.loads(content or "{}")
    except json.JSONDecodeError as exc:
        raise CVProfileError("OpenAI returned invalid profile JSON") from exc

    return normalize_candidate_profile(raw_profile)


def normalize_candidate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for field in PROFILE_FIELDS:
        normalized[field] = _normalize_list(profile.get(field))

    experience_years = profile.get("experience_years")
    if isinstance(experience_years, str):
        match = re.search(r"\d+(?:\.\d+)?", experience_years)
        experience_years = float(match.group(0)) if match else None
    if isinstance(experience_years, (int, float)) and math.isfinite(float(experience_years)):
        normalized["experience_years"] = max(0, round(float(experience_years), 1))
    else:
        normalized["experience_years"] = None

    if not any(normalized[field] for field in PROFILE_FIELDS):
        raise CVProfileError("No usable profile data was extracted from the CV")
    return normalized


def rank_jobs_for_profile(
    *, profile: dict[str, Any], jobs: list[dict[str, str]], limit: int
) -> list[dict[str, Any]]:
    scored: list[dict[str, Any]] = []
    for job in jobs:
        score, reasons = score_job(profile, job)
        if score < 15 and len(scored) >= limit:
            continue
        if score <= 0:
            continue
        scored.append({**job, "score": score, "reasons": reasons})

    scored.sort(key=lambda item: (item["score"], item.get("added_at", ""), item.get("published_date", "")), reverse=True)
    return scored[:limit]


def score_job(profile: dict[str, Any], job: dict[str, str]) -> tuple[int, list[str]]:
    haystacks = {
        "title": _normalize_text(job.get("title", "")),
        "profession": _normalize_text(job.get("profession", "")),
        "description": _normalize_text(job.get("description", "")),
        "sector": _normalize_text(job.get("sector", "")),
        "location": _normalize_text(job.get("location", "")),
        "education": _normalize_text(job.get("education_level", "")),
        "experience": _normalize_text(job.get("experience_years", "")),
    }
    combined_role = " ".join([haystacks["title"], haystacks["profession"]])
    combined_search = " ".join(haystacks.values())

    score = 0
    reasons: list[str] = []

    title_matches = _find_matches(profile.get("target_titles", []), combined_role)
    if title_matches:
        score += 30
        reasons.append(_reason("Role matches", title_matches))

    skill_terms = _unique_terms([*profile.get("skills", []), *profile.get("keywords", [])])
    skill_matches = _find_matches(skill_terms, combined_search)
    if skill_matches:
        score += min(30, 8 + len(skill_matches) * 6)
        reasons.append(_reason("Skills match", skill_matches[:4]))

    location_matches = _find_matches(profile.get("locations", []), haystacks["location"])
    if location_matches:
        score += 15
        reasons.append(_reason("Location matches", location_matches[:2]))
    elif _remote_compatible(profile, job):
        score += 12
        reasons.append("Remote preference appears compatible")

    experience_score, experience_reason = _experience_score(profile.get("experience_years"), job.get("experience_years", ""))
    score += experience_score
    if experience_reason:
        reasons.append(experience_reason)

    education_matches = _find_matches(profile.get("education", []), haystacks["education"])
    if education_matches:
        score += 5
        reasons.append(_reason("Education matches", education_matches[:2]))

    industry_matches = _find_matches(profile.get("industries", []), haystacks["sector"])
    language_matches = _find_matches(profile.get("languages", []), combined_search)
    if industry_matches or language_matches:
        score += 5
        reasons.append(_reason("Additional fit", [*industry_matches[:2], *language_matches[:2]]))

    if job.get("arrival_date") or job.get("added_at"):
        score += 5

    score = min(100, score)
    if score > 0 and not reasons:
        reasons.append("Recent offer from the last 7 days")
    return score, reasons[:5]


def _normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = value
    else:
        return []

    normalized: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = str(item).strip().lower()
        if not text or text in {"not specified", "unknown", "n/a", "none", "null"}:
            continue
        if text in seen:
            continue
        seen.add(text)
        normalized.append(text[:80])
    return normalized[:30]


def _normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", text.lower()).strip()


def _unique_terms(terms: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for term in terms:
        normalized = _normalize_text(term)
        if len(normalized) < 2 or normalized in seen:
            continue
        seen.add(normalized)
        unique.append(term)
    return unique


def _find_matches(needles: list[str], haystack: str) -> list[str]:
    matches: list[str] = []
    normalized_haystack = _normalize_text(haystack)
    for needle in needles:
        normalized_needle = _normalize_text(needle)
        if len(normalized_needle) < 2:
            continue
        if _term_matches(normalized_needle, normalized_haystack):
            matches.append(needle)
    return matches


def _term_matches(needle: str, haystack: str) -> bool:
    if not needle or not haystack:
        return False
    if " " in needle:
        return needle in haystack
    if re.search(r"[^a-z0-9]", needle):
        return needle in haystack
    return re.search(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", haystack) is not None


def _reason(prefix: str, matches: list[str]) -> str:
    cleaned = [str(match).strip() for match in matches if str(match).strip()]
    if not cleaned:
        return prefix
    return f"{prefix}: {', '.join(cleaned[:4])}"


def _remote_compatible(profile: dict[str, Any], job: dict[str, str]) -> bool:
    profile_locations = " ".join(profile.get("locations", []))
    job_text = " ".join([job.get("location", ""), job.get("work_mode", ""), job.get("title", "")])
    return "remote" in _normalize_text(profile_locations) and any(
        token in _normalize_text(job_text) for token in ("remote", "teletravail", "work from home")
    )


def _experience_score(candidate_years: Any, job_experience: str) -> tuple[int, str]:
    if not isinstance(candidate_years, (int, float)):
        return 0, ""
    numbers = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", str(job_experience or ""))]
    if not numbers:
        return 0, ""
    required = min(numbers)
    if float(candidate_years) + 0.5 >= required:
        return 10, f"Experience appears compatible ({candidate_years:g}+ years)"
    return 0, ""
