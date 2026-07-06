# Load the embedding model only once
import streamlit as st
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Converts text chunks into vector embeddings.

    Args:
        chunks (list): List of text chunks.

    Returns:
        embeddings: Vector representations of chunks.
    """

    model = load_embedding_model()
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings