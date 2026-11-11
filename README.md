# AI Assistant Framework

A modular, provider-backed AI assistant built with **FastAPI**, **Next.js**, and **Python**. The framework provides a foundation for building conversational AI applications with authentication, user-specific conversations, language model integration, and optional retrieval-augmented generation (RAG).

Designed as an independent and extensible project, it can be adapted to different applications and use cases.

## Features

- **Authentication:** Email and password registration and login.
- **Secure password storage:** Password hashing using PBKDF2-HMAC-SHA256.
- **Token-based authentication:** Signed bearer tokens for authenticated API access.
- **Conversation management:** Create, retrieve, and manage conversations.
- **User data isolation:** Conversations are associated with their owners, with ownership checks on protected operations.
- **LLM integration:** Gemini provider adapter for AI-generated responses.
- **Retrieval-augmented generation:** Optional retrieval layer with a lightweight demo implementation.
- **Vector search:** Optional Qdrant integration for semantic retrieval.
- **Web interface:** Next.js application with registration, login, and chat functionality.
- **Testing:** Automated tests covering authentication and conversation ownership.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | Next.js, React, TypeScript |
| Database | SQLAlchemy, SQLite by default |
| Authentication | Signed bearer tokens, PBKDF2 |
| AI provider | Google Gemini |
| Retrieval | Demo retriever, Qdrant |
| Testing | Pytest |

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── providers/
│   │   ├── retrieval/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── tests/
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   └── lib/
│   └── package.json
│
├── docs/
│   └── qdrant.md
│
├── examples/
├── .gitignore
└── README.md
```

## Requirements

- Python 3.11 or later
- Node.js 20 or later
- npm
- A Google Gemini API key for AI-generated responses

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/MoomFamily/moom-family-ai-assistant.git
cd moom-family-ai-assistant
```

### 2. Configure the backend

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment.

**Windows — Git Bash:**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

Create the local environment file:

```bash
cp .env.example .env
```

Update the configuration in `backend/.env`:

```env
APP_NAME=AI Assistant
APP_ENV=development
DATABASE_URL=sqlite:///./assistant.db
SECRET_KEY=YOUR_RANDOM_SECRET_KEY
ACCESS_TOKEN_MINUTES=60
ALLOWED_ORIGINS=http://localhost:3000

LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

RETRIEVAL_ENABLED=true
RETRIEVAL_BACKEND=demo
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Replace the placeholder values with your own credentials. Never commit `.env` or share API keys.

### 3. Start the backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Health check:

`http://127.0.0.1:8000/health`

### 4. Configure the frontend

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

`http://localhost:3000`

## Testing

### Backend

From the `backend` directory:

```bash
python -m pytest -q
python -m compileall -q app tests
```

### Frontend

From the `frontend` directory:

```bash
npm run lint
npx tsc --noEmit
npm run build
```

## Retrieval and Vector Search

The framework includes two retrieval options:

**Demo retrieval**

The default demo retriever provides a lightweight lexical retrieval implementation for development and experimentation.

**Qdrant retrieval**

Qdrant can be configured for vector-based semantic retrieval.

To enable it, configure the relevant environment variables:

```env
RETRIEVAL_BACKEND=qdrant
QDRANT_URL=YOUR_QDRANT_URL
QDRANT_API_KEY=YOUR_QDRANT_API_KEY
```

The project includes a JSONL ingestion utility using Gemini embeddings.

For configuration details, see [`docs/qdrant.md`](docs/qdrant.md).

## API Overview

The backend provides endpoints for:

- User registration and authentication.
- Authenticated conversation creation and retrieval.
- Sending messages within conversations.
- Health monitoring.

Interactive API documentation is available through FastAPI at:

`http://127.0.0.1:8000/docs`

## Security

The project includes password hashing, signed authentication tokens, and conversation ownership checks.

For deployment in a production environment, additional measures should be implemented and validated, including:

- HTTPS and secure token handling.
- Rate limiting and abuse protection.
- Email verification and password recovery.
- Token refresh and revocation.
- Database migrations and backups.
- Monitoring, logging, and dependency security scanning.
- Tenant isolation for private knowledge stored in vector databases.

The current Qdrant implementation uses a shared collection. It should not be used for private, multi-user knowledge without implementing and testing appropriate tenant isolation.

## License

The license for this project will be specified in the repository once selected.

---

Developed by **Moom Family**.