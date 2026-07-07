import streamlit as st
from utils.pdf_processor import extract_text_from_pdf
from utils.text_chunker import clean_text, chunk_text
from utils.embeddings import (generate_embeddings, generate_query_embedding)
from utils.faiss_index import (build_vector_store, search_vector_store)
from utils.gemini_helper import generate_answer

st.set_page_config(page_title="AskMyNotes", page_icon="📚", layout="wide")
st.info("💡 Upload one or more PDFs to enable question answering.")
st.title("📚 AskMyNotes")
st.caption("Learn Smarter with Your Own Study Materials")
st.divider()

upload_container = st.container()

with upload_container:
    st.subheader("📄 Upload Your Study Materials")
    st.caption("Upload one or more PDF files to build your personal knowledge base.")

    uploaded_files = st.file_uploader(
        "Choose one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )


question_container = st.container()

with question_container:
    st.subheader("❓ Ask a Question")
    st.caption("Ask anything about your uploaded study materials.")

    question = st.text_input(
        "Enter your question"
    )

    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        get_answer = st.button(
        "🚀 Get Answer",
        use_container_width=True,
        disabled=not uploaded_files
        )
if get_answer:

    if not uploaded_files:
        st.warning("Please upload at least one PDF.")

    else:

        for pdf in uploaded_files:

            extracted_text = extract_text_from_pdf(pdf)

            if extracted_text.strip():
                cleaned_text = clean_text(extracted_text)
                chunks = chunk_text(cleaned_text)
                chunks = [chunk for chunk in chunks if chunk.strip()]
                embeddings = generate_embeddings(chunks)
                index, stored_chunks = build_vector_store(
                                        chunks,
                                        embeddings
                                    )
                if question.strip():

                    query_embedding = generate_query_embedding(question)
                    #st.write("Query Embedding Shape:", query_embedding.shape)
                    retrieved_chunks = search_vector_store(
                        index,
                        query_embedding,
                        stored_chunks
                    )

                    answer = generate_answer(
                        question,
                        retrieved_chunks
                    )

                    st.subheader("🤖 AI Answer")

                    st.success(answer)
                    st.subheader("🔍 Most Relevant Sections")

                    for i, chunk in enumerate(retrieved_chunks):

                        with st.expander(f"Result {i + 1}"):

                            st.write(chunk)
                else:
                    st.warning("Please enter a question to get an answer.")

                st.subheader(f"📄 {pdf.name}")
                #st.success(f"Total Chunks Created: {len(chunks)}")
                #st.info(f"🧠 Embeddings Generated: {len(embeddings)}")
                #st.write("Embedding Shape:", embeddings.shape)
                #st.success("✅ FAISS Vector Store Created")
                #st.write("Vectors Stored:", index.ntotal)
                #st.write(embeddings[0][:10])  # Display first 10 dimensions of the first embedding

                for i, chunk in enumerate(chunks):
                    with st.expander(f"Chunk {i + 1}",expanded=False):
                        st.text_area(
                            label='Chunk Content',
                            value=chunk,
                            height=180,
                            key=f"{pdf.name}_chunk_{i + 1}",
                            label_visibility="collapsed"
                        )
            else:
                st.warning(f"⚠️ No readable text found in **{pdf.name}**. The PDF may be scanned or empty.")

    