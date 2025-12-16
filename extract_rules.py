from pypdf import PdfReader
import sys

try:
    reader = PdfReader("files/TwoRooms_Rulebook_v3.pdf")
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"--- Page {i+1} ---\n"
        text += page.extract_text() + "\n\n"
    
    with open("artifacts/two-rooms-rules/raw_rules.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    print("Successfully extracted text to artifacts/two-rooms-rules/raw_rules.txt")
    print(f"Total pages: {len(reader.pages)}")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
