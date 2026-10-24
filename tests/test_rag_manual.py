from app.rag import answer_question


result = answer_question(
    "How many annual leave days can employees carry forward?"
)

print("Question:", result["question"])
print("Answer:", result["answer"])
print("Sources:", len(result["sources"]))

for source in result["sources"]:
    print(
        f"Chunk {source['chunk_id']} "
        f"| Distance: {source['distance']:.4f}"
    )
