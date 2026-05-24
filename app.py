import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import analyzer

# Load environment variables
load_dotenv()

app = FastAPI(title="Resume ATS Checker API", version="1.0.0")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Route for analysis
@app.post("/api/analyze")
async def analyze(
    resume: UploadFile = File(...),
    jd: str = Form(...)
):
    # 1. Validation checks
    if not resume.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No selected file. Please upload a valid resume."
        )
        
    jd_clean = jd.strip()
    if not jd_clean:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description is empty. Please provide a job description."
        )
        
    try:
        # 2. Extract text from the uploaded file
        # resume.file is the underlying file-like object which pypdf and docx can read
        resume_text = analyzer.extract_text(resume.file, resume.filename)
        
        if not resume_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The resume was read successfully, but no text could be extracted. "
                       "This might happen if the PDF is scanned. Please upload a text-based PDF or DOCX file."
            )
            
        # 3. Analyze the matching score and details via LLM
        analysis = analyzer.analyze_resume_vs_jd(resume_text, jd_clean)
        
        return analysis
        
    except HTTPException as he:
        # Reraise FastAPI HTTPExceptions
        raise he
    except ValueError as ve:
        # Standard user-facing validation errors
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except RuntimeError as re:
        # Issues with the LLM API call
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
    except Exception as e:
        # Fallback catch-all error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred during parsing: {str(e)}")

# Mount static files directory at root, automatically serving index.html on "/"
# Note: Mount this after API routes to prevent intercepting API calls
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Resume ATS Checker FastAPI server on port {port}...")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
