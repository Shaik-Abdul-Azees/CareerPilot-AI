
import fitz  # PyMuPDF


def extract_resume_text(pdf_path: str) -> str:
    """
    Extract readable text from a resume PDF.

    Args:
        pdf_path: Path to the uploaded PDF file.

    Returns:
        Extracted text from all pages.
    """
    extracted_pages = []

    with fitz.open(pdf_path) as document:
        for page in document:
            page_text = page.get_text("text")
            if page_text.strip():
                extracted_pages.append(page_text.strip())

    return "\n\n".join(extracted_pages)


if __name__ == "__main__":
    pdf_path = input("Enter the path to your resume PDF: ").strip().strip('"')

    try:
        text = extract_resume_text(pdf_path)

        if text:
            print("\n--- Extracted Resume Text ---\n")
            print(text)
        else:
            print("No readable text found in the PDF.")

    except Exception as error:
        print(f"Could not read the PDF: {error}")
