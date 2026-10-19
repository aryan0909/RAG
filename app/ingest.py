from pathlib import Path

def load_document(file_path: str) -> str:
    """Read a text document and return its content"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    return path.read_text(encoding="utf-8")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping character-based chunks."""
    if chunk_size <=0:
        raise ValueError("Chunk Size must be greater than Zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be non negaitve and samller than chunk size")

    text = " ".join(text.split())

    chunks = []

    start = 0

    while start < len(text):
        end = min(start+chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:        
            chunks.append(chunk)

        if end == len(text):
            break;

        start = end - overlap

    return chunks


if __name__ == "__main__":
    document_path = Path(__file__).resolve().parent.parent/ "data"/ "company_policy.txt"

    document = load_document(str(document_path))
    chunks = chunk_text(document)

    print(f"Document Loaded: {document_path.name}")
    print(f"Total characters: {len(document)}")
    print(f"Total Chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n------- Chunk {index} -------")
        print(chunk)

