from pydantic import BaseModel


class JobDescription(BaseModel):
    title: str
    company: str
    required_skills: list[str]
    nice_to_have_skills: list[str]
    experience_years: int
    summary: str


class Project(BaseModel):
    name: str
    description: str
    tech: list[str]


class Experience(BaseModel):
    company: str
    title: str
    start: str
    end: str | None = None
    tech: list[str]
    highlights: list[str]


class Education(BaseModel):
    degree: str
    field_of_study: str | None = None
    institution: str
    start_year: int | None = None
    end_year: int | None = None


class Resume(BaseModel):
    skills: list[str]
    experiences: list[Experience]
    projects: list[Project]
    education: list[Education]