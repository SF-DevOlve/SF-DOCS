import re
from langchain_community.document_loaders import PyPDFLoader
import fitz  # PyMuPDF


def extract_urls(text):
    url_pattern = r'\b(?:https?://)?(?:www\.)?[\w.-]+\.[a-zA-Z]{2,}\b(?:\S*)?'
    urls = re.findall(url_pattern, text)
    return urls

def extract_emails_and_urls(text):
    # Regular expression pattern for emails
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


    # Extracting emails
    emails = re.findall(email_pattern, text)
    # Extracting URLs
    urls = extract_urls(text)

    return urls, emails


def get_emails_urls_from_pages_contents_from(resume_pdf_path: str):
    urls = []
    emails = []
    
    try:
        doc = fitz.open(resume_pdf_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            page_urls, page_emails = extract_emails_and_urls(page_text)
            urls.extend(page_urls)
            emails.extend(page_emails)
        doc.close()
    except Exception as e:
        print(f"Error: {e}")
    
    return urls, emails
