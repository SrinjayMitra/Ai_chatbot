# AI Customer Support Chatbot

LangChain (Python) RAG chatbot, served over GraphQL via FastAPI + Strawberry,
with a React/Redux frontend that persists chat state across refreshes.

## Stack
- **LangChain (Python)** — retrieval-augmented generation over FAQ docs
- **FastAPI + Strawberry GraphQL** — GraphQL API
- **Chroma** — in-memory vector store for FAQ retrieval
- **React + Redux Toolkit** — chat UI + global state, persisted to localStorage
- **OpenAI** — embeddings + chat completion (swap for a local model if you don't want API costs)

## Setup

### Backend (Python)
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # add your OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```
GraphQL endpoint: http://localhost:8000/graphql
(Strawberry serves an interactive GraphiQL playground at that same URL — good for testing `askBot` queries directly.)

### Frontend (unchanged — React/Redux)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Opens at http://localhost:5173

## Why Python for the backend
LangChain's Python package is the primary, best-documented version of the
library — the JS port lags behind on integrations and examples. Pairing it
with FastAPI (which you already know) and `strawberry-graphql` keeps GraphQL
in the loop without forcing the whole stack into Node. The frontend doesn't
care either way — GraphQL is a protocol, not a language, so React/Redux/Apollo
Client talk to this backend exactly the way they'd talk to a Node one.

## Verifying your resume metrics with real numbers

Don't ship placeholder percentages — generate real ones:

- **Payload size reduction**: `node scripts/measure-payload-size.js` (backend running on :8000)
- **Session state integrity**: `node scripts/simulate-sessions.js 100`
- **Resolution time vs manual doc search**: time yourself answering 10-15
  FAQ questions by manually searching docs, then time the same questions
  through the bot. Average the two and compute the % difference.

## Next steps to make this resume-ready
1. Swap the in-memory Chroma instance for a persisted Chroma or Pinecone store once your FAQ set grows past a few dozen docs.
2. Deploy backend to Render/Railway (FastAPI apps run there natively), frontend to Vercel — a live link is worth more than a repo link.
3. Add a couple of pytest tests for the resolvers and the `ask_bot` chain.
4. Record the real metrics above and update the resume bullets with them.
