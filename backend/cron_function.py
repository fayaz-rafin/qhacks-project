import schedule
import time
from recall_rss import fetch_feed
from redis_functions import existing_database, similarity_search
from discord import SyncWebhook
import os
import dotenv

dotenv.load_dotenv()

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]


def check_for_new_recalls(index: str = '1'):
    rss_feed_url = 'https://recalls-rappels.canada.ca/en/feed/cfia-alerts-recalls'
    entries = fetch_feed(rss_feed_url)
    rds = existing_database(index)
    for entry in entries:
        result = similarity_search(rds, entry.title)
        print(result)
        webhook = SyncWebhook.from_url(DISCORD_WEBHOOK)
        webhook.send(result[0])
        # print(entry.title, entry.link)


if __name__ == "__main__":
    # schedule.every(1).minutes.do(my_function)
    schedule.every(60).seconds.do(check_for_new_recalls)

    # Run the scheduler indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a short while to avoid high CPU usage
