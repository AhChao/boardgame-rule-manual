import argparse
from pypdf import PdfReader
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF.")
    parser.add_argument("input_pdf", help="Path to input PDF file")
    parser.add_argument("output_txt", help="Path to output text file")
    args = parser.parse_args()

    try:
        reader = PdfReader(args.input_pdf)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"--- Page {i+1} ---\n"
            text += page.extract_text() + "\n\n"
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(args.output_txt), exist_ok=True)

        with open(args.output_txt, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"Successfully extracted text to {args.output_txt}")
        print(f"Total pages: {len(reader.pages)}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
