from sso_scrapper import scrape_pdfs
from ingestion.orchestrator import run_ingestion_pipeline

def full_sync():
    print("🚀 Starting Automated Sync...")
    scrape_pdfs()
    run_ingestion_pipeline()
    print("✅ Sync Complete.")

if __name__ == "__main__":
    full_sync()