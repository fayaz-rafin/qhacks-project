import feedparser


def fetch_feed(feed_url):
    """
    Fetches and parses an RSS feed from the given URL.

    :param feed_url: The URL of the RSS feed to fetch.
    :return: A list of entries from the parsed feed.
    """
    # Parse the feed
    feed = feedparser.parse(feed_url)

    # Check if parsing was successful
    if feed.get('bozo', 0) == 0:
        return feed.entries
    else:
        print("Error parsing feed:", feed.bozo_exception)
        return []


if __name__ == "__main__":
    # Example usage
    rss_feed_url = 'https://recalls-rappels.canada.ca/en/feed/cfia-alerts-recalls'
    entries = fetch_feed(rss_feed_url)

    # Print titles and links of the latest entries
    for entry in entries:
        print(entry.title, entry.link)