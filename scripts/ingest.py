import json
import os
from pathlib import Path

from langchain_core.documents import Document

from app.index.document_loader import load_documents, split_documents
from app.index.vector_store import create_vectorstore


def load_local_chunks(data_dir: str = "data") -> list:
    all_chunks = []

    for filename in os.listdir(data_dir):
        if filename.endswith((".pdf", ".txt")):
            file_path = os.path.join(data_dir, filename)
            print(f"📄 Cargando: {filename}")
            docs = load_documents(file_path)

            for doc in docs:
                doc.metadata["source_type"] = "document"
                doc.metadata["source_name"] = filename

            chunks = split_documents(docs)
            all_chunks.extend(chunks)
            print(f"   → {len(chunks)} chunks")

    return all_chunks


def load_faq_chunks(path: str = "data/faq/faqs.json") -> list:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    for i, item in enumerate(data, start=1):
        docs.append(
            Document(
                page_content=f"Pregunta: {item['question']}\nRespuesta: {item['answer']}",
                metadata={
                    "source_type": item.get("source_type", "faq"),
                    "topic": item.get("topic"),
                    "product": item.get("product"),
                    "source_name": Path(path).name,
                    "chunk_id": f"faq-{i:03d}",
                },
            )
        )

    print(f"❓ Cargando FAQs: {Path(path).name}")
    chunks = split_documents(docs)
    print(f"   → {len(chunks)} chunks")
    return chunks


def main():
    local_chunks = load_local_chunks()
    faq_chunks = load_faq_chunks()

    all_chunks = local_chunks + faq_chunks

    create_vectorstore(all_chunks)
    print(f"✅ Total indexados: {len(all_chunks)} chunks")


if __name__ == "__main__":
    main()