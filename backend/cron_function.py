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
    """
    Check for new recalls by fetching the RSS feed from the given URL,
    comparing the titles with the existing database, and sending a webhook
    message with the recall details.

    :param index: The index of the existing database to search in (default: '1')
    :type index: str
    :return: None
    """
    rss_feed_url = 'https://recalls-rappels.canada.ca/en/feed/cfia-alerts-recalls'
    entries = fetch_feed(rss_feed_url)
    rds = existing_database(index)
    for entry in entries:
        result = similarity_search(rds, entry.title)
        score = result[0][1]
        metadata = result[0][0].metadata
        message = (
            f"Recall for {entry.title}: \nProduct: {metadata['description']}\nMerchant: {metadata['merchant_name']}\n"
            f"Date: {metadata['transaction_date']}\nLink: {entry.link}\nConfidence: {round((1 - score) * 100, 2)}%")
        webhook = SyncWebhook.from_url(DISCORD_WEBHOOK)
        webhook.send(message)
    return None


def sample_recall(index: str = '1', product: str = 'Cookie'):
    """
    This function sends a recall message for a given product.

    :param index: The index of the database to search in (default is '1').
    :param product: The name of the product to search for (default is 'Cookie').
    :return: None
    """
    webhook = SyncWebhook.from_url(DISCORD_WEBHOOK)
    rds = existing_database(index)
    result = similarity_search(rds, product)
    # print(result)
    score = result[0][1]
    metadata = result[0][0].metadata
    message = (f"Recall for {product}: \nProduct: {metadata['description']}\nMerchant: {metadata['merchant_name']}\n"
               f"Date: {metadata['transaction_date']}\nLink: https://recalls-rappels.canada.ca/en/alert-recall/alumauy-brand-sweet-pepper-ground-spice-recalled-due-undeclared-gluten\nConfidence: {round((1 - score) * 100, 2)}%")
    webhook.send(message)
    return None

if __name__ == "__main__":
    # schedule.every(1).minutes.do(my_function)
    schedule.every(60).seconds.do(check_for_new_recalls)

    # Run the scheduler indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a short while to avoid high CPU usage
