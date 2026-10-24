# RAG — Local Document Question Answering

**Build and query your private documents locally with zero cloud dependencies using LanceDB, Ollama, and Streamlit.**

A local Retrieval-Augmented Generation (RAG) application that lets you ask natural-language questions about your documents. It combines semantic search, vector storage, and a locally running large language model to generate answers grounded in retrieved document content.

The application uses **LanceDB** for vector search, **FastEmbed** for embeddings, **Ollama** to run Qwen locally, **FastAPI** for REST endpoints, and **Streamlit** for the interactive chat interface.

> **Privacy-first design:** Document retrieval and LLM inference run locally. Initial setup may require an internet connection to download Python packages and model files. No cloud-hosted LLM API is required.

## Features

- **Local LLM inference** using Qwen 2.5 1.5B through Ollama.
- **Semantic search** using dense vector embeddings.
- **Vector storage** with LanceDB.
- **Document chunking** with heading-aware splitting for the example policy document.
- **Grounded answer generation** using retrieved document context.
- **Source transparency** with source filenames, chunk IDs, retrieved text, and distances.
- **Relevance filtering** to reject weak retrieval matches.
- **REST API** with FastAPI and Pydantic request validation.
- **Interactive chat interface** using Streamlit.
- **Local development workflow** using Python, Git, and pytest.

## Tech Stack

| Technology               | Purpose                               |
| ------------------------ | ------------------------------------- |
| Python 3.11              | Application logic                     |
| LanceDB                  | Vector database and similarity search |
| FastEmbed                | Text embedding generation             |
| `BAAI/bge-small-en-v1.5` | Embedding model                       |
| Ollama                   | Local LLM runtime                     |
| `qwen2.5:1.5b`           | Answer generation                     |
| FastAPI                  | REST API                              |
| Pydantic                 | Request validation                    |
| Streamlit                | Chat UI                               |
| Pytest                   | API testing                           |

## Architecture

```mermaid
flowchart TD
    A[Company Documents] --> B[Document Loading and Chunking]
    B --> C[FastEmbed]
    C --> D[(LanceDB)]

    E[User Question] --> F[Query Embedding]
    F --> G[Vector Search]
    D --> G

    G --> H{Distance Threshold}
    H -->|Relevant matches| I[Build Context]
    H -->|Weak matches| J[Fallback Answer]

    I --> K[Ollama - Qwen]
    K --> L[Generated Answer]
    L --> M[Answer and Sources]
    J --> M

    N[Streamlit UI] <--> E
    M --> N

    O[FastAPI REST API] --> P[/search and /ask]
    P --> G
```

The Streamlit UI currently calls the RAG pipeline directly. FastAPI exposes separate REST endpoints for retrieval and question answering.

## How It Works

1. **Ingestion:** Load the source document and split it into meaningful chunks.
2. **Embedding:** Convert each chunk into a numerical vector.
3. **Storage:** Store document text, vectors, and metadata in LanceDB.
4. **Retrieval:** Embed the user's question and retrieve the nearest document chunks.
5. **Relevance filtering:** Compare retrieval distances against a configurable threshold.
6. **Generation:** Pass accepted chunks and the user's question to the local Qwen model.
7. **Response:** Return the answer with source metadata, or a fallback when retrieval is insufficiently relevant.

## Prerequisites

- Python 3.11
- Git
- Ollama
- Sufficient RAM and disk space for the local models
- Internet access for initial dependency and model downloads

The project was developed on Windows using Python 3.11.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/aryan0909/RAG.git
cd RAG
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If `requirements.txt` is available:

```powershell
python -m pip install -r requirements.txt
```

Ensure the dependencies include the packages used by the application, including:

- `fastapi`
- `uvicorn`
- `lancedb`
- `fastembed`
- `ollama`
- `streamlit`
- `pytest`
- `httpx`

### 4. Install Ollama and download the model

Install Ollama from:

https://ollama.com/

Download the model:

```powershell
ollama pull qwen2.5:1.5b
```

Verify that it runs:

```powershell
ollama run qwen2.5:1.5b
```

Ollama must be running when the application generates answers.

### 5. Prepare the vector database

The sample document is:

```text
data/company_policy.txt
```

Build the embeddings and LanceDB table:

```powershell
python -m app.embed_store
```

The generated vector database is stored under `data/lancedb/`.

The current ingestion workflow rebuilds the tutorial database in overwrite mode. Back up any data you need before rebuilding it.

## Run the Application

### Option A: Streamlit Chat UI

From the project root, with the virtual environment activated:

```powershell
python -m streamlit run app/ui.py
```

Open the local URL printed in the terminal, usually:

http://localhost:8501

Ask questions about the indexed documents. Expand **View sources** to inspect the retrieved chunks and their distances.

### Option B: FastAPI

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

The Streamlit interface currently calls the RAG functions directly, so FastAPI does not need to be running for the UI to work.

## API Endpoints

### `GET /`

Checks whether the API is running.

Example response:

```json
{
  "message": "LanceDB RAG API is running!"
}
```

### `POST /search`

Retrieves the nearest document chunks without generating an LLM answer.

Example request:

```json
{
  "question": "How many annual leave days can employees carry forward?",
  "limit": 2
}
```

The response includes retrieved text, source filenames, chunk IDs, and retrieval distances.

### `POST /ask`

Runs the complete RAG pipeline: retrieval, relevance filtering, and answer generation.

Example request:

```json
{
  "question": "How many annual leave days can employees carry forward?",
  "limit": 2
}
```

Example response:

```json
{
  "question": "How many annual leave days can employees carry forward?",
  "answer": "Employees can carry forward a maximum of 5 unused annual leave days into the next calendar year.",
  "sources": [
    {
      "chunk_id": 0,
      "source": "company_policy.txt",
      "distance": 0.2254,
      "text": "Employees can carry forward a maximum of 5 unused annual leave days into the next calendar year."
    }
  ]
}
```

_Example values are illustrative. Actual results depend on the indexed documents and query._

## Customize Your Documents

1. Add or update a source document under `data/`.
2. Update the ingestion logic if the document format requires additional parsing.
3. Run the ingestion and embedding workflow again.
4. Ask questions about the indexed content.

The current example uses a plain-text company policy document and heading-aware chunking. PDF, Word, HTML, and other formats require appropriate document loaders.

## Relevance Threshold

The application uses a configurable maximum retrieval distance in `app/rag.py`:

```python
MAX_DISTANCE = 0.45
```

If the best retrieval result exceeds this threshold, the application returns a fallback response instead of calling the LLM.

This is an initial threshold for the small example dataset, not a universal relevance score. It should be evaluated and tuned against representative supported and unsupported questions.

A distance threshold reduces the risk of generating answers from irrelevant context, but it does not guarantee factual correctness. The model prompt encourages grounded answers but cannot eliminate hallucinations entirely.

## Run Tests

Run the API tests:

```powershell
python -m pytest tests/test_api.py -v
```

The project also contains manual scripts for testing generation and end-to-end RAG behavior:

```powershell
python -m tests.test_generate_manual
python -m tests.test_rag_manual
```

The manual scripts require Ollama and the configured local model to be available.

## Project Structure

```text
RAG/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── ingest.py
│   ├── retrieve.py
│   ├── embed_store.py
│   ├── generate.py
│   ├── rag.py
│   └── ui.py
├── data/
│   └── company_policy.txt
├── tests/
│   ├── test_api.py
│   ├── test_generate_manual.py
│   └── test_rag_manual.py
├── .gitignore
├── requirements.txt
└── README.md
```

Generated vector databases, virtual environments, and local model caches should remain excluded from version control.

## Current Limitations

- The example uses a small document collection.
- Chunking is tailored to simple text documents with headings.
- Follow-up questions are not yet automatically interpreted using prior conversation history.
- The relevance threshold requires further evaluation.
- Model performance depends on local hardware and model size.

## Potential Improvements

- Context-aware follow-up questions and conversational RAG.
- PDF and Word document ingestion.
- Hybrid search and reranking.
- Retrieval evaluation with a benchmark question set.
- Improved error handling and automated tests.
- Document uploads through the UI.
- Configurable model and retrieval settings.

## License

Add an open-source license before distributing the project if you want to specify how others may use, modify, and redistribute it.

---

Built as a hands-on project to explore local LLMs, vector databases, semantic retrieval, and Retrieval-Augmented Generation.
