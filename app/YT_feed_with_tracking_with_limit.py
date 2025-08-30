import feedparser
import os
import env
channel_id = env.channel_id
feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
processed_file = "/saved/YT_processed_links.txt"
MAX_TRACKED_LINKS = 100  # Keep only last 100 processed links


def load_processed_links():
    """Read processed links from file (in insertion order)."""
    if not os.path.exists(processed_file):
        return []
    with open(processed_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def save_processed_link(link):
    """Append a processed link and cap file at MAX_TRACKED_LINKS."""
    links = load_processed_links()

    if link not in links:
        links.append(link)  # newest goes at the end
        # Keep only the newest MAX_TRACKED_LINKS
        links = links[-MAX_TRACKED_LINKS:]
        with open(processed_file, "w", encoding="utf-8") as f:
            f.write("\n".join(links) + "\n")


def get_feed_urls():
    """Get new video links from channel RSS feed, oldest first."""
    feed = feedparser.parse(feed_url)
    processed = load_processed_links()
    new_links = []

    # Reverse feed so oldest video comes first
    for entry in reversed(feed.entries[:100]):
        current_link = entry.link
        # Skip Shorts and already processed links
        if "/shorts/" not in current_link and current_link not in processed:
            new_links.append(current_link)

    return new_links


if __name__ == "__main__":
    links = get_feed_urls()
    print("New links to process (oldest first):", links)
