"""
HTTP endpoint routers for the Resume ATS Checker API.

This router manages requests sent from the client-side UI dashboard, specifically
the POST request containing the resume file upload and job description requirements.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app import analyzer

# Instantiate the modular router
router = APIRouter()

@router.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    jd: str = Form(...)
):
    """
    Compare the uploaded resume file and target job description using AI.
    
    1. Extracts text from the uploaded file (accepts .pdf, .docx, .txt).
    2. Packages and delivers content to the LLM analyzer service.
    3. Returns parsed, structured analysis results as a JSON payload.
    """
    # 1. Validation checks on incoming request parameters
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
        # 2. Extract plain text from the uploaded document stream
        # resume.file is a file-like temporary stream that pypdf and docx can read
        resume_text = analyzer.extract_text(resume.file, resume.filename)
        
        if not resume_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The resume was read successfully, but no text could be extracted. "
                       "This might happen if the PDF is scanned. Please upload a text-based PDF or DOCX file."
            )
            
        # 3. Analyze the matching score and details via the LangChain Gemini LLM chain
        analysis = analyzer.analyze_resume_vs_jd(resume_text, jd_clean)
        
        return analysis
        
    except HTTPException as he:
        # Re-raise explicit HTTP exceptions from the pipeline
        raise he
    except ValueError as ve:
        # Handle formatting or user document selection errors
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except RuntimeError as re:
        # Handle failures related to the Google Gemini API client calls
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
    except Exception as e:
        # Fallback catch-all for unhandled server issues
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An unexpected error occurred during parsing: {str(e)}"
        )
