import os
import analyzer

def test_extraction():
    print("Testing document text extraction...")
    
    # 1. Verify file exists
    resume_path = "sample_resume.docx"
    if not os.path.exists(resume_path):
        print(f"ERROR: {resume_path} does not exist. Run create_sample_resume.py first.")
        return False
        
    # 2. Run extraction
    try:
        with open(resume_path, "rb") as f:
            text = analyzer.extract_text(f, resume_path)
            
        print("\n--- Extracted Resume Text Sample ---")
        print(text[:400]) # First 400 chars
        print("------------------------------------\n")
        
        # 3. Assertions
        assert "Alex Developer" in text, "Name missing from extracted text"
        assert "alex.developer@email.com" in text, "Email missing from extracted text"
        assert "PostgreSQL" in text, "Skills missing from extracted text"
        assert "B.S. in Computer Science" in text, "Education missing from extracted text"
        
        print("SUCCESS: Text extraction verified successfully!")
        return True
    except Exception as e:
        print(f"ERROR: Extraction verification failed: {str(e)}")
        return False

def test_api_config():
    print("\nTesting environment configuration...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print(f"SUCCESS: GEMINI_API_KEY is configured in the environment (ends in ...{api_key[-4:] if len(api_key) > 4 else ''})")
        return True
    else:
        print("WARNING: GEMINI_API_KEY is not configured in the environment. "
              "You will need to paste your Gemini API Key in the UI input box to run AI analysis.")
        return False

if __name__ == "__main__":
    extraction_ok = test_extraction()
    api_ok = test_api_config()
    
    print("\n--- Test Summary ---")
    print(f"Extraction Status: {'PASSED' if extraction_ok else 'FAILED'}")
    print(f"API Configuration: {'CONFIGURED' if api_ok else 'NOT CONFIGURED (Optional in UI)'}")
    
    if extraction_ok:
        print("\nAll local offline backend modules are working correctly!")
