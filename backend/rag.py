import os
from pypdf import PdfReader
from typing import List


def save_uploaded_file(file, upload_dir: str = "../uploads") -> str:
    """
    Saves uploaded file to the main rag-chatbot/uploads folder.
    This ensures correct production-level folder structure.
    """

    # Get absolute path of backend folder
    backend_dir = os.path.dirname(os.path.abspath(__file__))

    # Move one level up to rag-chatbot/uploads
    upload_path = os.path.abspath(os.path.join(backend_dir, upload_dir))

    # Create uploads folder if it doesn't exist
    os.makedirs(upload_path, exist_ok=True)

    # Create full file path
    file_path = os.path.join(upload_path, file.filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from all pages of a PDF file using pypdf.
    """

    text = ""

    try:
        reader = PdfReader(file_path)

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Splits text into smaller chunks with overlap.
    This is required for vector database storage.
    """

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        if end >= len(text):
            break

        start += (chunk_size - overlap)

    return chunks