import fitz  # pymupdf
import sys

def inspect_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    for page in doc:
        print(f"--- Page {page.number} ---")
        blocks = page.get_text("blocks")
        for b in blocks:
            print(b)  # (x0, y0, x1, y1, "text", block_no, block_type)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_pdf(sys.argv[1])
    else:
        print("Usage: python inspect_pdf.py <pdf_path>")
