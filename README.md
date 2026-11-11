# Standalone AI Assistant Framework

A generic, provider-backed assistant starter with FastAPI, Next.js, email/password authentication, per-user conversation ownership, optional retrieval, and a Qdrant vector-search adapter. It is independent of any client-specific product or dataset.

## What is included
- FastAPI API with registration, login, signed bearer tokens, and authenticated conversation endpoints.
- PBKDF2-HMAC-SHA256 password hashing.
- Conversation ownership checks on every read/write operation.
- Gemini generation adapter and a small demo retriever.
- Optional Qdrant vector retrieval and JSONL ingestion helper.
- Minimal Next.js login/register/chat interface.
- Security and ownership tests.

## Local setup
Requirements: Python 3.11+, Node.js 20+.

### Backend
```bash
cd backend
python -m venv .venv
# Git Bash on Windows: source .venv/Scripts/activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env: set a long random SECRET_KEY and GEMINI_API_KEY
uvicorn app.main:app --reload
```
Health check: http://127.0.0.1:8000/health

### Frontend
In another terminal:
```bash
cd frontend
npm install
# create .env.local with NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
npm run dev
```
Open http://localhost:3000.

## Tests and checks
```bash
cd backend
pytest -q
python -m compileall -q app tests
cd ../frontend
npm run lint
npx tsc --noEmit
npm run build
```

## Qdrant (optional)
The default `RETRIEVAL_BACKEND=demo` uses a tiny lexical demo corpus. For semantic retrieval, configure a Qdrant instance and set `RETRIEVAL_BACKEND=qdrant`, `QDRANT_URL`, and `QDRANT_API_KEY`. The included ingestion utility uses Gemini embeddings. See `docs/qdrant.md`.

## Important security boundaries
This is a development baseline, not a production-certified service. Before production: use HTTPS; move tokens from localStorage to Secure/HttpOnly/SameSite cookies; add rate limiting, email verification, password reset, refresh-token rotation/revocation, migrations, backups, monitoring, abuse controls, provider timeouts, and security/dependency scanning. Qdrant ingestion currently targets one shared collection: do not store customer-private knowledge until tenant-aware filtering or collection isolation is implemented and tested.

## Open-source publication checklist
Choose a license; review intellectual property and dependencies; inspect all tracked files for secrets and private data; add CI and a security policy; then publish. No license is included intentionally. Do not include private customer data, proprietary prompts, private datasets, production credentials, or client-specific source code.
