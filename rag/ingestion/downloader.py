from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class PDFDownloader:
    def __init__(self, base_url: str, download_dir: str):
        self.base_url = base_url
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                )
            }
        )

    def fetch_page(self) -> str:
        """Download the HTML of the target page."""

        response = self.session.get(self.base_url, timeout=20)
        response.raise_for_status()
        return response.text

    def extract_pdf_links(self, html: str) -> list[str]:
        """Extract every PDF link from the page."""

        soup = BeautifulSoup(html, "html.parser")

        pdf_links = set()

        for link in soup.find_all("a", href=True):
            href = link["href"]

            if ".pdf" in href.lower():
                pdf_links.add(urljoin(self.base_url, href))

        return sorted(pdf_links)

    def download_pdf(self, pdf_url: str):
        """Download a single PDF."""

        filename = Path(urlparse(pdf_url).path).name

        destination = self.download_dir / filename

        if destination.exists():
            print(f"[SKIP] {filename}")
            return

        print(f"[DOWNLOAD] {filename}")

        response = self.session.get(pdf_url, timeout=60)
        response.raise_for_status()

        with open(destination, "wb") as f:
            f.write(response.content)

        print(f"[SAVED] {destination}")

    def download_all(self):
        """Download every discovered PDF."""

        html = self.fetch_page()

        pdf_links = self.extract_pdf_links(html)

        print(f"\nFound {len(pdf_links)} PDF(s).\n")

        for pdf in pdf_links:
            self.download_pdf(pdf)