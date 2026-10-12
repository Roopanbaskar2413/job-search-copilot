import ollama
from pydantic import BaseModel
from src.common.models import Resume, Experience, Project, Education
from src.resume_extractor.pdf_text import read_pdf, clean_text
from src.resume_extractor.sections import split_sections, split_jobs, split_projects
from src.resume_extractor.dates import parse_range, total_experience_years


MODEL = "llama3.2"

BASICS_PROMPT = """You read the skills and education sections of a resume.
Rules:
- Use ONLY the text given.
- Put each skill as its own item, not a sentence.
- For education, degree is the degree type, field_of_study is the subject, years are integers."""

JOB_PROMPT = """You read one job entry from a resume: a header line and its bullet points.
Rules:
- Use ONLY the text given.
- company is the company name only, without location or work-mode words such as Remote.
- tech lists technologies that are named in the bullet points. If a technology is not named there, do not list it.
- tech lists only software technologies, languages, frameworks, and cloud services. Do not list platforms, companies, or products being built (for example, Instagram)."""""

PROJECT_PROMPT = """You read one project entry from a resume.
Rules:
- Use ONLY the text given.
- name is the project name only.
- description is one or two sentences on what the project does and its notable features.
- tech is the list of technologies named in the heading or text."""


class JobFacts(BaseModel):
    company: str
    title: str
    tech: list[str]


class Basics(BaseModel):
    skills: list[str]
    education: list[Education]


def ask(system: str, text: str, schema_model, ctx: int = 4096):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        format=schema_model.model_json_schema(),
        options={"temperature": 0, "num_ctx": ctx},
    )
    return schema_model.model_validate_json(response["message"]["content"])


def extract_resume(text: str) -> Resume:
    sections = split_sections(text)

    basics = ask(
        BASICS_PROMPT,
        sections["TECHNICAL SKILLS"] + "\n\n" + sections["EDUCATION"],
        Basics,
    )

    experiences = []
    for job in split_jobs(sections["WORK EXPERIENCE"]):
        body = job["header"] + "\n" + "\n".join("- " + b for b in job["bullets"])
        facts = ask(JOB_PROMPT, body, JobFacts)
        start, end = parse_range(job["header"])
        experiences.append(
            Experience(**facts.model_dump(), start=start, end=end, highlights=job["bullets"])
        )

    projects = [
        ask(PROJECT_PROMPT, entry, Project)
        for entry in split_projects(sections["PERSONAL PROJECTS"])
    ]

    return Resume(
        skills=basics.skills,
        experiences=experiences,
        projects=projects,
        education=basics.education,
    )

if __name__ == "__main__":
    text = clean_text(read_pdf("data/private/Roopan_Bascaran_Resume.pdf"))
    print(extract_resume(text).model_dump_json(indent=2))
    resume = extract_resume(text)
    print(resume.model_dump_json(indent=2))
    print("Total years:", total_experience_years(resume.experiences))