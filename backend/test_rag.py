import os
from rag import chunk_text, extract_text_from_pdf

def test_chunking():
    print("Testing Text Chunking...")
    text = "A" * 1000  # 1000 characters
    chunk_size = 500
    overlap = 100
    
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    
    # Expected: 
    # Chunk 1: 0-500
    # Chunk 2: (500-100)=400 to 900
    # Chunk 3: (900-100)=800 to 1000
    
    assert len(chunks) == 3
    assert len(chunks[0]) == 500
    assert len(chunks[1]) == 500
    assert len(chunks[2]) == 200
    
    print("- Chunking logic: SUCCESS")

def test_pdf_extraction():
    print("Testing PDF Extraction (Placeholder)...")
    # This would require a real PDF file. 
    # For now, we verify the function handles missing files gracefully.
    result = extract_text_from_pdf("non_existent.pdf")
    assert result == ""
    print("- Error handling for missing PDFs: SUCCESS")

if __name__ == "__main__":
    try:
        test_chunking()
        test_pdf_extraction()
        print("\nAll RAG utility tests PASSED!")
    except Exception as e:
        print(f"RAG tests failed: {e}")
