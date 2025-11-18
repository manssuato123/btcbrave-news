import json
import requests
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

RSS_FEEDS = [
    "https://api.rss2json.com/v1/api.json?rss_url=https://cointelegraph.com/rss",
    "https://api.rss2json.com/v1/api.json?rss_url=https://cryptonews.com/news/feed",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://api.rss2json.com/v1/api.json?rss_url=https://finance.yahoo.com/news/rssindex",
    "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.bbci.co.uk/news/rss.xml",
    "https://api.rss2json.com/v1/api.json?rss_url=https://rss.cnn.com/rss/edition.rss",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.reutersagency.com/feed/?best-sectors=crypto"
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
  max_age = timedelta(hours=36)

  for url in RSS_FEEDS:
      print("Fetching:", url)
      try:
          r = requests.get(url, timeout=25)
          r.raise_for_status()
          data = r.json()
      except Exception as e:
          print("Error fetching", url, e)
          continue

      items = data.get("items", [])[:10]
      for item in items:
          pub_raw = item.get("pubDate")
          pub_dt = parse_pubdate(pub_raw, now)
          if now - pub_dt > max_age:
              continue

          all_items.append({
              "title": item.get("title", ""),
              "description": item.get("description", ""),
              "link": item.get("link", ""),
              "thumbnail": item.get("thumbnail", ""),
              "pubDate": pub_dt.isoformat()
          })

  all_items.sort(key=lambda x: x["pubDate"], reverse=True)
  all_items = all_items[:300]

  with open("news.json", "w", encoding="utf-8") as f:
      json.dump(all_items, f, ensure_ascii=False, indent=2)

  print(f"Saved", len(all_items), "items into news.json")

if __name__ == "__main__":
  main()
