from pathlib import Path

def load_document(file_path: str) -> str:
    """Read a text document and return its content"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    return path.read_text(encoding="utf-8")


def chunk_text(text: str) -> list[str]:
    """Split text into heading aware policy chunks."""

    sections = [
        section.strip()
        for section in text.split("\n\n")
        if section.strip()
    ]

    chunks = []
    current_chunk = []

    for section in sections:
        # A section without a heading starts a new chunk.
        if not current_chunk:
            current_chunk.append(section)
            continue

        # Recognize policy heading by their naming convention
        is_heading = (
            section.lower().endswith("policy")
            and len(section.split()) <= 5
        )

        if is_heading:
            chunks.append("\n\n". join(current_chunk))
            current_chunk = [section]
        else:
            current_chunk.append(section)

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

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

