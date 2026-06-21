<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=InstantRAG%20%F0%9F%9A%80&fontSize=80&animation=fadeIn" />
  
  <h3>RAG-as-a-Service Platform | Deploy context-aware chatbots from raw PDFs instantly</h3>

  <p>
    <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI"></a>
    <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
    <a href="https://www.pinecone.io/"><img src="https://img.shields.io/badge/Pinecone-000000?style=for-the-badge&logo=pinecone&logoColor=white" alt="Pinecone"></a>
    <a href="https://python.langchain.com/"><img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"></a>
    <a href="https://deepmind.google/technologies/gemini/"><img src="https://img.shields.io/badge/Gemini_2.5-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white" alt="Gemini"></a>
  </p>
</div>

---

<details open>
  <summary><b>✨ What is InstantRAG?</b></summary>
  <br/>
  InstantRAG is a modular Retrieval-Augmented Generation engine that lets you deploy a context-aware chatbot from any PDF in minutes — no custom backend required.
  <br/><br/>
  Upload a document. Ask questions. Get precise, context-grounded answers.
</details>

<details>
  <summary><b>🛠️ The Problem it Solves</b></summary>
  <br/>
  Building RAG pipelines from scratch requires setting up embeddings, vector stores, chunking logic, and LLM integration every single time. InstantRAG abstracts all of that into one modular engine you can plug any document into.
</details>

---

## 🚀 Key Features
- 📄 **Instant PDF Ingestion:** Automatic chunking and parsing using Langchain.
- 🔍 **Semantic Search:** Embeds queries and documents using LLaMA models and indexes them in Pinecone.
- ⚡ **Optimized Query Latency:** Fast vector search and LLM response generation.
- 🧩 **REST API Ready:** Immediate deployment through an interactive FastAPI UI.

## ⚙️ How It Works

1. **Upload** a PDF via the `/upload` API endpoint.
2. The document gets automatically **chunked and embedded**.
3. Embeddings are stored in the Pinecone **vector database** under a unique namespace.
4. **Query the chatbot** via `/chat/{namespace_id}` — it retrieves relevant chunks and feeds them to the Gemini LLM.
5. Get precise, context-aware answers grounded in your document!

---

## 💻 Getting Started

<details>
<summary><b>1️⃣ Prerequisites & Setup</b></summary>
<br/>

Make sure you have Python installed. It's recommended to use a virtual environment.

```bash
# Clone the repository
git clone https://github.com/mujii88/InstantRAG
cd InstantRAG

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the dependencies
pip install -r requirements.txt
```
</details>

<details>
<summary><b>2️⃣ Run the Application</b></summary>
<br/>

```bash
uvicorn main:app --reload
```
*Your interactive API documentation will be available at `http://127.0.0.1:8000/docs`.*
</details>

---

## 🔌 API Usage

### 📤 1. Upload a Document
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

### 💬 2. Query the Chatbot
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

---
<div align="center">
  <sub>Built with 💖 by Mujtaba Ahmed</sub>
</div>
