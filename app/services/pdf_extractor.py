import fitz  # PyMuPDF

def extract_text_from_pdf(filepath: str) -> str:
    with fitz.open(filepath) as pdf:
        return "\n".join(page.get_text() for page in pdf)
