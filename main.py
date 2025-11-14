from fastapi import FastAPI, UploadFile, Form, Body
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai
import uuid
import tempfile
import time

app = FastAPI()

# Initialize Pinecone
pc = Pinecone(api_key="pcsk_6LP2Nw_JUyBgbTTn1Mntt5MbjXUBE8rKtvLkqtY6BaTcVXXAwaJ4sTPQbX5RNXF5Z12RpR")
index_name = "ragsaad"
dense_index = pc.Index(index_name)

# 🔑 Configure Gemini
genai.configure(api_key="AIzaSyB87tiRrbIRp2jCW6_aLm4Zj1nkmR2F-ew")

def extract_records_from_pdf(pdf_path: str):
    """Extracts text chunks from a PDF and returns structured records list."""
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(documents)

    records = []
    for i, chunk in enumerate(chunks, start=1):
        record = {
            "_id": f"rec{i}",
            "text": chunk.page_content.strip(),
            "category": "general"
        }
        records.append(record)

    return records


@app.post("/upload")
async def upload_file(file: UploadFile):
    """Upload a PDF, index it, and return a unique namespace link."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    records = extract_records_from_pdf(tmp_path)
    user_namespace = str(uuid.uuid4())

    dense_index.upsert_records(user_namespace, records)
    time.sleep(5)

    chat_link = f"http://127.0.0.1:8000/chat/{user_namespace}"
    return {
        "message": "File uploaded successfully!",
        "namespace": user_namespace,
        "chat_link": chat_link
    }


@app.post("/chat/{namespace_id}")
async def chat(namespace_id: str, body: dict = Body(...)):
    query = body.get("query")

    # 1️⃣ Embed the query
    embed_response = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=[query],
        parameters={"input_type": "query"}
    )
    query_vector = embed_response.data[0].values

    # 2️⃣ Query Pinecone
    results = dense_index.query(
        namespace=namespace_id,
        vector=query_vector,
        top_k=5,
        include_metadata=True
    )

    # 3️⃣ Prepare context
    context = "\n\n".join(
        [match.metadata.get("text", "") for match in results.matches]
    )

    # 4️⃣ Use Gemini correctly ✅
    model = genai.GenerativeModel("models/gemini-2.5-flash")
 # <-- fixed

    prompt = f"""
    You are a helpful assistant that answers based on the given context.

    🧾 Context:
    {context}

    💬 Question:
    {query}

    Please respond clearly and concisely, formatted in markdown if needed.
    """

    response = model.generate_content(prompt)
    formatted_answer = response.text.strip()

    # 5️⃣ Return structured result
    return {
        "query": query,
        "context_snippets": [
            {"id": match.id, "text": match.metadata.get("text", "")[:200]}
            for match in results.matches
        ],
        "formatted_answer": formatted_answer
    }
