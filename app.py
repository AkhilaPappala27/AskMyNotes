import streamlit as st
from utils.pdf_processor import extract_text_from_pdf

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
        disabled=len(uploaded_files) == 0
        )
if get_answer:

    if not uploaded_files:
        st.warning("Please upload at least one PDF.")

    else:

        for pdf in uploaded_files:

            extracted_text = extract_text_from_pdf(pdf)

            st.subheader(f"📄 {pdf.name}")

            if extracted_text.strip():
                st.text_area(
                    label="Extracted Text",
                    value=extracted_text,
                    height=300,
                    key=pdf.name
                )
            else:
                st.warning(f"⚠️ No readable text found in **{pdf.name}**. The PDF may be scanned or empty.")

    