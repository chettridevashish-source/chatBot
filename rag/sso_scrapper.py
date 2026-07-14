import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import DOWNLOADS_DIR

TARGET_URL = "https://sso.sikkim.gov.in/help"
REQUEST_TIMEOUT_SECONDS = 30

def scrape_pdfs():
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(TARGET_URL, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', href=True):
        if link['href'].lower().endswith('.pdf'):
            pdf_url = urljoin(TARGET_URL, link['href'])
            filename = DOWNLOADS_DIR / link['href'].split('/')[-1]
            
            if not filename.exists():
                print(f"Downloading: {filename}")
                pdf_response = requests.get(pdf_url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
                pdf_response.raise_for_status()
                temporary_file = filename.with_suffix(".pdf.part")
                temporary_file.write_bytes(pdf_response.content)
                temporary_file.replace(filename)
