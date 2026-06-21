# InstantRAG 🚀
### RAG-as-a-Service Platform | Deploy context-aware chatbots from raw PDFs instantly

## What is InstantRAG?
InstantRAG is a modular Retrieval-Augmented Generation engine that lets you deploy a context-aware chatbot from any PDF in minutes — no custom backend required.

Upload a document. Ask questions. Get precise, context-grounded answers.

## The Problem it Solves
Building RAG pipelines from scratch requires setting up embeddings, vector stores, chunking logic, and LLM integration every single time. InstantRAG abstracts all of that into one modular engine you can plug any document into.

## Tech Stack
- **Language:** Python
- **LLM:** Google Gemini 2.5 Flash
- **Vector Database:** Pinecone
- **Embedding Model:** LLaMA Text Embed v2 (via Pinecone Inference)
- **Document Processing:** LangChain (PyPDFLoader, RecursiveCharacterTextSplitter)
- **API Layer:** FastAPI

## Key Features
- 📄 **Instant PDF ingestion:** Automatic chunking and parsing using Langchain.
- 🔍 **Semantic Search:** Embeds queries and documents using LLaMA models and indexes them in Pinecone.
- ⚡ **Optimized Query Latency:** Fast vector search and LLM response generation.
- 🚀 **REST API Ready:** Immediate deployment through an interactive FastAPI UI.

## How It Works
1. Upload a PDF via the `/upload` API endpoint.
2. The document gets automatically chunked and embedded.
3. Embeddings are stored in the Pinecone vector database under a unique namespace.
4. Query the chatbot via `/chat/{namespace_id}` — it retrieves relevant chunks and feeds them to the Gemini LLM.
5. Get precise, context-aware answers grounded in your document!

## Getting Started

### Prerequisites
Make sure you have Python installed. It's recommended to use a virtual environment.

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mujii88/InstantRAG
   cd InstantRAG
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Make sure you have the required API keys for Pinecone and Google Gemini AI in the code or environment setup.

5. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

## API Usage

### 1. Upload a Document
Uploads a PDF, indexes its chunks, and returns a unique namespace and a chat link.

```http
POST /upload
Content-Type: multipart/form-data
```
**Payload:** `file` (UploadFile)

**Response:**
```json
{
  "message": "File uploaded successfully!",
  "namespace": "some-uuid-namespace",
  "chat_link": "http://127.0.0.1:8000/chat/some-uuid-namespace"
}
```

### 2. Query the Chatbot
Ask questions regarding the uploaded document.

```http
POST /chat/{namespace_id}
Content-Type: application/json
```
**Payload:**
```json
{
  "query": "What are the key findings?"
}
```

**Response:**
```json
{
  "query": "What are the key findings?",
  "context_snippets": [
    {
      "id": "rec1",
      "text": "..."
    }
  ],
  "formatted_answer": "Based on the text..."
}
```

## Project Structure
```text
InstantRAG/
├── main.py              # Main FastAPI application with routing and RAG logic
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── .gitignore           # Ignored files for version control
└── ...
```
