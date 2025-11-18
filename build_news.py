import json
import re
import requests
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

# Lista de feeds convertidos via rss2json
RSS_FEEDS = [
    "https://api.rss2json.com/v1/api.json?rss_url=https://cointelegraph.com/rss",
    "https://api.rss2json.com/v1/api.json?rss_url=https://cryptonews.com/news/feed",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://api.rss2json.com/v1/api.json?rss_url=https://finance.yahoo.com/news/rssindex",
    "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.bbci.co.uk/news/rss.xml",
    "https://api.rss2json.com/v1/api.json?rss_url=https://rss.cnn.com/rss/edition.rss",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.reutersagency.com/feed/?best-sectors=crypto"
]

HEADERS = {
    "User-Agent": "BTCBRAVE-NewsBot/1.0 (+https://btcbrave.store)"
}

def parse_pubdate(s, now):
    """Converte texto de data do RSS em datetime (UTC)."""
    if not s:
        return now
    try:
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt
    except Exception:
        return now

def clean_html(text):
    """Remove tags HTML básicas da descrição."""
    if not text:
        return ""
    # remove tags HTML simples
    text = re.sub(r"<[^>]+>", "", text)
    # troca múltiplos espaços/linhas por 1 espaço
    text = re.sub(r"\s+", " ", text).strip()
    return text

def main():
    all_items = []
    seen_links = set()  # evita duplicados
    now = datetime.now(timezone.utc)

    # pega notícias das últimas 36h
    max_age = timedelta(hours=36)

    for url in RSS_FEEDS:
        print("Fetching:", url)
        try:
            r = requests.get(url, timeout=25, headers=HEADERS)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print("Error fetching", url, e)
            continue

        items = data.get("items", [])[:10]  # até 10 de cada feed

        for item in items:
            pub_raw = item.get("pubDate")
            pub_dt = parse_pubdate(pub_raw, now)

            # descarta notícia velha demais
            if now - pub_dt > max_age:
                continue

            link = item.get("link", "")
            if not link or link in seen_links:
                # sem link ou duplicada
                continue
            seen_links.add(link)

            all_items.append({
                "title": item.get("title", "").strip(),
                "description": clean_html(item.get("description", "")),
                "link": link,
                "thumbnail": item.get("thumbnail", ""),
                "pubDate": pub_dt.isoformat()
            })

    # ordena por data (mais recente primeiro)
    all_items.sort(key=lambda x: x["pubDate"], reverse=True)

    # limita a no máximo 300 notícias
    all_items = all_items[:300]

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print("Saved", len(all_items), "items into news.json")

if __name__ == "__main__":
    main()
