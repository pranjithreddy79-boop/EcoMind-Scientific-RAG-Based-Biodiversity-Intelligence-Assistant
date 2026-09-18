def chunk_text(
    text,
    chunk_size=120,
    overlap=30
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_documents(documents):

    chunks = []

    for document in documents:

        text_chunks = chunk_text(
            document["text"]
        )

        for chunk in text_chunks:

            chunks.append({
                "source": document["source"],
                "text": chunk,
                "source_info": document.get(
                    "source_info"
                )
            })

    return chunks