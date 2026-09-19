import os
import sys
import urllib.request
import ssl
import json
import uuid

def submit_application():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, 'mystorage_intern_assignment.pdf')

    if not os.path.exists(pdf_path):
        print(f"Error: Could not find PDF report at {pdf_path}")
        print("Please run 'python generate_pdf.py' first!")
        return

    url = "https://mystorage.vn/api/careers/apply"
    
    # Payload details
    fields = {
        'job': 'product-engineering-intern',
        'name': 'NGUYỄN NHƯ KHẢI',
        'email': 'khai0335814880@gmail.com',
        'phone': '0335814880',
        'note': "The last project I built with an AI coding tool (Antigravity AI) was my interactive Developer Portfolio and the STOW 2.0 AI Assistant prototype for MyStorage. While the AI rapidly scaffolded UI components and PDF generation scripts, I had to fix several critical issues myself: refactoring legacy Angular template syntax, fixing signal array mutation bugs, resolving i18n locale desync, and engineering a custom Python PDF merger script with Arial TrueType font registration to display Vietnamese Unicode characters without font rendering errors, combining my CV with clickable assignment links under the 4MB limit.",
        'links': "https://github.com/khai0335814880-create/mystorage-intern-challenge\nhttps://mystorage-intern-challenge-e507g80yp.vercel.app/"
    }

    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    CRLF = "\r\n"
    data = []

    # Text fields
    for name, value in fields.items():
        data.append(f"--{boundary}")
        data.append(f'Content-Disposition: form-data; name="{name}"')
        data.append("")
        data.append(value)

    # PDF File field
    with open(pdf_path, 'rb') as f:
        file_bytes = f.read()

    data.append(f"--{boundary}")
    data.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(pdf_path)}"')
    data.append('Content-Type: application/pdf')
    data.append("")
    
    # Assemble multipart body
    body_header = (CRLF.join(data) + CRLF).encode('utf-8')
    body_footer = (CRLF + f"--{boundary}--" + CRLF).encode('utf-8')
    
    body = body_header + file_bytes + body_footer

    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    req.add_header('Content-Length', str(len(body)))

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print(f"Sending application payload to {url}...")
    print(f"Candidate: NGUYỄN NHƯ KHẢI ({fields['email']})")
    print(f"Attachment PDF size: {len(file_bytes)} bytes ({len(file_bytes)/(1024*1024):.3f} MB)")
    print("-" * 50)

    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            resp_bytes = resp.read()
            status_code = resp.status
            print(f"STATUS CODE: {status_code}")
            print("RESPONSE BODY:")
            try:
                res_json = json.loads(resp_bytes.decode('utf-8'))
                print(json.dumps(res_json, indent=2, ensure_ascii=False))
            except Exception:
                print(resp_bytes.decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_bytes = e.read()
        print(f"HTTP ERROR: {e.code}")
        print("ERROR BODY:")
        try:
            res_json = json.loads(err_bytes.decode('utf-8'))
            print(json.dumps(res_json, indent=2, ensure_ascii=False))
        except Exception:
            print(err_bytes.decode('utf-8', errors='ignore'))
    except Exception as e:
        print(f"Request Error: {e}")

if __name__ == '__main__':
    submit_application()
