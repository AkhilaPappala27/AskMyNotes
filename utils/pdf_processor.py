import fitz


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a single uploaded PDF file.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        str: Extracted text from the PDF
    """

    text = ""

    try:
        # Open PDF from uploaded file
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        # Read each page
        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")

    return text