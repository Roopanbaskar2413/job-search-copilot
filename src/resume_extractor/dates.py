import re
from datetime import date

DATE_RANGE = re.compile(
    r"(\d{2})/(\d{4})\s*[-–]\s*(\d{2}/\d{4}|Present|Current)", re.IGNORECASE
)


def parse_range(header: str) -> tuple[str, str | None]:
    match = DATE_RANGE.search(header)
    if not match:
        raise ValueError(f"No date range found in: {header}")
    start = f"{match.group(2)}-{match.group(1)}"
    end_raw = match.group(3)
    if end_raw.lower() in ("present", "current"):
        return start, None
    month, year = end_raw.split("/")
    return start, f"{year}-{month}"


def _index(year_month: str) -> int:
    year, month = year_month.split("-")
    return int(year) * 12 + int(month)


def total_experience_years(experiences, today: date | None = None) -> float:
    today = today or date.today()
    now = today.year * 12 + today.month
    spans = sorted(
        (_index(e.start), _index(e.end) if e.end else now) for e in experiences
    )
    total = 0
    cur_start, cur_end = None, None
    for start, end in spans:
        if cur_end is None or start > cur_end:
            if cur_end is not None:
                total += cur_end - cur_start
            cur_start, cur_end = start, end
        else:
            cur_end = max(cur_end, end)
    if cur_end is not None:
        total += cur_end - cur_start
    return round(total / 12, 1)


if __name__ == "__main__":
    assert parse_range("Engineer | Velvee Labs Remote / San Jose, CA 03/2025 - 09/2026") == ("2025-03", "2026-09")
    assert parse_range("Intern | Velvee Labs Remote / San Jose, CA 11/2024 - 02/2025") == ("2024-11", "2025-02")
    assert parse_range("Engineer | Acme 01/2023 - Present") == ("2023-01", None)
    print("date tests passed")