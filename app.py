import streamlit as st
from utils.pdf_processor import extract_text_from_pdf
from utils.text_chunker import clean_text, chunk_text
from utils.embeddings import (
    generate_embeddings,
    generate_query_embedding
)
from utils.faiss_index import (
    build_vector_store,
    search_vector_store
)
from utils.gemini_helper import generate_answer


# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="AskMyNotes",
    page_icon="📚",
    layout="wide"
)

# ======================================================
# Session State Initialization
# ======================================================

if "vector_stores" not in st.session_state:
    st.session_state.vector_stores = {}

if "processed" not in st.session_state:
    st.session_state.processed = False


# -------------------------------------------------------
# Header
# -------------------------------------------------------
st.title("📚 AskMyNotes")

st.markdown("""
### Learn Smarter with Your Own Study Materials

Upload PDFs, ask questions, and receive AI-powered answers grounded in your uploaded notes.
""")

st.info("💡 Upload one or more PDF files to begin.")

st.divider()


# -------------------------------------------------------
# Upload Section
# -------------------------------------------------------
with st.container(border=True):
    st.subheader("📄 Upload Your Study Materials")
    st.caption("Upload one or more PDF files.")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )
# Reset cached vector stores whenever the uploaded PDFs change.

current_files = sorted([pdf.name for pdf in uploaded_files]) if uploaded_files else []

if st.session_state.get("processed_files") != current_files:
    st.session_state.vector_stores = {}
    st.session_state.processed = False
    st.session_state.processed_files = current_files

# ======================================================
# Process PDFs Only Once
# ======================================================

if uploaded_files and not st.session_state.processed:

    with st.spinner("Indexing your study materials..."):

        for pdf in uploaded_files:

            extracted_text = extract_text_from_pdf(pdf)

            if not extracted_text.strip():
                continue

            cleaned_text = clean_text(extracted_text)

            chunks = chunk_text(cleaned_text)

            chunks = [
                chunk
                for chunk in chunks
                if chunk.strip()
            ]

            embeddings = generate_embeddings(chunks)

            index, stored_chunks = build_vector_store(
                chunks,
                embeddings
            )

            st.session_state.vector_stores[pdf.name] = {
                "index": index,
                "chunks": stored_chunks
            }

        st.session_state.processed = True

    st.success("✅ Study materials indexed successfully!")

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.title("📚 AskMyNotes")
    st.caption("AI-Powered Study Assistant")

    st.divider()

    st.subheader("📊 Project Status")

    if uploaded_files:
        st.success("🟢 Ready to answer questions")
        st.write(f"📄 PDFs Uploaded: {len(uploaded_files)}")
    else:
        st.warning("🟡 Waiting for PDFs")

    st.divider()

    st.subheader("⚙️ Technology Stack")

    st.markdown("""
- 🤖 **LLM:** Gemini 2.5 Flash
- 🧠 **Embeddings:** all-MiniLM-L6-v2
- 🗄 **Vector Database:** FAISS
- 📄 **PDF Parser:** PyMuPDF
- 🌐 **Framework:** Streamlit
""")

# -------------------------------------------------------
# Question Section
# -------------------------------------------------------
with st.container(border=True):

    st.subheader("❓ Ask a Question")

    question = st.text_input(
        "Enter your question"
    )

    col1, col2, col3 = st.columns([2,1,2])

    with col2:
        get_answer = st.button(
            "🚀 Get Answer",
            use_container_width=True,
            disabled=not uploaded_files
        )

# -------------------------------------------------------
# Processing
# -------------------------------------------------------
if get_answer:

    if not uploaded_files:
        st.warning("Please upload at least one PDF.")

    elif not question.strip():
        st.warning("Please enter a question to get an answer.")

    else:

        with st.spinner("Generating your answer..."):

            for pdf in uploaded_files:

                data = st.session_state.vector_stores[pdf.name]

                index = data["index"]
                stored_chunks = data["chunks"]

                # Question Embedding
                query_embedding = generate_query_embedding(question)

                # Semantic Search
                retrieved_chunks = search_vector_store(
                    index,
                    query_embedding,
                    stored_chunks
                )

                # Gemini Answer
                answer = generate_answer(
                    question,
                    retrieved_chunks
                )

                # -------------------------------------------------------
                # AI Answer
                # -------------------------------------------------------

                st.subheader("🤖 AI Answer")

                with st.container(border=True):
                    st.markdown(answer)

                st.divider()

                # -------------------------------------------------------
                # Retrieved Chunks
                # -------------------------------------------------------

                st.subheader("📖 Reference Sections")

                for i, chunk in enumerate(retrieved_chunks):

                    with st.expander(f"📄 Source {i+1}"):

                        st.write(chunk)

                #st.divider()

                # -------------------------------------------------------
                # All Chunks (Debug)
                # -------------------------------------------------------

                #st.subheader(f"📚 Processed Chunks — {pdf.name}")

                #for i, chunk in enumerate(chunks):

                #    with st.expander(f"Chunk {i+1}"):

                #        st.text_area(
                #            "Chunk Content",
                #            value=chunk,
                #            height=180,
                #            key=f"{pdf.name}_{i}",
                #            label_visibility="collapsed"
                #        )
