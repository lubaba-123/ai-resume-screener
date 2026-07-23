from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.extractor import extract_text

app = FastAPI(title="AI Resume Screener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    allowed_extensions = (".pdf", ".docx")
    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed.")

    file_bytes = await file.read()

    try:
        extracted_text = extract_text(file.filename, file_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    if not extracted_text:
        raise HTTPException(status_code=422, detail="No text could be extracted. The file may be a scanned/image-based document.")

    return {
        "filename": file.filename,
        "extracted_text": extracted_text,
        "character_count": len(extracted_text)
    }