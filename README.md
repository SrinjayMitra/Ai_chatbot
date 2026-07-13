# GP AI Product Assistant 🤖

An AI-powered customer support chatbot that helps users find relevant products using **Retrieval-Augmented Generation (RAG)**. The system combines LangChain, vector search, and LLM-based responses to understand user queries and recommend products from company documentation.

The backend is built with **FastAPI + Strawberry GraphQL**, while the frontend uses **React + Redux Toolkit** for a responsive chatbot experience with persistent conversation history.

---

## 🚀 Features

- 🔎 **AI-powered product search**
  - Understands natural language queries
  - Retrieves relevant product information from company documents
  - Provides product recommendations with reasoning

- 🧠 **Retrieval-Augmented Generation (RAG)**
  - Document-based knowledge retrieval
  - Vector similarity search using ChromaDB
  - Reduces hallucinations by grounding responses in company data

- 💬 **Modern chatbot interface**
  - Real-time conversational UI
  - User and AI message separation
  - Product recommendation cards
  - Auto-scrolling chat window
  - Persistent chat history

- ⚡ **GraphQL API**
  - Strawberry GraphQL schema
  - Efficient frontend-backend communication
  - Interactive GraphiQL testing environment

- 💾 **Persistent sessions**
  - Redux Toolkit state management
  - Conversation history stored using localStorage

---

# 🏗️ Architecture

```
                 User
                  |
                  |
          React + Redux Frontend
                  |
                  |
          Apollo GraphQL Client
                  |
                  |
        FastAPI + Strawberry GraphQL
                  |
                  |
             LangChain RAG
                  |
        ---------------------
        |                   |
    Chroma Vector       OpenAI LLM
       Store          Embeddings + Chat
        |
   Product Documents
```

---

# 🛠️ Tech Stack

## Backend

| Technology         | Purpose                 |
| ------------------ | ----------------------- |
| Python             | Backend development     |
| LangChain          | RAG pipeline            |
| FastAPI            | API framework           |
| Strawberry GraphQL | GraphQL server          |
| ChromaDB           | Vector database         |
| OpenAI API         | Embeddings + generation |

## Frontend

| Technology    | Purpose                 |
| ------------- | ----------------------- |
| React         | UI framework            |
| Redux Toolkit | Global state management |
| Apollo Client | GraphQL communication   |
| Vite          | Development environment |

---

# 📂 Project Structure

```
AI-Product-Assistant/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── graphql/
│   │   ├── rag/
│   │   └── embeddings/
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── Message.jsx
│   │   │   └── ProductCard.jsx
│   │   │
│   │   ├── redux/
│   │   └── apollo/
│   │
│   └── package.json
│
└── README.md
```

---

# ⚙️ Installation

## Backend Setup

Clone the repository:

```bash
git clone <repository-url>
cd AI-Product-Assistant
```

Create virtual environment:

```bash
cd backend

python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment variables:

```bash
cp .env.example .env
```

Add your OpenAI key:

```
OPENAI_API_KEY=your_api_key_here
```

Run backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend runs at:

```
http://localhost:8000/graphql
```

---

# Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create environment file:

```bash
cp .env.example .env
```

Run development server:

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🧪 Testing GraphQL API

Open:

```
http://localhost:8000/graphql
```

Example query:

```graphql
query {
  askBot(question: "I need something to stop sewer backflow") {
    productName
    productUrl
    category
    reason
  }
}
```

Example response:

```json
{
  "productName": "Backwater Valve",
  "category": "Plumbing",
  "reason": "Designed to prevent sewer water from flowing back into buildings."
}
```

---

# 🧠 How RAG Works

1. Product documents are loaded into the system.
2. Documents are converted into vector embeddings.
3. Embeddings are stored inside ChromaDB.
4. User queries are converted into embeddings.
5. Similar documents are retrieved.
6. LangChain passes retrieved context to the LLM.
7. The chatbot generates a grounded response.

---

# 🔮 Future Improvements

- Add persistent vector storage using Pinecone or Chroma persistence
- Add authentication and user accounts
- Add product filtering by price/category
- Add analytics dashboard for customer queries
- Deploy backend with Docker
- Add automated tests for GraphQL resolvers

---

# 👨‍💻 Author

**Srinjay Mitra**

Built with React, FastAPI, LangChain, GraphQL, and OpenAI.
