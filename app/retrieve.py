from pathlib import Path

import lancedb
from fastembed import TextEmbedding

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "lancedb"

TABLE_NAME = "company_documents"
MODEL_NAME = "BAAI/bge-small-en-v1.5"

def search_documents(query: str, limit: int = 2) -> list[dict]:
    """Retrieve the most relevant document chunks for a query"""

    if not query.strip():
        raise ValueError("Query cannot be empty")

    if limit <= 0:
        raise ValueError("Limit must be grater than 0")

    #1. Load the same embedding model used during ingestion
    model = TextEmbedding(model_name=MODEL_NAME)

    #2. Convert the user's question into a vector
    query_vector = next(model.query_embed([query])).tolist()

    #3. Connect to the existing LanceDB database.
    db = lancedb.connect(str(DB_PATH))
    table = db.open_table(TABLE_NAME)

    #4. Find the nearest vector and return their associated text
    results = (
        table.search(query_vector)
        .limit(limit)
        .to_list()
    )

    return results

if __name__ == "__main__":
    question = "How many annual leaves days can employees carry forward?"

    matches = search_documents(question)

    print(f"Question: {question}")

    for rank, match in enumerate(matches, start=1):
        print(f"\n--- Result {rank} ---")
        print(f"Chunk ID: {match['chunk_id']}")
        print(f"Distance: {match['_distance']:.4f}")
        print(f"Text: {match['text']}")