import json
from src.resume_extractor.pdf_text import read_pdf, clean_text
from src.resume_extractor.extract import extract_resume

RESUME_PDF = "data/private/Roopan_Bascaran_Resume.pdf"
EXPECTED = "data/private/resume_expected.json"


def norm(s: str) -> str:
    s = s.lower().strip()
    if s.startswith("aws "):
        s = s[4:]
    return s


def f1(p: float, r: float) -> float:
    return 2 * p * r / (p + r) if p + r else 0.0


def compare_sets(label, got, want, f1s):
    g = {norm(x) for x in got}
    w = {norm(x) for x in want}
    hit = len(g & w)
    precision = hit / len(g) if g else 0.0
    recall = hit / len(w) if w else 1.0
    score = f1(precision, recall)
    f1s.append(score)
    print(f"{label}: F1 {score:.2f}")
    if g - w:
        print("    extra:  ", sorted(g - w))
    if w - g:
        print("    missing:", sorted(w - g))


def check(label, got, want, checks):
    ok = got == want
    checks.append(ok)
    if not ok:
        print(f"WRONG {label}: got {got!r}, want {want!r}")


def main():
    with open(EXPECTED) as f:
        want = json.load(f)
    got = extract_resume(clean_text(read_pdf(RESUME_PDF)))
    checks, f1s = [], []

    compare_sets("skills", got.skills, want["skills"], f1s)

    check("job count", len(got.experiences), len(want["experiences"]), checks)
    for g, w in zip(got.experiences, want["experiences"]):
        name = w["title"]
        for field in ("company", "title", "start", "end"):
            check(f"{name}.{field}", getattr(g, field), w[field], checks)
        compare_sets(f"{name}.tech", g.tech, w["tech"], f1s)

    got_projects = {p.name.lower(): p for p in got.projects}
    for w in want["projects"]:
        g = got_projects.get(w["name"].lower())
        check(f"project {w['name']} found", g is not None, True, checks)
        if g is None:
            f1s.append(0.0)
            continue
        compare_sets(f"project {w['name']}.tech", g.tech, w["tech"], f1s)

    for g, w in zip(got.education, want["education"]):
        for field in w:
            check(f"education.{field}", getattr(g, field), w[field], checks)

    print()
    print(f"Exact fields: {sum(checks)}/{len(checks)}")
    print(f"Average F1:   {sum(f1s) / len(f1s):.2f}")


if __name__ == "__main__":
    main()