# Qdrant semantic retrieval

1. Create a Qdrant Cloud cluster or run Qdrant locally.
2. Set `RETRIEVAL_BACKEND=qdrant`, `QDRANT_URL`, `QDRANT_API_KEY`, and the embedding settings in `backend/.env`.
3. Prepare a UTF-8 JSONL file with one object per line, e.g. `{"id": 1, "text": "Your content chunk", "source": "manual"}`. IDs must be integers in this starter.
4. From `backend`, activate the virtual environment and run `python -m app.retrieval.ingest_qdrant chunks.jsonl`.
5. Restart the API.

The included Qdrant collection is shared across users. This is suitable only for non-sensitive demo/public content. Add tenant filters or collection isolation before storing private customer knowledge.
