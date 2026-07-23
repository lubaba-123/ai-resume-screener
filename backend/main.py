from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from services.extractor import extract_text
from services.llm_service import get_resume_comparison

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


@app.post("/submit-job-description")
async def submit_job_description(
    jd_text: str = Form(None),
    jd_file: UploadFile = File(None)
):
    if jd_file is not None:
        allowed_extensions = (".pdf", ".docx")
        if not jd_file.filename.lower().endswith(allowed_extensions):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed for JD upload.")

        file_bytes = await jd_file.read()
        try:
            extracted_jd_text = extract_text(jd_file.filename, file_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract JD text: {str(e)}")

        if not extracted_jd_text:
            raise HTTPException(status_code=422, detail="No text could be extracted from the JD file.")

        return {
            "source": "file",
            "filename": jd_file.filename,
            "job_description_text": extracted_jd_text,
            "character_count": len(extracted_jd_text)
        }

    if jd_text is not None and jd_text.strip():
        return {
            "source": "text",
            "job_description_text": jd_text.strip(),
            "character_count": len(jd_text.strip())
        }

    raise HTTPException(status_code=400, detail="Either jd_text or jd_file must be provided.")


@app.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    jd_text: str = Form(None),
    jd_file: UploadFile = File(None)
):
    allowed_extensions = (".pdf", ".docx")

    if not resume_file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed for resume.")

    resume_bytes = await resume_file.read()
    try:
        resume_text = extract_text(resume_file.filename, resume_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract resume text: {str(e)}")

    if not resume_text:
        raise HTTPException(status_code=422, detail="No text could be extracted from the resume.")

    job_description_text = None

    if jd_file is not None:
        if not jd_file.filename.lower().endswith(allowed_extensions):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed for JD.")
        jd_bytes = await jd_file.read()
        try:
            job_description_text = extract_text(jd_file.filename, jd_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract JD text: {str(e)}")
    elif jd_text is not None and jd_text.strip():
        job_description_text = jd_text.strip()

    if not job_description_text:
        raise HTTPException(status_code=400, detail="Either jd_text or jd_file must be provided.")

    try:
        result = get_resume_comparison(resume_text, job_description_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM comparison failed: {str(e)}")

    return result