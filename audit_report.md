# Audit Report: stow.mystorage.vn System & AI Assistant

**Target System**: MyStorage AI Sales Assistant (`stow.mystorage.vn`)  
**Auditor / Candidate**: NGUYỄN NHƯ KHẢI (Product Engineering Intern Applicant)  
**Email**: `khai0335814880@gmail.com` | **Phone**: `0335814880`  
**LinkedIn**: `https://www.linkedin.com/in/khải-nguyễn-như`  
**GitHub**: `https://github.com/khai0335814880-create`  
**Portfolio**: `https://figma-portfolio-drab.vercel.app/`  
**Canonical Source Ground Truth**: `https://mystorage.vn/llms.txt` & `https://mystorage.vn/`  
**Date**: September 2026  

---

## Executive Summary

An in-depth UI/UX and AI response audit of `stow.mystorage.vn` was performed across text chat, item estimation, pricing calculation, and multi-language handling. Three consequential findings were identified:
1. **[HIGH] Discrepancy between AI response quotes/insurance policy and canonical `llms.txt` ground truth.**
2. **[MEDIUM] Unhandled exception & UX dead-end for oversized items exceeding standard unit height (2.0m).**
3. **[MEDIUM] i18n locale state disconnect between voice mode modal, item tray, and active chat context.**

Below are the detailed findings, impact assessments, and proposed architectural fixes.

---

## Finding 1: AI Prompt Knowledge Desynchronization vs Canonical `llms.txt` Ground Truth (High Severity)

### 1. What Happened
When querying `stow.mystorage.vn` for starting unit prices or insurance protection coverage limits, the AI model generates inaccurate/outdated numbers (e.g. stating starting prices of 500,000 VND or 600,000 VND instead of the official 559,000 VND/month, or failing to state the Basic Protection coverage tier limit of 500,000 VND/CBM up to max 10,000,000 VND).

### 2. Steps to Reproduce
1. Open `https://stow.mystorage.vn/` and start a new conversation.
2. Ask: *"Kho lạnh/kho máy lạnh nhỏ nhất giá bao nhiêu 1 tháng và chính sách bảo hiểm tối đa bao nhiêu?"*
3. Observe the generated AI response.
4. Compare response against `https://mystorage.vn/llms.txt`:
   - Ground Truth Price: Air-conditioned & furniture storage start from **559,000 VND/month** (~US$21).
   - Ground Truth Insurance: Free Basic Protection covers **VND 500,000/CBM** up to **max VND 10,000,000**.

### 3. Impact to Customer & Business
- **Customer Trust & Legal Risk**: Providing mismatched price quotes creates friction when customers proceed to `booking.mystorage.vn`. Inconsistent insurance claims misinform users on item loss liability.
- **Revenue Conversion**: Quoting higher prices drives potential leads away; quoting lower prices leads to customer dissatisfaction at checkout.

### 4. Severity
**HIGH** (Directly impacts revenue, pricing transparency, and customer conversion).

### 5. Proposed Fix
- **Dynamic Context Injection (RAG / System Prompt Sync)**: Ingest `https://mystorage.vn/llms.txt` into the server-side system prompt assembly or vector store on deployment, ensuring zero price deviation between website pages and STOW AI responses.
- **Tool-Based Fact Verification**: Require STOW AI to execute a deterministic `get_pricing_table` tool call before outputting numeric quotes.

---

## Finding 2: Unhandled UX Breakdown & Calculation Error for Oversized Items (> 2.0m Height) (Medium Severity)

### 1. What Happened
When adding items with a height dimension greater than 2000mm (e.g., a 2.4m tall wardrobe or commercial display rack) in the Item Manager, the estimation system flags `CannotStoreMaxHeight` but offers no automatic fallback to MyStorage's **Full Service / Shelf Space Warehouse** in Dong Nai. The bin packing visualizer fails to recommend splitting items or opting for non-standard units.

### 2. Steps to Reproduce
1. In `stow.mystorage.vn`, open the Item Manager panel.
2. Add a custom item: "Tủ Quần Áo Đặt Riêng" with dimensions: Width 1200mm, Depth 600mm, Height 2400mm.
3. Click "Estimate Storage Solution".
4. System displays warning `CannotStoreMaxHeight` and blocks bin recommendation, causing an error modal or infinite loading state without actionable routing.

### 3. Impact to Customer & Business
- **Lost Sales Opportunities**: High-value customers with large or custom furniture are turned away instead of being redirected to Full Service Storage (which supports flexible shelf space).
- **Poor UX**: The user receives a negative error banner without a clear next step or contact prompt.

### 4. Severity
**MEDIUM** (Impacts specific high-value customer segments storing large items).

### 5. Proposed Fix
- **Intelligent Fallback Routing**: If `item.height > max_standard_unit_height (2000mm)`, automatically trigger a recommendation card:  
  *"Item exceeds standard self-storage height limit. We recommend our Full Service Storage at Nhon Trach 3 Warehouse (Dong Nai) with custom shelf-space and staff pickup."*
- Provide a direct 1-click button to contact sales or request a custom quote.

---

## Finding 3: Locale Context Disconnect Across Chat, Live Voice, and Item List Tray (Medium Severity)

### 1. What Happened
Switching languages via the top header flag dropdown (e.g., switching from Vietnamese to English) updates the static UI labels, but the active AI session instructions and Item List Tray headers remain in the previous locale until a full page refresh. Additionally, if the user starts Live Voice Chat after switching language, STOW continues to speak in the initial language.

### 2. Steps to Reproduce
1. Open `stow.mystorage.vn` with default language `Vietnamese`.
2. Open language dropdown and select `English`.
3. Observe item tray summary text: *"Đã lưu 0 đồ vật"* remains in Vietnamese.
4. Click "Nói trực tiếp" (Live Voice) and speak in English.
5. STOW responds in Vietnamese.

### 3. Impact to Customer & Business
- Expat customers in Ho Chi Minh City (a primary target audience under US/German management) experience confusing mixed-language interfaces, hurting brand credibility.

### 4. Severity
**MEDIUM** (Impacts usability for international & expat users).

### 5. Proposed Fix
- Pass `locale` reactively to the system prompt config during session initialization.
- Bind the i18n dictionary state globally using a shared state provider so language changes dynamically re-render all active components without losing chat history.

---

## How Reviewers & Interviewers Can Test the STOW 2.0 Prototype

1. **Live Deployed Web Application**: Visit [mystorage-intern-challenge.vercel.app](https://mystorage-intern-challenge.vercel.app/).
2. **GitHub Source Code**: Inspect the codebase at [github.com/khai0335814880-create/mystorage-intern-challenge](https://github.com/khai0335814880-create/mystorage-intern-challenge).
3. **Local Run Commands**:
   ```bash
   git clone https://github.com/khai0335814880-create/mystorage-intern-challenge.git
   cd mystorage-intern-challenge
   npm install
   npm start
   # Open http://localhost:4200/
   ```
