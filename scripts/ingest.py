from app.index.document_loader import load_documents, split_documents
from app.index.vector_store import create_vectorstore

docs = load_documents("data/test.txt")
chunks = split_documents(docs)
create_vectorstore(chunks)
print(f"✅ Indexados {len(chunks)} chunks")