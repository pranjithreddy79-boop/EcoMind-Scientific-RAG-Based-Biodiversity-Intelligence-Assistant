from rag.embedder import Embedder
from rag.vector_store import VectorStore


class Retriever:

    def __init__(self):

        self.embedder = Embedder()

        self.store = VectorStore.load()

    def retrieve(
        self,
        query,
        top_k=3
    ):

        query_embedding = (
            self.embedder.encode([query])
        )

        results = self.store.search(
            query_embedding,
            top_k=top_k
        )

        return results


if __name__ == "__main__":

    retriever = Retriever()

    query = input(
        "Enter your environmental question: "
    )

    results = retriever.retrieve(
        query,
        top_k=3
    )

    print(
        "\n===== SCIENTIFIC EVIDENCE =====\n"
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"Result {i}"
        )

        print(
            f"Relevance: "
            f"{result['score']:.4f}"
        )

        print(
            f"File: {result['source']}"
        )

        source = result.get(
            "source_info"
        )

        if source:

            print(
                f"Scientific source: "
                f"{source['title']}"
            )

            print(
                f"Organization: "
                f"{source['organization']}"
            )

            print(
                f"Type: {source['type']}"
            )

            print(
                f"URL: {source['url']}"
            )

        print(
            f"\nEvidence:\n"
            f"{result['text']}"
        )

        print("-" * 80)