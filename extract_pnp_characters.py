from pypdf import PdfReader
import sys
import glob
import os

try:
    # Ensure output directory exists
    os.makedirs("artifacts/two-rooms-rules", exist_ok=True)
    
    output_text = ""
    # Get all PnP files sorted
    pdf_files = sorted(glob.glob("files/PnP*.pdf"))
    
    if not pdf_files:
        print("No PnP PDF files found in files/")
        sys.exit(1)

    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        output_text += f"\n\n=== FILE: {os.path.basename(pdf_file)} ===\n\n"
        reader = PdfReader(pdf_file)
        for i, page in enumerate(reader.pages):
            output_text += f"--- Page {i+1} ---\n"
            text = page.extract_text()
            if text:
                output_text += text + "\n"
            else:
                output_text += "[No text extracted]\n"

    with open("artifacts/two-rooms-rules/raw_pnp_characters.txt", "w", encoding="utf-8") as f:
        f.write(output_text)

    print("Successfully extracted text to artifacts/two-rooms-rules/raw_pnp_characters.txt")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
