import pandas as pd
import pdfplumber
import docx
import os


# Read the dummy csv
jobs_df = pd.read_csv("jobs.csv")

# Function to loading up the file
def extract_text(file):
    """
    Extract text from a PDF or DOCX file.
    Returns the text as a string.
    """
    filename = file.name if hasattr(file, "name") else file
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    elif ext == ".docx":
        doc = docx.Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX.")

# -----------------------------
# Example usage:
# -----------------------------
file_path = r"C:\Users\chidu\Downloads\Resume-CHIDUBEM-AMECHI-IT-Search.pdf"  # or "example.docx"
content = extract_text(file_path)
print("----- FILE CONTENT START -----")
print(content)
print("----- FILE CONTENT END -----")
