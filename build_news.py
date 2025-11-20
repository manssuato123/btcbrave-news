import json
import re
import requests
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Lista de feeds convertidos via rss2json
RSS_FEEDS = [
    # CRYPTO NEWS
    "https://api.rss2json.com/v1/api.json?rss_url=https://cointelegraph.com/rss",
    "https://api.rss2json.com/v1/api.json?rss_url=https://cryptonews.com/news/feed",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.coindesk.com/arc/outboundfeeds/rss/",

    # FINANCE / BUSINESS
    "https://api.rss2json.com/v1/api.json?rss_url=https://finance.yahoo.com/news/rssindex",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.investing.com/rss/news.rss",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.marketwatch.com/feeds/topstories",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.bloomberg.com/feed/podcast/businessweek.xml",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.investors.com/news/feed/",

    # WORLD NEWS
    "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.bbci.co.uk/news/rss.xml",
    "https://api.rss2json.com/v1/api.json?rss_url=https://rss.cnn.com/rss/edition.rss",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.reutersagency.com/feed/?best-topics=conflict&post_type=best",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.aljazeera.com/xml/rss/all.xml",
    "https://api.rss2json.com/v1/api.json?rss_url=https://rss.msn.com/en-us/",
    "https://api.rss2json.com/v1/api.json?rss_url=https://apnews.com/hub/apf-topnews?output=xml",
    "https://api.rss2json.com/v1/api.json?rss_url=https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.washingtonpost.com/rss/national",

    # GAMES
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.gamespot.com/feeds/news/",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.polygon.com/rss/index.xml",

    # FOOD / COOKING
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.bonappetit.com/feed/rss",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.allrecipes.com/feed/",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.thespruceeats.com/rss",

    # EXTRA (opcionais)
    "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.feedburner.com/forbes/business",
    "https://api.rss2json.com/v1/api.json?rss_url=https://www.wsj.com/xml/rss/3_7014.xml"
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
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def fetch_article_image(link):
    """
    Tenta pegar a imagem principal da página:
    1) <meta property="og:image">
    2) <meta name="twitter:image">
    3) primeira <img>
    """
    if not link:
        return ""

    try:
        resp = requests.get(link, timeout=60, headers=HEADERS)
        resp.raise_for_status()
    except Exception as e:
        print("Error fetching article HTML:", link, e)
        return ""

    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    # 1) og:image
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        src = og["content"].strip()
        if src.startswith("//"):
            src = "https:" + src
        if src.startswith("/"):
            src = urljoin(link, src)
        if src.startswith("http"):
            return src

    # 2) twitter:image
    tw = soup.find("meta", attrs={"name": "twitter:image"})
    if tw and tw.get("content"):
        src = tw["content"].strip()
        if src.startswith("//"):
            src = "https:" + src
        if src.startswith("/"):
            src = urljoin(link, src)
        if src.startswith("http"):
            return src

    # 3) primeira <img>
    img = soup.find("img")
    if img and img.get("src"):
        src = img["src"].strip()
        if src.startswith("//"):
            src = "https:" + src
        if src.startswith("/"):
            src = urljoin(link, src)
        if src.startswith("http"):
            return src

    return ""

def main():
    all_items = []
    seen_links = set()
    now = datetime.now(timezone.utc)
    max_age = timedelta(days=7)

    for url in RSS_FEEDS:
        print("Fetching RSS:", url)
        try:
            r = requests.get(url, timeout=25, headers=HEADERS)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print("Error fetching RSS:", url, e)
            continue

        items = data.get("items", [])[:300]  # até 10 de cada feed

        for item in items:
            pub_raw = item.get("pubDate")
            pub_dt = parse_pubdate(pub_raw, now)

            # descarta notícia velha demais
            if now - pub_dt > max_age:
                continue

            link = item.get("link", "").strip()
            if not link or link in seen_links:
                continue
            seen_links.add(link)

            # thumbnail vinda do RSS
            thumb = (item.get("thumbnail") or "").strip()

            # se não for uma URL http válida, tenta buscar da página
            if not (thumb.startswith("http://") or thumb.startswith("https://")):
                print("  No valid thumbnail in RSS, fetching from article:", link)
                thumb = fetch_article_image(link)

            all_items.append({
                "title": item.get("title", "").strip(),
                "description": clean_html(item.get("description", "")),
                "link": link,
                "thumbnail": thumb,
                "pubDate": pub_dt.isoformat()
            })

    # ordena por data (mais recente primeiro)
    all_items.sort(key=lambda x: x["pubDate"], reverse=True)

    # limita a no máximo 1000 notícias
    all_items = all_items[:3000]

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print("Saved", len(all_items), "items into news.json")

if __name__ == "__main__":
    main()
