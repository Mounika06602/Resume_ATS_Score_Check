import urllib.request
import urllib.parse
import mimetypes
import uuid

def send_test_request():
    url = "http://127.0.0.1:5000/api/analyze"
    
    # Read resume docx
    with open("sample_resume.docx", "rb") as f:
        resume_data = f.read()
        
    # Read jd text
    with open("sample_jd.txt", "r", encoding="utf-8") as f:
        jd_data = f.read()
        
    # Construct multipart form-data
    boundary = uuid.uuid4().hex
    parts = []
    
    # Resume file part
    parts.append(f"--{boundary}".encode())
    parts.append(f'Content-Disposition: form-data; name="resume"; filename="sample_resume.docx"'.encode())
    parts.append(b'Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    parts.append(b'')
    parts.append(resume_data)
    
    # JD text part
    parts.append(f"--{boundary}".encode())
    parts.append(f'Content-Disposition: form-data; name="jd"'.encode())
    parts.append(b'')
    parts.append(jd_data.encode())
    
    parts.append(f"--{boundary}--".encode())
    parts.append(b'')
    
    body = b"\r\n".join(parts)
    
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    
    try:
        response = urllib.request.urlopen(req)
        print("Success! Response Code:", response.status)
        print(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print("Error Code:", e.code)
        print(e.read().decode('utf-8'))
    except Exception as e:
        print("General Exception:", str(e))

if __name__ == "__main__":
    send_test_request()
