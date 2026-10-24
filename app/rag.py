from app.generate import generate_answer
from app.retrieve import search_documents

FALLBACK_ANSWER = (
    "I could not find this information "
    "in the provided company documents."
)

# Initial threshold for our small tutorial dataset.
# Will validate and tune it using test queries.
MAX_DISTANCE = 0.45

def answer_question(question: str, limit: int = 2) -> dict:
    """Retrieve document chunks and generate a grounded answer."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    # Retrieve relevant document chunks.
    results = search_documents(query=question, limit=limit)

    # Handle cases where retrieval returns no documents.
    if not results:
        return {
            "question": question,
            "answer": FALLBACK_ANSWER,
            "sources": [],
        }

    # Reject Result when the best match is not relevant enough
    best_distance = results[0]["_distance"]

    if best_distance > MAX_DISTANCE:
        return {
                "question": question,
                "answer": FALLBACK_ANSWER,
                "sources":[],
            }

    relevant_results = [
        result 
        for result in results
        if result["_distance"] <= MAX_DISTANCE
    ]


    # Combine retrieved text into the LLM context.
    context = "\n\n".join(
        result["text"]for result in relevant_results
    )

    # Generate an answer using the retrieved context.
    answer = generate_answer(
        question=question,
        context=context,
    )

    # Return the answer and source metadata.
    sources = [
        {
            "chunk_id": result["chunk_id"],
            "source": result["source"],
            "distance": result["_distance"],
            "text": result["text"],
        }
        for result in relevant_results
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }
