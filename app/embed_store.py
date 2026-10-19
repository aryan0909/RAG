from pathlib import Path

import lancedb
from fastembed import TextEmbedding

from app.ingest import chunk_text, load_document



PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "company_policy.txt"
DB_PATH = PROJECT_ROOT / "data" / "lancedb"

TABLE_NAME = "company_documents"
MODEL_NAME = "BAAI/bge-small-en-v1.5"

def build_vector_store() -> None:
    #1. Load the source document
    document = load_document(str(DATA_PATH))

    #2. Split the doucment into chunks
    chunks = chunk_text(document)

    if not chunks:
        raise ValueError("The document contians no usable text")

    print(f"Loaded Document: {DATA_PATH.name}")
    print(f"Number of chunks: {len(chunks)}")

    #3. Load the pretrained embedding model
    model = TextEmbedding(model_name=MODEL_NAME)

    #4. Convert each chunk into numerical vector
    embeddings = list(model.embed(chunks))

    #5. Prepare records for the vector database
    records = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        records.append(
            {
                "chunk_id":index,
                "text": chunk,
                "source":DATA_PATH.name,
                "vector": embedding.tolist()
            }
        )  

    #6. Connect to local lanceDB database
    db = lancedb.connect(str(DB_PATH))

    #7. Create the table, replacing the previous version if present
    table = db.create_table(
        TABLE_NAME,
        data = records,
        mode = "overwrite",
    )

    print(f"Stored {len(records)} records in lanceDB")
    print(f"Vector dimensions: {len(records[0]['vector'])}")
    print(f"Database path: {DB_PATH}")

if __name__ == "__main__":
    build_vector_store()