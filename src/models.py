from pydantic import BaseModel

class JobDescription(BaseModel):
    title: str
    company: str
    required_skills: list[str]
    nice_to_have_skills: list[str]
    experience_years: int
    summary: str

class Resume(BaseModel):
    name: str
    skills: list[str]
    experience_years: int
    projects: list[str]