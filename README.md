# PDF Content Extractor

## 1. Project Description
The PDF Content Extractor is a secure, locally-hosted desktop toolset explicitly engineered for high-fidelity extraction of text and visual assets from PDF documents. By eliminating the necessity for external cloud processing, it ensures the absolute privacy of your local documents.

The application leverages PyMuPDF and specifically `pymupdf4llm` to parse complex document structures, delivering:
1. **Mixed Content Markdown:** Extracted text with inline images positioned contextually, perfect for cross-application rich-text transfer.
2. **Pure Markdown:** De-noised, text-only Markdown code optimized for LLM ingestion and plain-text archiving.
3. **Artwork Assets:** A consolidated gallery of all high-resolution visual elements and vector graphics exported natively into standard image formats.

## 2. Technical Stack
- **Frontend Framework:** Streamlit
- **Backend Core:** Python 3.8+
- **Parsing Engines:** PyMuPDF (`fitz`), `pymupdf4llm`

## 3. Quick Start
### 3.1 Dependencies
Ensure you have Python installed locally. If you are operating within the pre-packaged executable environment, dependencies are managed automatically via the provided batch script.

### 3.2 Execution
Double-click the `start.bat` script located in the root directory. 
The system will initialize a virtual environment, install the prerequisites detailed in `requirements.txt`, and launch the web-based graphical interface on `http://localhost:8501`.

## 4. Notable Features
- **Heuristic Outline Detection:** The engine dynamically analyzes the ratio of text density to vector paths, warning the user if the document has been completely converted to outlines (Create Outlines) or is strictly a scanned image requiring OCR.
- **Deep Fallback Extraction:** Bypasses conventional xref extraction limitations by initiating high-precision rendering snapshots for fragmented vector graphics that cannot be natively pulled.
- **Base64 Data URI Integration:** Converts localized visual assets into Base64 format asynchronously, allowing native HTML inline rendering of complex reports directly within the UI tabs.

---
**Author Info:**
Jiackey-DMESTUDIO制作
