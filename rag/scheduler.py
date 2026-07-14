import schedule
import time
from sync_all import full_sync

# Schedule sync every day at 2 AM
schedule.every().day.at("02:00").do(full_sync)

while True:
    schedule.run_pending()
    time.sleep(60)