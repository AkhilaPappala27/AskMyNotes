import faiss
import numpy as np


def build_vector_store(chunks, embeddings):
    """
    Builds a FAISS index from embeddings.

    Args:
        chunks (list): List of text chunks.
        embeddings (numpy.ndarray): Embedding vectors.

    Returns:
        index: FAISS index
        chunks: Original text chunks
    """

    # Convert embeddings to float32 (required by FAISS)
    embeddings = np.array(embeddings).astype("float32")

    # Get embedding dimension
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings
    index.add(embeddings)

    return index, chunks



def search_vector_store(index, query_embedding, chunks, top_k=3):
    """
    Search the FAISS index and return the most relevant chunks.
    """

    top_k = min(top_k, len(chunks))
    # Convert to numpy float32
    query_embedding = np.asarray(query_embedding, dtype=np.float32)


    distances, indices = index.search(query_embedding, top_k)

    retrieved_chunks = [
        chunks[i] for i in indices[0]
    ]

    return retrieved_chunks