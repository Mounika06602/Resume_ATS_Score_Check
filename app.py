import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import analyzer

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Ensure static folder exists
os.makedirs(app.static_folder, exist_ok=True)

# Route to serve the frontend homepage
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Catch-all route to serve static files or redirect to homepage
@app.route('/<path:path>')
def serve_static(path):
    static_file_path = os.path.join(app.static_folder, path)
    if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# API Route for analysis
@app.route('/api/analyze', methods=['POST'])
def analyze():
    # 1. Validation checks
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file found in the request. Please upload a file."}), 400
        
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file. Please upload a valid resume."}), 400
        
    jd_text = request.form.get('jd', '').strip()
    if not jd_text:
        return jsonify({"error": "Job description is empty. Please provide a job description."}), 400
        
    # Get client-provided API key from header or form
    api_key = request.headers.get('X-Gemini-API-Key') or request.form.get('api_key')
    # Clean whitespace/newlines from client key if present
    if api_key:
        api_key = api_key.strip()
        
    try:
        # 2. Extract text from the uploaded file
        resume_text = analyzer.extract_text(file, file.filename)
        
        if not resume_text.strip():
            return jsonify({
                "error": "The resume was read successfully, but no text could be extracted. "
                         "This might happen if the PDF is scanned. Please upload a text-based PDF or DOCX file."
            }), 400
            
        # 3. Analyze the matching score and details via LLM
        analysis = analyzer.analyze_resume_vs_jd(resume_text, jd_text, api_key=api_key)
        
        return jsonify(analysis)
        
    except ValueError as ve:
        # Standard user-facing errors
        return jsonify({"error": str(ve)}), 400
    except RuntimeError as re:
        # Issues with the LLM API call
        return jsonify({"error": str(re)}), 500
    except Exception as e:
        # Fallback catch-all error
        return jsonify({"error": f"An unexpected error occurred during parsing: {str(e)}"}), 500

if __name__ == '__main__':
    # Get port from environmental variables, default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Run server locally, accessible via localhost
    print(f"Starting Resume ATS Checker server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
