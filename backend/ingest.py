from pypdf import PdfReader
from docx import Document
import os

def extract_text(file_path):

    text = ""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"

    elif ext == ".docx":
        doc = Document(file_path)
        for p in doc.paragraphs:
            text += p.text + "\n"

    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    return text


# 🤖 SIMPLE IA (on upgrade après vers GPT)
def generate_checklist(text):

    keywords = ["inspect", "verify", "check", "install", "test", "confirm"]

    tasks = []

    for line in text.split("\n"):
        low = line.lower()
        if any(k in low for k in keywords):
            tasks.append({
                "task": line.strip(),
                "status": "pending"
            })

    return tasks


def process_file(file_path):

    text = extract_text(file_path)

    checklist = generate_checklist(text)

    return {
        "filename": os.path.basename(file_path),
        "tasks": checklist,
        "count": len(checklist)
    }
