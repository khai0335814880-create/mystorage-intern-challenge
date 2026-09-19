# MyStorage Product Engineering Intern Assignment — STOW 2.0 Solution

**Candidate**: NGUYỄN NHƯ KHẢI  
**Role**: Product Engineering Intern (AI-Native)  
**Email**: `khai0335814880@gmail.com` | **Phone**: `0335814880`  
**LinkedIn**: [linkedin.com/in/khải-nguyễn-như](https://www.linkedin.com/in/kh%E1%BA%A3i-nguy%E1%BB%85n-nh%C6%B0)  
**GitHub**: [github.com/khai0335814880-create](https://github.com/khai0335814880-create)  
**Portfolio**: [figma-portfolio-drab.vercel.app](https://figma-portfolio-drab.vercel.app/)  
**Live Prototype URL**: [mystorage-intern-challenge-e507g80yp.vercel.app](https://mystorage-intern-challenge-e507g80yp.vercel.app/)  

---

## 📁 Repository Structure

```
mystorage-intern-challenge/
├── CV_AI_ProductManage_EN.pdf       # Candidate CV (Page 1 in merged report)
├── audit_report.md                # Detailed system audit of stow.mystorage.vn (Findings 1, 2, 3)
├── generate_pdf.py                # Python script to merge CV + audit report into single PDF (< 4MB)
├── mystorage_intern_assignment.pdf # Single merged PDF file (< 4MB) with clickable links
├── src/
│   ├── index.html
│   ├── main.ts
│   └── app/
│       ├── app.ts
│       └── stow-assistant/       # STOW 2.0 Angular Component (Prototype Deliverable)
│           ├── stow-assistant.ts
│           ├── stow-assistant.html
│           └── stow-assistant.css
├── angular.json
├── package.json
└── tsconfig.json
```

---

## 🌐 How Reviewers Can Access & Test the STOW 2.0 Prototype

1. **Live Deployed Prototype URL**: Visit [mystorage-intern-challenge-e507g80yp.vercel.app](https://mystorage-intern-challenge-e507g80yp.vercel.app/).
2. **GitHub Source Code**: Inspect repository at [github.com/khai0335814880-create/mystorage-intern-challenge](https://github.com/khai0335814880-create/mystorage-intern-challenge).
3. **Local Run Commands**:
   ```bash
   git clone https://github.com/khai0335814880-create/mystorage-intern-challenge.git
   cd mystorage-intern-challenge
   npm install
   npm start
   # Open browser at http://localhost:4200/
   ```

### Re-compiling PDF Assignment Report
```bash
python generate_pdf.py
```

---

## 📤 Submitting Application to MyStorage API Endpoint

Run the following `cURL` command to submit your completed assignment PDF:

```bash
curl -X POST https://mystorage.vn/api/careers/apply \
  -F "job=product-engineering-intern" \
  -F "name=NGUYỄN NHƯ KHẢI" \
  -F "email=khai0335814880@gmail.com" \
  -F "phone=0335814880" \
  -F "note=The last project I built with an AI coding tool (Antigravity AI) was my interactive Developer Portfolio and the STOW 2.0 AI Assistant prototype for MyStorage. While the AI rapidly scaffolded UI components and PDF generation scripts, I had to fix several critical issues myself: refactoring legacy Angular template syntax, fixing signal array mutation bugs, resolving i18n locale desync, and engineering a custom Python PDF merger to combine my CV with clickable assignment links under the 4MB limit." \
  -F "links=https://github.com/khai0335814880-create/mystorage-intern-challenge" \
  -F "file=@mystorage_intern_assignment.pdf;type=application/pdf"
```
