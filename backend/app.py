from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from docx import Document
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------
# IA SIMPLE (checklist)
# -------------------------
def generate_checklist(text: str):

    keywords = [
        "inspect", "verify", "check", "install",
        "test", "confirm", "measure", "ensure"
    ]

    tasks = []

    for line in text.split("\n"):
        low = line.lower()

        if any(k in low for k in keywords) and len(line.strip()) > 5:
            tasks.append({
                "task": line.strip(),
                "status": "pending"
            })

    return tasks


# -------------------------
# EXTRACTION TEXTE
# -------------------------
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


# -------------------------
# UPLOAD ENDPOINT
# -------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)

    checklist = generate_checklist(text)

    return {
        "filename": file.filename,
        "tasks": checklist
    }
