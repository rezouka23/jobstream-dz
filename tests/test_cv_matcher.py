from __future__ import annotations

from jobstream.cv_matcher import normalize_candidate_profile, rank_jobs_for_profile, score_job


def test_profile_normalization_and_deterministic_ranking() -> None:
    profile = normalize_candidate_profile(
        {
            "target_titles": ["Backend Developer", "backend developer"],
            "skills": ["Python", "FastAPI"],
            "languages": ["French"],
            "locations": ["Algiers"],
            "experience_years": "3 years",
            "education": [],
            "industries": ["Software"],
            "keywords": [],
        }
    )
    jobs = [
        {
            "id": "weaker",
            "title": "Office Assistant",
            "description": "French speaking team",
            "location": "Algiers",
            "arrival_date": "2026-09-01",
        },
        {
            "id": "stronger",
            "title": "Backend Developer",
            "description": "Python and FastAPI services",
            "location": "Algiers",
            "sector": "Software",
            "experience_years": "2 years",
            "arrival_date": "2026-09-01",
        },
    ]

    ranked = rank_jobs_for_profile(profile=profile, jobs=jobs, limit=2)

    assert profile["experience_years"] == 3.0
    assert profile["target_titles"] == ["backend developer"]
    assert [job["id"] for job in ranked] == ["stronger", "weaker"]
    assert ranked[0]["score"] > ranked[1]["score"]


def test_score_job_does_not_match_skill_inside_larger_word() -> None:
    score, reasons = score_job(
        {"skills": ["sql"]},
        {"description": "NoSQL databases", "arrival_date": "2026-09-01"},
    )

    assert score == 5
    assert reasons == ["Recent offer"]
