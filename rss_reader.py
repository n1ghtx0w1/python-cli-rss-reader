import feedparser
import datetime
import time
import os

FEEDS_FILE = "feeds.txt"
feeds = []

def fetch_feed(url):
    feed = feedparser.parse(url)
    return feed

def display_feed_items(feed, monitor_mode=False):
    current_time = datetime.datetime.now()
    for i, entry in enumerate(feed.entries):
        color = ""

        if monitor_mode:
            published_time = datetime.datetime(*entry.published_parsed[:6])
            time_diff = current_time - published_time

            if time_diff.total_seconds() <= 900:  # 15 minutes
                color = "\033[91m"  # Red
            elif time_diff.total_seconds() <= 1800:  # 30 minutes
                color = "\033[93m"  # Yellow
            elif time_diff.total_seconds() <= 3600:  # 60 minutes
                color = "\033[94m"  # Blue
            elif time_diff.total_seconds() <= 86400:  # 24 hours
                color = "\033[92m"  # Green
            else:
                continue  # Skip feeds older than 24 hours

        print(f"{color}{i+1}. {entry.title}\033[0m")  # Reset color

def view_feed_item(feed, index):
    if 0 <= index < len(feed.entries):
        entry = feed.entries[index]
        print(f"Title: {entry.title}")
        print(f"Description: {entry.description}")
        print(f"URL: {entry.link}")
    else:
        print("Invalid index.")

def view_feed_items():
    if not feeds:
        print("No feeds available.")
        return

    for i, feed_url in enumerate(feeds):
        print(f"{i+1}. {feed_url}")

    feed_choice = input("Enter the number of the feed to view its items: ")
    try:
        feed_index = int(feed_choice) - 1
        if 0 <= feed_index < len(feeds):
            feed_url = feeds[feed_index]
            feed = fetch_feed(feed_url)
            display_feed_items(feed)
            item_choice = input("Enter the item number to view (0 to go back): ")
            item_index = int(item_choice) - 1
            if item_index == -1:
                return
            view_feed_item(feed, item_index)
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def add_feed():
    url = input("Enter the URL of the RSS feed to add: ")
    feed = fetch_feed(url)
    if feed.entries:
        feeds.append(url)
        print("Feed added successfully.")
        save_feeds()
    else:
        print("Invalid feed URL or no items found.")

def remove_feed():
    if not feeds:
        print("No feeds available.")
        return

    for i, feed_url in enumerate(feeds):
        print(f"{i+1}. {feed_url}")

    choice = input("Enter the number of the feed to remove: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(feeds):
            del feeds[index]
            print("Feed removed successfully.")
            save_feeds()
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def save_feeds():
    with open(FEEDS_FILE, "w") as file:
        for feed_url in feeds:
            file.write(feed_url + "\n")

def load_feeds():
    try:
        with open(FEEDS_FILE, "r") as file:
            feed_urls = file.readlines()
            for url in feed_urls:
                feed = fetch_feed(url.strip())
                if feed.entries:
                    feeds.append(url.strip())
    except FileNotFoundError:
        pass

def display_feed_items_operations(feed):
    current_time = datetime.datetime.now()
    for i, entry in enumerate(feed.entries):
        published_time = datetime.datetime(*entry.published_parsed[:6])
        time_diff = current_time - published_time

        if time_diff.total_seconds() > 86400:  # Skip feeds older than 24 hours
            continue

        color = ""

        if time_diff.total_seconds() <= 900:  # 15 minutes
            color = "\033[91m"  # Red
        elif time_diff.total_seconds() <= 1800:  # 30 minutes
            color = "\033[93m"  # Yellow
        elif time_diff.total_seconds() <= 3600:  # 60 minutes
            color = "\033[94m"  # Blue
        elif time_diff.total_seconds() <= 86400:  # 24 hours
            color = "\033[92m"  # Green

        title = f"{color}{i+1}. {entry.title}\033[0m"  # Reset color
        published = f"Published: {published_time.strftime('%Y-%m-%d %H:%M:%S')}"
        link = f"Link: {entry.link}"

        print(title)
        print(published)
        print(link)
        print()

def operations_monitor():
    os.system("clear" if os.name == "posix" else "cls")
    print("=== Operations Monitor ===")
    print("Operations Monitor will monitor RSS feeds in real-time by fetching data every 60 seconds.")
    print("Color codes:")
    print("\033[91mRed\033[0m = The first 15 minutes of an RSS feed being published.")
    print("\033[93mYellow\033[0m = 15 - 30 minutes of an RSS feed being published.")
    print("\033[94mBlue\033[0m = 30 - 60 minutes of an RSS feed being published.")
    print("\033[92mGreen\033[0m = 1 hour to 24 hours of an RSS feed being published.")
    print()

    while True:
        current_time = datetime.datetime.now()
        for url in feeds:
            feed = fetch_feed(url)
            display_feed_items_operations(feed)

        print("Enter 'q' to return to the previous menu.")
        choice = input("Choice: ")

        if choice.lower() == "q":
            break

        time.sleep(60)
        os.system("clear" if os.name == "posix" else "cls")

def main():
    load_feeds()

    while True:
        print("\n=== RSS Feed Reader ===")
        print("1. Add RSS feed")
        print("2. Remove RSS feed")
        print("3. View feed items")
        print("4. Operations Monitor")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_feed()
        elif choice == "2":
            remove_feed()
        elif choice == "3":
            if not feeds:
                print("No feeds available.")
                continue

            for i, feed_url in enumerate(feeds):
                print(f"{i+1}. {feed_url}")

            feed_choice = input("Enter the number of the feed to view its items: ")
            try:
                feed_index = int(feed_choice) - 1
                if 0 <= feed_index < len(feeds):
                    feed_url = feeds[feed_index]
                    feed = fetch_feed(feed_url)
                    display_feed_items(feed)
                    item_choice = input("Enter the item number to view (0 to go back): ")
                    item_index = int(item_choice) - 1
                    if item_index == -1:
                        continue
                    view_feed_item(feed, item_index)
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "4":
            operations_monitor()
        elif choice == "0":
            save_feeds()
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
