import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

TARGET_URL = "https://sso.sikkim.gov.in/help"
DOWNLOAD_DIR = "data/downloads"

def scrape_pdfs():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(TARGET_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', href=True):
        if link['href'].endswith('.pdf'):
            pdf_url = urljoin(TARGET_URL, link['href'])
            filename = os.path.join(DOWNLOAD_DIR, link['href'].split('/')[-1])
            
            if not os.path.exists(filename):
                print(f"Downloading: {filename}")
                content = requests.get(pdf_url, headers=headers).content
                with open(filename, 'wb') as f:
                    f.write(content)