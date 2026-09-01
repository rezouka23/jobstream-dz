from __future__ import annotations

import json
import math
import re
import unicodedata
from typing import Any, Mapping


PROFILE_FIELDS = (
    "target_titles",
    "skills",
    "languages",
    "locations",
    "education",
    "industries",
    "keywords",
)
PROFILE_JSON_SCHEMA = {
    "name": "candidate_profile",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            **{
                field: {"type": "array", "items": {"type": "string"}}
                for field in PROFILE_FIELDS
            },
            "experience_years": {"type": ["number", "null"]},
        },
        "required": [*PROFILE_FIELDS, "experience_years"],
        "additionalProperties": False,
    },
}


class CVProfileError(RuntimeError):
    pass


def extract_candidate_profile(
    *, cv_text: str, api_key: str, model: str, text_char_limit: int
) -> dict[str, Any]:
    if not api_key:
        raise CVProfileError("OPENAI_API_KEY is not configured")

    try:
        from openai import OpenAI

        response = OpenAI(api_key=api_key, timeout=30).chat.completions.create(
            model=model,
            response_format={"type": "json_schema", "json_schema": PROFILE_JSON_SCHEMA},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract a concise job-search profile from the CV. Do not invent "
                        "missing facts. Use lowercase strings where practical."
                    ),
                },
                {"role": "user", "content": cv_text[:text_char_limit]},
            ],
        )
        content = response.choices[0].message.content if response.choices else ""
        profile = json.loads(content or "{}")
    except (json.JSONDecodeError, IndexError, AttributeError, TypeError) as exc:
        raise CVProfileError("OpenAI returned an invalid candidate profile") from exc
    except Exception as exc:
        raise CVProfileError("OpenAI profile extraction failed") from exc

    if not isinstance(profile, dict):
        raise CVProfileError("OpenAI returned an invalid candidate profile")
    return normalize_candidate_profile(profile)


def normalize_candidate_profile(profile: Mapping[str, Any]) -> dict[str, Any]:
    normalized = {field: _normalize_list(profile.get(field)) for field in PROFILE_FIELDS}
    experience = profile.get("experience_years")
    if isinstance(experience, str):
        match = re.search(r"\d+(?:\.\d+)?", experience)
        experience = float(match.group(0)) if match else None
    if isinstance(experience, (int, float)) and math.isfinite(float(experience)):
        normalized["experience_years"] = max(0, round(float(experience), 1))
    else:
        normalized["experience_years"] = None
    if not any(normalized[field] for field in PROFILE_FIELDS):
        raise CVProfileError("No usable profile data was extracted from the CV")
    return normalized


def rank_jobs_for_profile(
    *, profile: Mapping[str, Any], jobs: list[dict[str, str]], limit: int
) -> list[dict[str, Any]]:
    scored: list[dict[str, Any]] = []
    for job in jobs:
        score, reasons = score_job(profile, job)
        if score > 0:
            scored.append({**job, "score": score, "reasons": reasons})
    scored.sort(
        key=lambda item: (
            item["score"],
            item.get("added_at", ""),
            item.get("published_date", ""),
            item.get("id", ""),
        ),
        reverse=True,
    )
    return scored[: max(0, limit)]


def score_job(profile: Mapping[str, Any], job: Mapping[str, str]) -> tuple[int, list[str]]:
    haystacks = {
        "title": _normalize_text(job.get("title", "")),
        "profession": _normalize_text(job.get("profession", "")),
        "description": _normalize_text(job.get("description", "")),
        "sector": _normalize_text(job.get("sector", "")),
        "location": _normalize_text(job.get("location", "")),
        "education": _normalize_text(job.get("education_level", "")),
    }
    combined_role = " ".join((haystacks["title"], haystacks["profession"]))
    combined_search = " ".join(haystacks.values())
    score = 0
    reasons: list[str] = []

    title_matches = _find_matches(profile.get("target_titles", []), combined_role)
    if title_matches:
        score += 30
        reasons.append(_reason("Role matches", title_matches))

    skills = _unique_terms([*profile.get("skills", []), *profile.get("keywords", [])])
    skill_matches = _find_matches(skills, combined_search)
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

    experience_score, experience_reason = _experience_score(
        profile.get("experience_years"), job.get("experience_years", "")
    )
    score += experience_score
    if experience_reason:
        reasons.append(experience_reason)

    education_matches = _find_matches(profile.get("education", []), haystacks["education"])
    if education_matches:
        score += 5
        reasons.append(_reason("Education matches", education_matches[:2]))

    industries = _find_matches(profile.get("industries", []), haystacks["sector"])
    languages = _find_matches(profile.get("languages", []), combined_search)
    if industries or languages:
        score += 5
        reasons.append(_reason("Additional fit", [*industries[:2], *languages[:2]]))

    if job.get("arrival_date") or job.get("added_at"):
        score += 5
    score = min(100, score)
    if score and not reasons:
        reasons.append("Recent offer")
    return score, reasons[:5]


def _normalize_list(value: Any) -> list[str]:
    items = [value] if isinstance(value, str) else value if isinstance(value, list) else []
    normalized: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = str(item).strip().lower()
        if not text or text in {"not specified", "unknown", "n/a", "none", "null"}:
            continue
        if text not in seen:
            seen.add(text)
            normalized.append(text[:80])
    return normalized[:30]


def _normalize_text(value: Any) -> str:
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", text.lower()).strip()


def _unique_terms(terms: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for term in terms:
        normalized = _normalize_text(term)
        if len(normalized) >= 2 and normalized not in seen:
            seen.add(normalized)
            unique.append(term)
    return unique


def _find_matches(needles: Any, haystack: str) -> list[str]:
    matches: list[str] = []
    normalized_haystack = _normalize_text(haystack)
    for needle in needles if isinstance(needles, list) else []:
        normalized = _normalize_text(needle)
        if len(normalized) >= 2 and _term_matches(normalized, normalized_haystack):
            matches.append(str(needle))
    return matches


def _term_matches(needle: str, haystack: str) -> bool:
    if not needle or not haystack:
        return False
    if " " in needle or re.search(r"[^a-z0-9]", needle):
        return needle in haystack
    return re.search(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", haystack) is not None


def _reason(prefix: str, matches: list[str]) -> str:
    return f"{prefix}: {', '.join(str(match).strip() for match in matches[:4])}"


def _remote_compatible(profile: Mapping[str, Any], job: Mapping[str, str]) -> bool:
    preferences = _normalize_text(" ".join(profile.get("locations", [])))
    job_text = _normalize_text(
        " ".join((job.get("location", ""), job.get("work_mode", ""), job.get("title", "")))
    )
    return "remote" in preferences and any(
        token in job_text for token in ("remote", "teletravail", "work from home")
    )


def _experience_score(candidate_years: Any, job_experience: str) -> tuple[int, str]:
    if not isinstance(candidate_years, (int, float)):
        return 0, ""
    requirements = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", job_experience or "")]
    if requirements and float(candidate_years) + 0.5 >= min(requirements):
        return 10, f"Experience appears compatible ({candidate_years:g}+ years)"
    return 0, ""
