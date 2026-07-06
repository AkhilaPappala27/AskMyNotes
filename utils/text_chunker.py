from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

def clean_text(text):
    """
    Removes unnecessary whitespace from extracted PDF text.
    """
    text=re.sub(r"[ \t]+", " ", text)
    text=re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text, chunk_size=500, chunk_overlap=100):
    """
    Splits text into meaningful overlapping chunks using
    LangChain's RecursiveCharacterTextSplitter.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_text(text)

    return chunks