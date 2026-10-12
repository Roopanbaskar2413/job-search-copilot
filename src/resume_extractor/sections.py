import re
from src.resume_extractor.pdf_text import HEADINGS


def split_sections(text: str) -> dict[str, str]:
    pattern = "(" + "|".join(HEADINGS) + ")"
    parts = re.split(pattern, text)
    sections = {}
    for i in range(1, len(parts), 2):
        sections[parts[i]] = parts[i + 1].strip()
    return sections


def split_jobs(experience_text: str) -> list[dict]:
    jobs = []
    for line in experience_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("•"):
            jobs[-1]["bullets"].append(line.lstrip("• ").strip())
        else:
            jobs.append({"header": line, "bullets": []})
    return jobs


def split_projects(projects_text: str) -> list[str]:
    return [p.strip() for p in projects_text.split("•") if p.strip()]