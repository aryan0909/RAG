from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.retrieve import search_documents
from app.rag import answer_question

app = FastAPI(title="LanceDB RAG")

class SearchRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    limit: int = Field(default=2, ge=1, le=10)

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    limit: int = Field(default=2, ge=1, le=10)

@app.get("/")
def home():
    return {"message": "LanceDB RAG is Running!!"}

@app.post("/search")
def search(request: SearchRequest):
    try:
        results = search_documents(
            query=request.question,
            limit=request.limit,
        )

        return {
            "question": request.question,
            "results":[
                {
                    "chunk_id": result["chunk_id"],
                    "text":result["text"],
                    "source": result["source"],
                    "distance": result["_distance"],
                }
                for result in results
            ],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail = str(exc),
        ) from exc


@app.post("/ask")
def ask(request: AskRequest):
    try:
        return answer_question(
            question = request.question,
            limit=request.limit,
        ) 
    except ValueError as exec:
        raise HTTPException(
            status_code=400,
            detail=str(exec),
        )from exec