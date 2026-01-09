import pypdf
import os

pdf_path = "../files/1_-_Nature_Core_Rulebook_021925.pdf"
output_path = "raw_rules.txt"

def extract_text():
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        return

    reader = pypdf.PdfReader(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        for i, page in enumerate(reader.pages):
            f.write(f"--- Page {i + 1} ---\n")
            f.write(page.extract_text())
            f.write("\n\n")
    print(f"Successfully extracted text to {output_path}")

if __name__ == "__main__":
    extract_text()
