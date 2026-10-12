from pypdf import PdfReader
import re   # at the top of the file


HEADINGS = ["SUMMARY", "TECHNICAL SKILLS", "WORK EXPERIENCE", "PERSONAL PROJECTS", "EDUCATION"]

def clean_text(raw: str) -> str:
    text = " ".join(raw.split())
    text = text.replace("•", "\n•")
    text = re.sub(r",(?=[A-Za-z])", ", ", text)
    text = re.sub(r"(?<=[.!?])\s+(?=[A-Z][A-Za-z ]+ \|)", "\n", text)
    for heading in HEADINGS:
        text = text.replace(heading, f"\n\n{heading}\n")
    return text.strip()

def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text())
    return "\n".join(pages)

if __name__ == "__main__":
    print(clean_text(read_pdf("data/private/Roopan_Bascaran_Resume.pdf")))