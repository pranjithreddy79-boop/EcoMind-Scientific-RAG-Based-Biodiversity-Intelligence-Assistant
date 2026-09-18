from rag.document_loader import load_documents
from rag.chunker import chunk_documents
from rag.embedder import Embedder
from rag.vector_store import VectorStore


def build_index():

    print(
        "Loading knowledge documents..."
    )

    documents = load_documents()

    print(
        f"Documents loaded: {len(documents)}"
    )

    chunks = chunk_documents(
        documents
    )

    print(
        f"Chunks created: {len(chunks)}"
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    metadata = [
        {
            "source": chunk["source"],
            "text": chunk["text"],
            "source_info": chunk["source_info"]
        }
        for chunk in chunks
    ]

    embedder = Embedder()

    print(
        "Creating embeddings..."
    )

    embeddings = embedder.encode(
        texts
    )

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    store = VectorStore(
        embeddings.shape[1]
    )

    store.add(
        embeddings,
        metadata
    )

    store.save()

    print(
        "Vector database created successfully."
    )

    print(
        "Index: data/environment.index"
    )

    print(
        "Metadata: data/environment_metadata.json"
    )


if __name__ == "__main__":
    build_index()