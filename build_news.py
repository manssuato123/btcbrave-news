"""BTCBRAVE News: RSS/Atom direto, com fallback rss2json e retenção segura.

Dependências: pip install requests beautifulsoup4
Opcional: segredo RSS2JSON_API_KEY no GitHub Actions.
"""
from __future__ import annotations

import json
import os
import re
import html
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlsplit, urlunsplit, parse_qsl, urlencode
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

RSS_FEEDS = [
    # CRYPTO
    ('https://cointelegraph.com/rss', 'crypto'),
    ('https://cryptonews.com/news/feed', 'crypto'),
    ('https://www.coindesk.com/arc/outboundfeeds/rss/', 'crypto'),
    ('https://decrypt.co/feed', 'crypto'),

    # FINANCE / MARKETS
    ('https://finance.yahoo.com/news/rssindex', 'finance'),
    ('https://www.investing.com/rss/news_14.rss', 'finance'),
    ('https://www.marketwatch.com/feeds/topstories', 'finance'),
    ('https://www.cnbc.com/id/100003114/device/rss/rss.html', 'finance'),
    ('https://www.investors.com/news/feed/', 'finance'),
    ('https://www.wsj.com/xml/rss/3_7014.xml', 'finance'),
    ('https://feeds.bbci.co.uk/news/business/rss.xml', 'finance'),
    ('https://www.theguardian.com/business/rss', 'finance'),
    ('https://rss.nytimes.com/services/xml/rss/nyt/Business.xml', 'finance'),

    # WORLD
    ('https://feeds.bbci.co.uk/news/rss.xml', 'world'),
    ('https://feeds.bbci.co.uk/news/world/rss.xml', 'world'),
    ('https://rss.cnn.com/rss/edition.rss', 'world'),
    ('https://www.reutersagency.com/feed/?best-topics=conflict&post_type=best', 'world'),
    ('https://www.aljazeera.com/xml/rss/all.xml', 'world'),
    ('https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'world'),
    ('https://feeds.washingtonpost.com/rss/national', 'world'),
    ('https://www.theguardian.com/world/rss', 'world'),
    ('https://feeds.npr.org/1001/rss.xml', 'world'),
    ('https://apnews.com/hub/apf-topnews?output=xml', 'world'),

    # GAMES
    ('https://www.gamespot.com/feeds/news/', 'games'),
    ('https://www.polygon.com/rss/index.xml', 'games'),
    ('https://www.theverge.com/rss/games/index.xml', 'games'),

    # COOKING
    ('https://www.bonappetit.com/feed/rss', 'food'),
    ('https://www.allrecipes.com/feed/', 'food'),
    ('https://www.thespruceeats.com/rss', 'food'),
    ('https://www.seriouseats.com/rss', 'food'),

    # TECHNOLOGY
    ('https://feeds.bbci.co.uk/news/technology/rss.xml', 'technology'),
    ('https://www.theguardian.com/technology/rss', 'technology'),
    ('https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml', 'technology'),
    ('https://www.theverge.com/rss/tech/index.xml', 'technology'),
    ('https://www.theverge.com/rss/index.xml', 'technology'),
    ('https://techcrunch.com/feed/', 'technology'),
    ('https://feeds.arstechnica.com/arstechnica/index', 'technology'),
    ('https://www.wired.com/feed/rss', 'technology'),
    ('https://www.engadget.com/rss.xml', 'technology'),
    ('https://www.technologyreview.com/feed', 'technology'),
    ('https://www.cnet.com/rss/news/', 'technology'),

    # ARTIFICIAL INTELLIGENCE
    ('https://www.theverge.com/rss/ai-artificial-intelligence/index.xml', 'ai'),
    ('https://techcrunch.com/category/artificial-intelligence/feed/', 'ai'),
    ('https://arstechnica.com/ai/feed/', 'ai'),
]
OUTPUT = Path(__file__).resolve().parent / 'news.json'
MAX_AGE = timedelta(days=7)
MAX_PER_FEED = 300
MAX_TOTAL = 3000
MAX_IMAGE_LOOKUPS = 12
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; BTCBRAVE-NewsBot/2.0; +https://btcbrave.store)',
           'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml, */*'}
RSS2JSON_KEY = os.environ.get('RSS2JSON_API_KEY', '').strip()


def http_url(url):
    if not isinstance(url, str):
        return ''
    url = html.unescape(url.strip())
    p = urlparse(url)
    return url if p.scheme in ('http', 'https') and p.netloc else ''



# Remove apenas parâmetros conhecidos de rastreamento, sem eliminar ?id= etc.
TRACKING_PARAMETERS = {'fbclid', 'gclid', 'dclid', 'igshid', 'mc_cid', 'mc_eid',
                       'at_medium', 'at_campaign', 'traffic_source'}


def canonical_link(link):
    url = http_url(link)
    if not url:
        return ''
    p = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not (k.lower().startswith('utm_') or k.lower() in TRACKING_PARAMETERS)]
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/') or '/',
                       urlencode(query), ''))


def headline_key(title, pubdate):
    # Matérias de dias diferentes podem ter o mesmo título (ex.: boletim diário).
    date = parse_pubdate(pubdate)
    compact = re.sub(r'[^a-z0-9]+', ' ', clean_html(title, 300).lower()).strip()
    return (date.date().isoformat(), compact) if date and compact else None

def parse_pubdate(value):
    """Devolve datetime UTC ou None (nunca inventa data atual)."""
    if not value:
        return None
    value = str(value).strip()
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        try:
            dt = parsedate_to_datetime(value)
        except (ValueError, TypeError, IndexError):
            try:
                dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def clean_html(value, max_length=440):
    if not value:
        return ''
    text = BeautifulSoup(str(value), 'html.parser').get_text(' ', strip=True)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_length].rstrip()


def first_img_markup(value, base):
    if not value:
        return ''
    soup = BeautifulSoup(str(value), 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src') or ''
        result = http_url(urljoin(base, src)) if src else ''
        if result:
            return result
    return ''


def node_text(node, names):
    for child in node:
        tag = child.tag.rsplit('}', 1)[-1].lower()
        if tag in names and child.text and child.text.strip():
            return child.text.strip()
    return ''


def node_link(node):
    for child in node:
        if child.tag.rsplit('}', 1)[-1].lower() == 'link':
            if child.get('href') and child.get('rel', 'alternate') in ('alternate', ''):
                return child.get('href', '')
            if child.text and child.text.strip():
                return child.text.strip()
    return ''


def node_image(node, base, summary):
    for child in node.iter():
        tag = child.tag.rsplit('}', 1)[-1].lower()
        if tag in ('thumbnail', 'content', 'enclosure'):
            src = child.attrib.get('url') or ''
            mime = child.attrib.get('type', '')
            if tag == 'enclosure' and mime and not mime.startswith('image/'):
                continue
            if tag == 'content' and mime and not mime.startswith('image/'):
                continue
            result = http_url(urljoin(base, src)) if src else ''
            if result:
                return result
    return first_img_markup(summary, base)


def parse_xml_feed(content, base, category):
    root = ET.fromstring(content)
    nodes = [node for node in root.iter() if node.tag.rsplit('}', 1)[-1].lower() in ('item', 'entry')]
    if not nodes:
        raise ValueError('Feed sem elementos RSS/Atom')
    out = []
    for node in nodes[:MAX_PER_FEED]:
        title = clean_html(node_text(node, {'title'}), 300)
        link = http_url(urljoin(base, node_link(node)))
        date = node_text(node, {'pubdate', 'published', 'updated', 'date', 'issued'})
        pub = parse_pubdate(date)
        if not title or not link or not pub:
            continue
        raw_desc = node_text(node, {'description', 'summary', 'encoded', 'content'})
        thumb = node_image(node, link, raw_desc)
        out.append({'title': title, 'description': clean_html(raw_desc), 'link': link,
                    'thumbnail': thumb, 'pubDate': pub.isoformat(), 'category': category})
    return out


def parse_json_feed(data, category):
    if data.get('status') != 'ok':
        raise ValueError(f"rss2json status: {data.get('message', data.get('status', 'unknown'))}")
    out = []
    for item in data.get('items', [])[:MAX_PER_FEED]:
        pub = parse_pubdate(item.get('pubDate') or item.get('published'))
        title = clean_html(item.get('title'), 300)
        link = http_url(item.get('link'))
        if not pub or not title or not link:
            continue
        raw = item.get('description') or item.get('content') or ''
        enclosure = item.get('enclosure') or {}
        enclosure_link = enclosure.get('link', '') if isinstance(enclosure, dict) else ''
        thumbnail = http_url(item.get('thumbnail') or enclosure_link)
        if not thumbnail:
            thumbnail = first_img_markup(raw, link)
        out.append({'title': title, 'description': clean_html(raw), 'link': link,
                    'thumbnail': thumbnail, 'pubDate': pub.isoformat(), 'category': category})
    return out


def fetch_feed(feed):
    url, category = feed
    errors = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=(5, 12))
        resp.raise_for_status()
        items = parse_xml_feed(resp.content, url, category)
        if items:
            return (url, items, None)
        errors.append('RSS direto: nenhuma matéria com data válida')
    except Exception as exc:
        errors.append(f'RSS direto: {exc}')

    # Fallback: sem chave, rss2json limita a 10 posts por feed.
    params = {'rss_url': url}
    if RSS2JSON_KEY:
        params.update(api_key=RSS2JSON_KEY, count=100)
    try:
        resp = requests.get('https://api.rss2json.com/v1/api.json', params=params,
                            headers=HEADERS, timeout=(5, 12))
        resp.raise_for_status()
        items = parse_json_feed(resp.json(), category)
        if items:
            return (url, items, None)
        errors.append('rss2json: nenhuma matéria com data válida')
    except Exception as exc:
        errors.append(f'rss2json: {exc}')
    return (url, [], '; '.join(errors))


def fetch_article_image(link):
    try:
        response = requests.get(link, headers=HEADERS, timeout=(4, 7),
                                allow_redirects=True, stream=True)
        response.raise_for_status()
        # Evita transferir artigos muito grandes. Basta o HTML inicial.
        chunks = []
        total = 0
        for chunk in response.iter_content(8192):
            chunks.append(chunk)
            total += len(chunk)
            if total >= 300_000:
                break
        response.close()
        soup = BeautifulSoup(b''.join(chunks), 'html.parser')
        for attrs in ({'property': 'og:image'}, {'name': 'twitter:image'}):
            meta = soup.find('meta', attrs=attrs)
            if meta and meta.get('content'):
                url = http_url(urljoin(link, meta['content']))
                if url:
                    return url
        for img in soup.find_all('img'):
            url = http_url(urljoin(link, img.get('src', '')))
            if url:
                return url
    except requests.RequestException:
        pass
    return ''


def load_old():
    if not OUTPUT.exists():
        return []
    try:
        raw = json.loads(OUTPUT.read_text(encoding='utf-8'))
        return raw if isinstance(raw, list) else []
    except (ValueError, OSError):
        return []


def valid_recent(item, now):
    if not isinstance(item, dict):
        return False
    d = parse_pubdate(item.get('pubDate'))
    return bool(d and now - MAX_AGE <= d <= now + timedelta(minutes=5)
                and http_url(item.get('link')) and item.get('title'))


def main():
    now = datetime.now(timezone.utc)
    previous = load_old()
    fresh = []
    ok_sources = 0
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(fetch_feed, feed) for feed in RSS_FEEDS]
        for future in as_completed(futures):
            url, items, err = future.result()
            if err:
                print(f'[WARN] {url}: {err}', flush=True)
            else:
                ok_sources += 1
                print(f'[OK] {url}: {len(items)} artigos', flush=True)
                fresh.extend(items)

    if ok_sources == 0:
        raise RuntimeError('Nenhum feed respondeu. news.json anterior foi PRESERVADO.')

    # Notícias novas prevalecem; notícias anteriores protegem contra falhas temporárias.
    # Ordenar primeiro faz priorizar a versão mais nova do mesmo link.
    fresh.sort(key=lambda i: i['pubDate'], reverse=True)
    combined = {}
    by_headline = {}
    for item in fresh + previous:
        if not valid_recent(item, now):
            continue
        key = canonical_link(item.get('link'))
        if not key:
            continue
        headline = headline_key(item['title'], item['pubDate'])
        # Duplicação: URL com parâmetros de rastreamento e título idêntico no mesmo dia.
        existing_key = key if key in combined else by_headline.get(headline)
        if existing_key:
            old = combined[existing_key]
            if not old.get('thumbnail') and item.get('thumbnail'):
                old['thumbnail'] = http_url(item['thumbnail'])
            if not old.get('description') and item.get('description'):
                old['description'] = clean_html(item['description'])
            continue
        canonical = {k: item.get(k, '') for k in ('title', 'description', 'link', 'thumbnail', 'pubDate')}
        canonical['title'] = clean_html(canonical['title'], 300)
        canonical['description'] = clean_html(canonical['description'])
        canonical['link'] = key
        canonical['thumbnail'] = http_url(canonical['thumbnail'])
        canonical['pubDate'] = parse_pubdate(canonical['pubDate']).isoformat()
        category = item.get('category')
        if category in {'crypto', 'finance', 'world', 'games', 'food', 'technology', 'ai'}:
            canonical['category'] = category
        combined[key] = canonical
        if headline:
            by_headline[headline] = key

    articles = sorted(combined.values(), key=lambda i: (i['pubDate'], i['link']), reverse=True)[:MAX_TOTAL]

    # Só tenta imagens principais das matérias recentes ainda sem fotografia.
    needs_images = [item for item in articles if not item['thumbnail']][:MAX_IMAGE_LOOKUPS]
    if needs_images:
        with ThreadPoolExecutor(max_workers=6) as pool:
            found = list(pool.map(fetch_article_image, [item['link'] for item in needs_images]))
        for item, thumb in zip(needs_images, found):
            if thumb:
                item['thumbnail'] = thumb

    if not articles:
        raise RuntimeError('Nenhuma notícia recente válida. news.json anterior foi PRESERVADO.')

    payload = json.dumps(articles, ensure_ascii=False, indent=2) + '\n'
    if OUTPUT.exists() and OUTPUT.read_text(encoding='utf-8') == payload:
        print(f'Sem alteração: {len(articles)} notícias; {ok_sources}/{len(RSS_FEEDS)} feeds disponíveis')
        return
    with tempfile.NamedTemporaryFile('w', dir=OUTPUT.parent, prefix='.news-', suffix='.json',
                                     delete=False, encoding='utf-8') as tmp:
        tmp.write(payload)
        temp_path = Path(tmp.name)
    temp_path.replace(OUTPUT)
    print(f'Atualizado: {len(articles)} notícias; {ok_sources}/{len(RSS_FEEDS)} feeds disponíveis')


if __name__ == '__main__':
    main()
