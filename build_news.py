import json
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import feedparser

# AGORA USAMOS OS RSS DIRETO, SEM rss2json
RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://cryptonews.com/news/feed",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://finance.yahoo.com/news/rssindex",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://www.reutersagency.com/feed/?best-sectors=crypto"
]

def parse_pubdate(s, now):
    if not s:
        return now
    try:
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return now

def main():
    all_items = []
    now = datetime.now(timezone.utc)
    max_age = timedelta(hours=36)  # notícias até 36h

    for url in RSS_FEEDS:
        print("Fetching:", url)
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print("Error fetching", url, e)
            continue

        entries = feed.entries[:10]

        for entry in entries:
            pub_raw = getattr(entry, "published", "") or getattr(entry, "updated", "")
            pub_dt = parse_pubdate(pub_raw, now)

            if now - pub_dt > max_age:
                continue

            title = getattr(entry, "title", "")
            description = getattr(entry, "summary", "") or getattr(entry, "description", "")
            link = getattr(entry, "link", "")

            # thumbnail simples (muitos feeds não têm imagem)
            thumbnail = ""

            all_items.append({
                "title": title,
                "description": description,
                "link": link,
                "thumbnail": thumbnail,
                "pubDate": pub_dt.isoformat()
            })

    # ordenar por data (mais novas primeiro)
    all_items.sort(key=lambda x: x["pubDate"], reverse=True)

    # limitar a 300 notícias
    all_items = all_items[:300]

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_items)} items into news.json")

if __name__ == "__main__":
    main()
