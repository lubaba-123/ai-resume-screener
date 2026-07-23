# AI Resume Screener & Feedback

An AI-powered tool that compares a resume against a job description, returns a match score (0–100), flags missing keywords, and gives actionable rewrite suggestions.

## Overview

Upload a resume (PDF/DOCX) and a job description (paste or upload), and the tool uses an LLM to analyze the fit and return structured feedback: a match score, missing keywords, and rewrite suggestions.

## Tech Stack

- **Frontend:** Next.js (App Router), Tailwind CSS
- **Backend:** FastAPI (Python)
- **Text Extraction:** pdfplumber (PDF), python-docx (DOCX)
- **LLM:** Google Gemini API (`gemini-flash-latest`)

## Project Structure
ai-resume-screener/
├── backend/
│ ├── main.py # FastAPI app and routes
│ ├── services/
│ │ ├── extractor.py # PDF/DOCX text extraction
│ │ ├── prompt_builder.py # LLM prompt template
│ │ └── llm_service.py # Gemini API call + JSON validation/retry
│ ├── requirements.txt
│ └── .env.example
├── frontend/
│ └── src/app/
│ ├── layout.js
│ ├── page.js # Main UI (upload form + results)
│ └── globals.css
└── README.md
## Setup Instructions

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:
GEMINI_API_KEY=your_api_key_here
Run the server:
```bash
uvicorn main:app --reload
```

Backend runs at `http://127.0.0.1:8000`. API docs available at `http://127.0.0.1:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/upload-resume` | Upload a resume and extract text |
| POST | `/submit-job-description` | Submit a JD via text or file |
| POST | `/analyze` | Upload resume + JD, get match score, missing keywords, and suggestions |

## How It Works

1. User uploads a resume (PDF/DOCX) and provides a job description (text or file)
2. Backend extracts plain text from both documents
3. A structured prompt is sent to Gemini, forcing a strict JSON response
4. The response is validated; if malformed, the system retries once
5. Frontend displays the match score, missing keywords, and suggestions

## Team Roles

| Name | Role |
|------|------|
| Lubaba | Full-stack development (backend, frontend, LLM integration) |

*Note: This project was completed individually.*

## Common Issues & Fixes

- **CORS errors:** Handled via `CORSMiddleware` in `main.py`
- **Scanned/image PDFs:** Text extraction may return empty; OCR fallback not yet implemented
- **LLM returning non-JSON output:** Handled via prompt constraints + retry logic in `llm_service.py`