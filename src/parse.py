import ollama
from src.common.models import JobDescription

def parse_job(text: str) -> JobDescription:
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": "____"},
            {"role": "user", "content": text},
        ],
        format=JobDescription.model_json_schema(),
        options={"temperature": 0},
    )
    return JobDescription.model_validate_json(response["message"]["content"])

if __name__ == "__main__":
    with open("data/private/job1.txt") as f:
        job = parse_job(f.read())
    print(job.model_dump_json(indent=2))