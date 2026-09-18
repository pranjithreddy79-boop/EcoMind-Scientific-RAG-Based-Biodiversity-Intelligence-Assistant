from pathlib import Path
from pypdf import PdfReader


PDF_DIR = Path("knowledge/sources")
OUTPUT_DIR = Path("knowledge/extracted")


def extract_pdf(pdf_path):
    print(f"\nReading: {pdf_path.name}")

    reader = PdfReader(str(pdf_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        try:
            text = page.extract_text()
        except Exception as error:
            print(f"Could not read page {page_number}: {error}")
            continue

        if text:
            pages.append(
                f"\n--- PAGE {page_number} ---\n{text}"
            )

    return "\n".join(pages)


def extract_all_pdfs():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_path in pdf_files:

        text = extract_pdf(pdf_path)

        output_file = OUTPUT_DIR / f"{pdf_path.stem}.txt"

        output_file.write_text(
            text,
            encoding="utf-8"
        )

        print(
            f"Saved: {output_file}"
        )

        print(
            f"Characters extracted: {len(text):,}"
        )


if __name__ == "__main__":
    extract_all_pdfs()