import os
from app.index.document_loader import load_documents, split_documents
from app.index.vector_store import create_vectorstore

all_chunks = []

for filename in os.listdir("data"):
    if filename.endswith((".pdf", ".txt")):
        file_path = os.path.join("data", filename)
        print(f"📄 Cargando: {filename}")
        docs = load_documents(file_path)
        chunks = split_documents(docs)
        all_chunks.extend(chunks)
        print(f"   → {len(chunks)} chunks")

create_vectorstore(all_chunks)
print(f"✅ Total indexados: {len(all_chunks)} chunks")