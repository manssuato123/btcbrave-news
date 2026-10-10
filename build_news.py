<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#05060a">

  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>BTCBRAVE News | Crypto, Markets & World</title>
  <meta name="description" content="BTCBRAVE News: crypto, financial markets, world news, gaming and cooking, updated throughout the day.">
  <style>
    :root {
      --bg-main: #05060a;
      --bg-card: #111318;
      --accent: #d4af37;
      --accent-soft: #ffdd70;
      --text-main: #f5f5f5;
      --text-muted: #a0a4b8;
      --border-soft: #252837;
    }
     
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      background: radial-gradient(circle at top, #151827 0, #05060a 40%, #020308 100%);
      color: var(--text-main);
    }
     
    header {
      background: rgba(5, 6, 10, 0.96);
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-soft);
      position: sticky;
      top: 0;
      z-index: 10;
      backdrop-filter: blur(14px);
    }

    .logo {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: none;
      color: var(--accent);
      font-size: 18px;
    }

    .logo-badge {
      width: 30px;
      height: 30px;
      border-radius: 999px;
      border: 2px solid var(--accent);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
    }

    header nav a {
      margin: 0 10px;
      text-decoration: none;
      color: var(--text-muted);
      font-weight: 500;
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding-bottom: 4px;
      border-bottom: 2px solid transparent;
      transition: 0.2s;
    }

    header nav a:hover {
      color: var(--accent-soft);
      border-bottom-color: var(--accent);
    }

    .filter-bar {
      max-width: 1600px;
      margin: 10px auto 0;
      padding: 8px 18px 0;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }

    .filter-btn {
      background: #111318;
      color: var(--text-muted);
      border: 1px solid var(--border-soft);
      border-radius: 999px;
      padding: 6px 14px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      cursor: pointer;
      transition: 0.18s ease;
    }

    .filter-btn:hover {
      border-color: var(--accent-soft);
      color: var(--accent-soft);
    }

    .filter-btn.active {
      background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899, #f97316);
      color: #ffffff;
      border-color: transparent;
    }

    .loading-news {
      max-width: 1600px;
      margin: 16px auto 0;
      padding: 8px 18px;
      font-size: 13px;
      color: var(--text-muted);
      display: none;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 16px;
      padding: 18px;
      max-width: 1600px;
      margin: 10px auto 0;
    }

    @media (max-width: 1100px) {
      .grid {
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      }
      .grid > .card {
        grid-column: span 1 !important;
      }
    }

    .grid > .card {
      min-height: 240px;
    }

    .grid > .card:nth-child(15n + 1),
    .grid > .card:nth-child(15n + 13) {
      grid-column: span 2;
    }

    .card {
      background: radial-gradient(circle at top left, #202538 0, #111318 45%, #05060a 100%);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 22px 40px rgba(0,0,0,0.6);
      border: 2px solid rgba(255,255,255,0.18);
      transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
      position: relative;
      cursor: pointer;
      display: flex;
      flex-direction: column;
    }

    .card:hover {
      transform: translateY(-3px);
      box-shadow: 0 30px 60px rgba(0,0,0,0.8);
      border-color: rgba(255, 221, 112, 0.4);
    }

    .card-body {
      padding: 16px 18px 18px;
      background: transparent;
      margin-top: auto;
    }

    .title {
      font-size: 19px;
      font-weight: 700;
      margin-bottom: 6px;
      color: #fdfdfd;
    }

    .desc {
      color: var(--text-muted);
      font-size: 14px;
      line-height: 1.5;
      max-height: 72px;
      overflow: hidden;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
    }

    .meta-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 10px;
      font-size: 12px;
      color: var(--text-muted);
    }

    .badge-live {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(220, 53, 69, 0.96);
      color: #fff;
      font-size: 10px;
      padding: 3px 8px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.16em;
    }

    .article-view {
      width: 100%;
      background: radial-gradient(circle at top, #111318 0, #05060a 40%, #020308 100%);
      display: none;
      flex-direction: column;
      padding: 40px 18px 32px;
      position: relative;
    }

    .article-view.open {
      display: flex;
    }

    .article-inner {
      max-width: 960px;
      margin: 0 auto;
      background: #05060a;
      border-radius: 18px;
      padding: 28px 22px 26px;
      border: 1px solid rgba(212, 175, 55, 0.4);
      box-shadow: 0 30px 70px rgba(0,0,0,0.9);
    }

    .article-title {
      font-size: 28px;
      line-height: 1.3;
      font-weight: 800;
      margin-bottom: 12px;
      color: #ffffff;
    }

    .article-body {
      font-size: 14px;
      line-height: 1.7;
      background: #fffcf2 !important;
      color: #000000 !important;
      padding: 20px;
      border-radius: 12px;
      margin-top: 15px;
    }

    .article-close {
      position: fixed;
      top: 120px;
      left: 18px;
      background: #ffffff;
      border: 2px solid rgba(0,0,0,0.7);
      color: #000;
      border-radius: 999px;
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 30px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.7);
      z-index: 9999;
    }

    .article-close:hover {
      background: #ffe891;
      transform: translateY(-1px);
    }

    .news-status { max-width:1600px; margin:0 auto; padding:6px 18px; font-size:12px; color:var(--text-muted); }
    .load-more-wrap { text-align:center; margin:12px 0 32px; }
    .load-more-btn { background:var(--accent); color:#05060a; border:0; border-radius:999px; padding:12px 28px; font-weight:750; cursor:pointer; }
    .load-more-btn:hover { background:var(--accent-soft); }
    .empty-state { text-align:center; padding:28px; color:var(--text-muted); }
    .card-img-placeholder { width:100%; height:180px; display:flex; justify-content:center; align-items:center; background:linear-gradient(135deg,#192036,#0b0e15); font-size:13px; letter-spacing:.18em; color:#d4af37; }
    .grid > .card:nth-child(15n + 1) .card-img-placeholder,
    .grid > .card:nth-child(15n + 13) .card-img-placeholder { height:100%; position:absolute; inset:0; }
    .card-img-small { height:50px; width:100%; object-fit:contain; object-position:bottom; }
    @media (max-width:650px) {
      .grid { grid-template-columns:minmax(0,1fr); gap:12px; padding:12px; }
      .grid > .card { grid-column:span 1 !important; }
      header { padding:12px; }
      .article-view { padding:20px 12px; }
      .article-inner { padding:20px 14px; }
      .article-close { top:78px; left:8px; }
      .logo a { margin-left:0!important; }
    }
    .card-img-medium { width:100%; height:180px; object-fit:cover; display:block; border-bottom:1px solid rgba(255,255,255,0.08); }
    .card-img-large { height:200px; width:100%; object-fit:cover; }

    .btcbrave-login-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.75);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 12000;
    }

    .btcbrave-login-card {
      background: #ffffff;
      color: #111827;
      width: 100%;
      max-width: 420px;
      border-radius: 8px;
      padding: 28px 30px 24px;
      box-shadow: 0 25px 60px rgba(0,0,0,0.5);
      position: relative;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    }

    .btcbrave-login-close {
      position: absolute;
      top: 10px;
      right: 12px;
      border: none;
      background: transparent;
      font-size: 18px;
      cursor: pointer;
    }

    .btcbrave-login-title {
      margin: 0 0 8px;
      font-size: 20px;
      font-weight: 700;
      text-align: center;
    }

    .btcbrave-login-subtitle {
      margin: 0 0 18px;
      font-size: 13px;
      line-height: 1.4;
      text-align: center;
      color: #4b5563;
    }

    .btcbrave-login-footnote {
      margin: 8px 0 0;
      font-size: 11px;
      color: #6b7280;
      text-align: center;
    }

    .grid > .card:nth-child(15n + 1),
    .grid > .card:nth-child(15n + 13) {
      position: relative;
    }

    .grid > .card:nth-child(15n + 1) .card-img-medium,
    .grid > .card:nth-child(15n + 13) .card-img-medium {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      border-bottom: none;
    }

    .grid > .card:nth-child(15n + 1)::before,
    .grid > .card:nth-child(15n + 13)::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(
        to top,
        rgba(0, 0, 0, 0.9) 0%,
        rgba(0, 0, 0, 0.4) 50%,
        rgba(0, 0, 0, 0.0) 100%
      );
      z-index: 1;
    }

    .grid > .card:nth-child(15n + 1) .card-body,
    .grid > .card:nth-child(15n + 13) .card-body {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      margin-top: 0;
      z-index: 2;
      padding: 18px 20px 20px;
    }
  </style>
</head>
<body>

  <iframe name="hiddenBrevoFrame" style="display:none;"></iframe>

  <div id="btcbraveLoginOverlay" class="btcbrave-login-overlay" style="display:none;">
    <div class="btcbrave-login-card">
      <button id="btcbraveLoginClose" class="btcbrave-login-close">×</button>

      <h2 class="btcbrave-login-title">Create your BTCBRAVE alerts</h2>
      <p class="btcbrave-login-subtitle">
        Get price moves, news alerts and updates directly in your inbox.
      </p>

      <form
        id="btcbraveLoginForm"
        action="https://2c3bfeb6.sibforms.com/serve/MUIFAKgSltnznFnj2zjaw4q0uanLuPr2YkDp8mCKOGx7h6wryGbcOg1E9mFahRvBm-kOBCKJOtMy9KAr8gMRb5wpQ6inGj09IQ58wRykX6PTnBjKQa7BQbWUIMTEIc54CEooAtFJHCiYZsoGRvag8I6YxWeVxSqiv_dCO4fEwcbslj8RbwoeIRN9V_5L3R8BiSU8D_unfJRG8BsjcA=="
        method="POST"
        target="hiddenBrevoFrame"
        novalidate
      >
        <label for="btcbraveLoginEmail" style="display:block; font-size:12px; font-weight:600; margin-bottom:4px; color:#374151;">
          Email address
        </label>

        <input
          type="email"
          id="btcbraveLoginEmail"
          name="EMAIL"
          placeholder="Enter your email"
          required
          style="
            width:100%;
            padding:10px;
            border-radius:6px;
            border:1px solid #d1d5db;
            font-size:14px;
            box-sizing:border-box;
          "
        />

        <button
          type="submit"
          style="
            width:100%;
            margin-top:10px;
            padding:10px 0;
            border-radius:999px;
            border:none;
            background:linear-gradient(90deg,#3b82f6,#8b5cf6,#ec4899,#f97316);
            color:#ffffff;
            font-size:14px;
            font-weight:700;
            cursor:pointer;
          "
        >
          Continue
        </button>

        <input type="text" name="email_address_check" value="" style="display:none;">
        <input type="hidden" name="locale" value="en">
      </form>

      <p class="btcbrave-login-footnote">
        Please check your inbox after subscribing. To unsubscribe, use the link in any BTCBRAVE email.
      </p>
    </div>
  </div>

  <header>
    <div class="logo" style="display:flex; flex-direction:column; justify-content:center;">

      <div style="display:flex; align-items:center; gap:10px;">
        <div class="logo-badge" 
             style="width:40px; height:40px; border-radius:999px; border:2px solid var(--accent); 
                    display:flex; align-items:center; justify-content:center; padding:0;">
          <img src="borboleta.png" 
               alt="BTCBRAVE Butterfly Logo" 
               style="width:38px; height:38px; border-radius:50%; object-fit:cover; 
                      object-position:center; background:var(--bg-main);" />
        </div>

        <span style="
            background: linear-gradient(90deg,#1d4ed8,#7c3aed,#ec4899,#f59e0b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 22px;
            text-shadow: 0 0 6px rgba(255,255,255,0.2);">
          BTCBRAVE News
        </span>
      </div>

      <a href="mailto:news@btcbrave.store"
         style="
           margin-left:80px;
           margin-top:2px;
           font-size:12px;
           color:var(--text-muted);
           text-decoration:none;
           display:flex;
           align-items:center;
           gap:6px;">
        <span style="font-size:14px;">📩</span>
        news@btcbrave.store
      </a>

    </div>

    <div id="floating-subscribe" 
      style="
        position:absolute;
        right:24px;
        top:12px;
        display:flex;
        align-items:center;
        justify-content:center;
        width:24px;
        height:24px;
        background:#fff;
        border-radius:999px;
        font-size:12px;
        font-weight:700;
        letter-spacing:0.5px;
        box-shadow:0 8px 20px rgba(0,0,0,0.6);
        cursor:pointer;
        border:1px solid rgba(255,255,255,0.25);">
      🔔
    </div>

    <nav style="display:none;"></nav>
  </header>

  <div class="filter-bar">
    <button class="filter-btn active" data-filter="all">All</button>
    <button class="filter-btn" data-filter="crypto">Crypto</button>
    <button class="filter-btn" data-filter="finance">Finance</button>
    <button class="filter-btn" data-filter="world">World</button>
    <button class="filter-btn" data-filter="games">Games</button>
    <button class="filter-btn" data-filter="food">Cooking</button>
    <button class="filter-btn" data-filter="blog">Blog</button>
  </div>

  <!-- Reader -->
  <div class="article-view" id="articleView">
    <button class="article-close" id="articleClose">×</button>
    <div class="article-inner">
      <div id="articleImage"></div>
      <div class="article-title" id="articleTitle"></div>
      <div class="article-body" id="articleBody"></div>
    </div>
  </div>

  <div id="loadingNews" class="loading-news" role="status">Loading the latest news...</div>
  <div id="newsStatus" class="news-status" role="status" aria-live="polite"></div>

  <!-- Um único grid para tudo (News + Blog intercalados) -->
  <div id="newsGrid" class="btcbrave-grid grid"></div>
  <div class="load-more-wrap" id="loadMoreWrap" style="display:none;">
    <button type="button" id="loadMoreBtn" class="load-more-btn">Load more news</button>
  </div>
  <p id="emptyState" class="empty-state" style="display:none;">No articles found in this category.</p>
  <!-- blogGrid fica só como reserva, mas vazio/sem uso visual -->
  <div id="blogGrid" class="btcbrave-grid grid" style="display:none;"></div>

  <!-- NEWS + BLOG: leitor, categorias, proteção do HTML e atualização a cada 10 minutos -->
  <script>
    const newsGrid = document.getElementById('newsGrid');
    const blogGrid = document.getElementById('blogGrid');
    const loading = document.getElementById('loadingNews');
    const newsStatus = document.getElementById('newsStatus');
    const emptyState = document.getElementById('emptyState');
    const loadMoreWrap = document.getElementById('loadMoreWrap');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const articleView = document.getElementById('articleView');
    const articleTitle = document.getElementById('articleTitle');
    const articleBody = document.getElementById('articleBody');
    const articleClose = document.getElementById('articleClose');
    const articleImageBox = document.getElementById('articleImage');
    const BLOG_POSTS_URL = 'https://blog.btcbrave.store/posts.json';
    const NEWS_REFRESH_MS = 10 * 60 * 1000;
    const RENDER_BATCH_SIZE = 60;
    const BLOG_BATCH_SIZE = 10;
    let globalBlogItems = [];
    let blogReaderActive = false;
    let blogReaderOffset = 0;
    let lastScrollY = 0;
    let refreshInProgress = false;
    let lastCheckAt = 0;
    let lastFingerprint = '';
    let storedNews = [];
    let storedBlog = [];
    let allCombined = [];
    let filteredCombined = [];
    let renderOffset = 0;
    let currentFilter = 'all';

    function safeHttpUrl(value) {
      try {
        if (!plainText(value).trim()) return '';
        const u = new URL(plainText(value).trim(), location.href);
        return ['http:', 'https:'].includes(u.protocol) ? u.href : '';
      } catch (_) { return ''; }
    }

    function plainText(value) {
      return String(value == null ? '' : value);
    }

    function parseDate(value) {
      if (!value) return new Date(0);
      const d = new Date(value);
      return Number.isFinite(d.getTime()) ? d : new Date(0);
    }

    function getSourceName(link) {
      let host = '';
      try { host = new URL(link).hostname.toLowerCase().replace(/^www\./, ''); }
      catch (_) { return 'NEWS'; }
      const names = {
        'cointelegraph.com':'Cointelegraph', 'cryptonews.com':'CryptoNews',
        'coindesk.com':'CoinDesk', 'yahoo.com':'Yahoo Finance',
        'investors.com':'Investors.com', 'wsj.com':'WSJ',
        'investing.com':'Investing.com', 'marketwatch.com':'MarketWatch',
        'bloomberg.com':'Bloomberg', 'cnbc.com':'CNBC', 'forbes.com':'Forbes',
        'bbc.co.uk':'BBC News', 'bbc.com':'BBC News', 'cnn.com':'CNN',
        'reuters.com':'Reuters', 'aljazeera.com':'Al Jazeera',
        'msn.com':'MSN News', 'apnews.com':'AP News', 'nytimes.com':'The New York Times',
        'washingtonpost.com':'The Washington Post', 'gamespot.com':'GameSpot',
        'polygon.com':'Polygon', 'allrecipes.com':'Allrecipes',
        'thespruceeats.com':'The Spruce Eats', 'bonappetit.com':'Bon Appétit'
      };
      const match = Object.keys(names).find(domain => host === domain || host.endsWith('.' + domain));
      return match ? names[match] : host.toUpperCase();
    }

    function getCategory(link) {
      const name = getSourceName(link);
      if (['Cointelegraph','CryptoNews','CoinDesk'].includes(name)) return 'crypto';
      if (['Yahoo Finance','Investors.com','WSJ','Investing.com','MarketWatch','Bloomberg','CNBC','Forbes'].includes(name)) return 'finance';
      if (['GameSpot','Polygon'].includes(name)) return 'games';
      if (['Allrecipes','The Spruce Eats','Bon Appétit'].includes(name)) return 'food';
      if (['BBC News','CNN','Reuters','Al Jazeera','MSN News','AP News','The New York Times','The Washington Post'].includes(name)) return 'world';
      return 'all';
    }

    function createSlug(title) {
      return plainText(title).toLowerCase().normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '').slice(0, 72) || 'article';
    }

    function stableHash(text) {
      let h = 2166136261;
      for (const c of plainText(text)) {
        h ^= c.charCodeAt(0);
        h = Math.imul(h, 16777619);
      }
      return (h >>> 0).toString(36);
    }

    function assignSlug(item, idx) {
      const base = createSlug(item.slug || item.id || item.guid || item.title || 'post-' + idx);
      item._slug = `${base}-${stableHash(item.link || item.title || idx)}`;
    }

    // Só permite tags de formatação e links/imagens HTTP(S) vindos dos posts.
    // Impede scripts, eventos onclick, iframes, estilos perigosos e URLs javascript:.
    const allowedTags = new Set(['p','div','span','br','strong','b','em','i','u',
      'h2','h3','h4','h5','ul','ol','li','blockquote','a','img','pre','code','hr']);
    const forbiddenTags = new Set(['script','style','svg','math','iframe','object','embed',
      'form','input','button','textarea','select','link','meta','base']);

    function appendSafeNode(parent, source) {
      if (source.nodeType === Node.TEXT_NODE) {
        parent.appendChild(document.createTextNode(source.textContent || ''));
        return;
      }
      if (source.nodeType !== Node.ELEMENT_NODE) return;
      const tag = source.tagName.toLowerCase();
      if (forbiddenTags.has(tag)) return;
      if (!allowedTags.has(tag)) {
        Array.from(source.childNodes).forEach(c => appendSafeNode(parent, c));
        return;
      }
      const out = document.createElement(tag);
      if (tag === 'a') {
        const href = safeHttpUrl(source.getAttribute('href'));
        if (href) {
          out.href = href;
          out.target = '_blank';
          out.rel = 'noopener noreferrer';
        }
      }
      if (tag === 'img') {
        const src = safeHttpUrl(source.getAttribute('src'));
        if (!src) return;
        out.src = src;
        out.alt = source.getAttribute('alt') || '';
        out.loading = 'lazy';
        out.style.maxWidth = '100%';
        out.style.height = 'auto';
      }
      Array.from(source.childNodes).forEach(c => appendSafeNode(out, c));
      parent.appendChild(out);
    }

    function appendSafeHtml(parent, markup) {
      const source = new DOMParser().parseFromString('<div>' + plainText(markup) + '</div>', 'text/html');
      const root = source.body.firstElementChild;
      if (root) Array.from(root.childNodes).forEach(c => appendSafeNode(parent, c));
    }

    function makeImage(url, title) {
      const src = safeHttpUrl(url);
      const placeholder = document.createElement('div');
      placeholder.className = 'card-img-placeholder';
      placeholder.textContent = 'BTCBRAVE NEWS';
      if (!src) return placeholder;
      const img = document.createElement('img');
      img.className = 'card-img-medium';
      img.src = src;
      img.alt = title;
      img.loading = 'lazy';
      img.decoding = 'async';
      img.addEventListener('error', () => img.replaceWith(placeholder), {once:true});
      return img;
    }

    function buildCard(item, isBlog, blogIndex) {
      const title = plainText(item.title);
      const link = safeHttpUrl(item.link);
      const category = plainText(item.category || (isBlog ? 'blog' : getCategory(link))).toLowerCase();
      const card = document.createElement('article');
      card.className = 'card';
      card.dataset.category = category;
      card.dataset.source = isBlog ? 'blog' : 'news';
      card.dataset.slug = item._slug || '';
      card.dataset.blogIndex = String(blogIndex ?? 0);
      card.dataset.external = !isBlog ? link : '';
      card.dataset.full = isBlog ? '' : plainText(item.fullText);
      card.tabIndex = 0;
      card.setAttribute('role', 'link');
      card.setAttribute('aria-label', title);
      card.appendChild(makeImage(item.thumbnail, title));

      if (isBlog) {
        const share = document.createElement('button');
        share.type = 'button';
        share.className = 'share-btn';
        share.textContent = '↗ Share';
        Object.assign(share.style, {position:'absolute', top:'12px', right:'12px', zIndex:'5',
          background:'#111',padding:'8px 12px',borderRadius:'10px',cursor:'pointer',
          border:'1px solid #333',color:'#fff'});
        share.addEventListener('click', e => {
          e.stopPropagation();
          const url = link || `https://news.btcbrave.store/?post=${encodeURIComponent(item._slug || '')}`;
          shareBlogPost(url, title);
        });
        card.appendChild(share);
      }

      const body = document.createElement('div');
      body.className = 'card-body';
      const heading = document.createElement('div');
      heading.className = 'title';
      const strong = document.createElement('strong');
      strong.textContent = title;
      heading.appendChild(strong);
      const desc = document.createElement('div');
      desc.className = 'desc';
      const summary = plainText(item.description);
      desc.textContent = summary.length > 120 ? summary.slice(0, 120) + '…' : summary;
      const meta = document.createElement('div');
      meta.className = 'meta-row';
      const date = parseDate(item.pubDate);
      const dateText = date.getTime() ? date.toLocaleDateString() : '';
      meta.textContent = `${dateText} • ${isBlog ? 'BTCBRAVE Blog' : getSourceName(link)}`;
      body.append(heading, desc, meta);
      card.appendChild(body);
      card.addEventListener('click', e => openArticle(item, isBlog, blogIndex, card, e));
      card.addEventListener('keydown', e => {
        if (e.key === 'Enter' && e.target === card) {
          e.preventDefault();
          openArticle(item, isBlog, blogIndex, card, e);
        }
      });
      return card;
    }

    function renderBlogBatch(reset = false) {
      if (reset) articleBody.replaceChildren();
      if (!globalBlogItems.length || blogReaderOffset >= globalBlogItems.length) return;
      const slice = globalBlogItems.slice(blogReaderOffset, blogReaderOffset + BLOG_BATCH_SIZE);
      const fragment = document.createDocumentFragment();
      slice.forEach(post => {
        const article = document.createElement('article');
        article.style.marginBottom = '24px';
        const thumb = safeHttpUrl(post.thumbnail);
        if (thumb) {
          const img = document.createElement('img');
          img.src = thumb;
          img.alt = plainText(post.title);
          img.loading = 'lazy';
          Object.assign(img.style, {width:'100%',maxHeight:'260px',objectFit:'cover',borderRadius:'10px'});
          article.appendChild(img);
        }
        const heading = document.createElement('h3');
        heading.textContent = plainText(post.title);
        heading.style.color = '#111827';
        article.appendChild(heading);
        const date = document.createElement('div');
        date.style.cssText = 'font-size:12px;color:#4b5563;margin-bottom:8px;';
        const d = parseDate(post.pubDate);
        date.textContent = d.getTime() ? d.toLocaleDateString() : '';
        article.appendChild(date);
        const text = document.createElement('div');
        // fullText é HTML do blog; sanitizado antes de inserir no leitor.
        appendSafeHtml(text, post.fullText || post.description || '');
        article.appendChild(text);
        fragment.appendChild(article);
        fragment.appendChild(document.createElement('hr'));
      });
      articleBody.appendChild(fragment);
      blogReaderOffset += slice.length;
    }

    function openArticle(item, isBlog, blogIndex, card, event) {
      if (event?.target?.closest('.share-btn')) return;
      lastScrollY = window.scrollY;
      if (!isBlog && card.dataset.external && !item.fullText) {
        window.location.href = card.dataset.external;
        return;
      }
      articleImageBox.replaceChildren();
      articleTitle.textContent = isBlog ? '' : plainText(item.title);
      if (isBlog && globalBlogItems.length) {
        blogReaderActive = true;
        blogReaderOffset = Number.isInteger(blogIndex) ? blogIndex : 0;
        renderBlogBatch(true);
      } else {
        blogReaderActive = false;
        articleBody.replaceChildren();
        if (safeHttpUrl(item.thumbnail)) {
          const img = document.createElement('img');
          img.src = safeHttpUrl(item.thumbnail);
          img.alt = plainText(item.title);
          img.style.cssText = 'width:100%;max-height:420px;object-fit:contain;border-radius:12px;margin-bottom:20px;';
          articleImageBox.appendChild(img);
        }
        appendSafeHtml(articleBody, item.fullText || item.description || '');
      }
      articleView.classList.add('open');
      articleView.scrollIntoView({behavior:'smooth',block:'start'});
    }

    function closeArticle() {
      articleView.classList.remove('open');
      blogReaderActive = false;
      blogReaderOffset = 0;
      window.scrollTo({top:lastScrollY,behavior:'auto'});
    }
    articleClose.addEventListener('click', closeArticle);
    articleView.addEventListener('click', e => { if (e.target === articleView) closeArticle(); });
    window.addEventListener('scroll', () => {
      if (!blogReaderActive || !articleView.classList.contains('open')) return;
      if (blogReaderOffset >= globalBlogItems.length) return;
      if (articleBody.getBoundingClientRect().bottom - window.innerHeight < 450) renderBlogBatch();
    }, {passive:true});

    function rebuildCombined() {
      const news = storedNews.map((item, i) => {
        const n = {...item, category:item.category || getCategory(item.link)};
        assignSlug(n, i);
        return n;
      }).filter(x => parseDate(x.pubDate).getTime() <= Date.now());
      const blog = storedBlog.map((item, i) => {
        const n = {...item, category:item.category || 'blog'};
        assignSlug(n, i + 10000);
        return n;
      }).filter(x => parseDate(x.pubDate).getTime() <= Date.now());
      news.sort((a,b) => parseDate(b.pubDate) - parseDate(a.pubDate));
      blog.sort((a,b) => parseDate(b.pubDate) - parseDate(a.pubDate));
      globalBlogItems = blog;
      allCombined = [];
      let ni = 0, bi = 0;
      // Mantém o visual original: 1 notícia do blog, 1 notícia externa.
      while (ni < news.length || bi < blog.length) {
        if (bi < blog.length) allCombined.push({item:blog[bi],isBlog:true,blogIndex:bi++});
        if (ni < news.length) allCombined.push({item:news[ni++],isBlog:false});
      }
      applyFilter(currentFilter);
    }

    function renderNextBatch() {
      if (renderOffset >= filteredCombined.length) {
        loadMoreWrap.style.display = 'none';
        return;
      }
      const frag = document.createDocumentFragment();
      const end = Math.min(renderOffset + RENDER_BATCH_SIZE, filteredCombined.length);
      while (renderOffset < end) {
        const {item, isBlog, blogIndex} = filteredCombined[renderOffset++];
        frag.appendChild(buildCard(item, isBlog, blogIndex));
      }
      newsGrid.appendChild(frag);
      loadMoreWrap.style.display = renderOffset < filteredCombined.length ? 'block' : 'none';
    }

    function applyFilter(filter) {
      currentFilter = filter;
      filteredCombined = allCombined.filter(({item,isBlog}) =>
        filter === 'all' || (filter === 'blog' ? isBlog :
          (plainText(item.category || getCategory(item.link)).toLowerCase() === filter)));
      newsGrid.replaceChildren();
      renderOffset = 0;
      emptyState.style.display = filteredCombined.length ? 'none' : 'block';
      renderNextBatch();
    }
    loadMoreBtn.addEventListener('click', renderNextBatch);
    document.querySelector('.filter-bar').addEventListener('click', e => {
      const btn = e.target.closest('.filter-btn');
      if (!btn) return;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.toggle('active', b === btn));
      applyFilter(btn.dataset.filter || 'all');
    });

    // Ao chegar perto do fim da lista visível, carrega mais cards sem criar milhares de nós.
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        if (entries.some(e => e.isIntersecting) && !articleView.classList.contains('open')) renderNextBatch();
      }, {rootMargin:'500px'});
      observer.observe(loadMoreWrap);
    }

    async function fetchJson(url) {
      const target = url + (url.includes('?') ? '&' : '?') + '_=' + Date.now();
      const response = await fetch(target, {cache:'no-store'});
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const json = await response.json();
      if (!Array.isArray(json)) throw new Error('JSON inválido (esperado array)');
      return json;
    }

    async function loadAllNews() {
      if (refreshInProgress) return;
      refreshInProgress = true;
      if (!lastCheckAt) loading.style.display = 'block';
      try {
        const outcomes = await Promise.allSettled([fetchJson('news.json'), fetchJson(BLOG_POSTS_URL)]);
        const okNews = outcomes[0].status === 'fulfilled';
        const okBlog = outcomes[1].status === 'fulfilled';
        if (okNews) storedNews = outcomes[0].value;
        if (okBlog) storedBlog = outcomes[1].value;
        const fingerprint = JSON.stringify([storedNews, storedBlog]);
        if (fingerprint !== lastFingerprint) {
          lastFingerprint = fingerprint;
          rebuildCombined();
        }
        if (okNews || okBlog) {
          const clock = new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
          newsStatus.textContent = (okNews && okBlog ? 'Last checked: ' : 'Some sources unavailable. Last checked: ') + clock;
        } else {
          newsStatus.textContent = 'Unable to refresh. Showing the last available news.';
          console.warn('News fetch failed:', outcomes[0].reason, outcomes[1].reason);
        }
        lastCheckAt = Date.now();

        // Link permanente ao artigo: tenta achar no lote, mesmo quando não está visível.
        const targetSlug = new URLSearchParams(location.search).get('post');
        if (targetSlug && !window._btcbravePermalinkOpened) {
          const idx = allCombined.findIndex(x => x.item._slug === targetSlug);
          if (idx >= 0) {
            window._btcbravePermalinkOpened = true;
            if (currentFilter !== 'all') applyFilter('all');
            while (renderOffset <= idx && renderOffset < filteredCombined.length) renderNextBatch();
            const card = Array.from(newsGrid.querySelectorAll('.card'))[idx];
            if (card) { card.scrollIntoView({block:'center'}); card.click(); }
          }
        }
      } catch (e) {
        console.error('BTCBRAVE refresh error', e);
        newsStatus.textContent = 'Unable to refresh. Check your internet connection.';
      } finally {
        refreshInProgress = false;
        loading.style.display = 'none';
      }
    }

    loadAllNews();
    setInterval(loadAllNews, NEWS_REFRESH_MS);
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden && Date.now() - lastCheckAt > NEWS_REFRESH_MS / 2) loadAllNews();
    });
  </script>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const overlay = document.getElementById('btcbraveLoginOverlay');
      const closeBtn = document.getElementById('btcbraveLoginClose');
      const bell = document.getElementById('floating-subscribe');
      const form = document.getElementById('btcbraveLoginForm');
      const email = document.getElementById('btcbraveLoginEmail');
      const iframe = document.querySelector('iframe[name="hiddenBrevoFrame"]');
      if (!overlay || !form) return;
      const open = () => { overlay.style.display = 'flex'; };
      const close = () => { overlay.style.display = 'none'; };
      const previousRequest = Number(localStorage.getItem('btcbraveSubscribeRequestAt') || 0);
      const recentlySubmitted = previousRequest && Date.now() - previousRequest < 30 * 86400000;
      // Legado: evita mostrar o formulário repetidamente a visitantes antigos.
      const legacy = localStorage.getItem('btcbraveSubscribed') === 'true';
      if (!recentlySubmitted && !legacy) setTimeout(open, 1500);
      closeBtn.addEventListener('click', close);
      overlay.addEventListener('click', e => { if (e.target === overlay) close(); });
      // Sem integração com a API do Brevo não é possível remover a inscrição por aqui.
      // O cancelamento real é feito pelo link unsubscribe de cada email.
      bell?.addEventListener('click', open);
      let submitted = false;
      iframe?.addEventListener('load', () => {
        if (!submitted) return;
        submitted = false;
        alert('Subscription request sent. Please check your inbox for confirmation.');
        close();
      });
      form.addEventListener('submit', event => {
        const value = email.value.trim();
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          event.preventDefault();
          alert('Please enter a valid email address.');
          return;
        }
        // Indica somente envio do formulário, NÃO confirmação de inscrição.
        localStorage.setItem('btcbraveSubscribeRequestAt', String(Date.now()));
        submitted = true;
      });
    });
  </script>

  <script>
    function shareBlogPost(url, title) {
      const text = `Check this article on BTCBRAVE News:\n${title}\n${url}`;

      if (navigator.share) {
        navigator.share({
          title: title,
          text: text,
          url: url
        }).catch(err => {
          console.log("Share failed", err);
        });
        return;
      }

      if (/Android|iPhone|iPad/i.test(navigator.userAgent)) {
        const whatsUrl = `https://wa.me/?text=${encodeURIComponent(text)}`;
        window.open(whatsUrl, '_blank');
        return;
      }

      prompt("Copy this link to share:", url);
    }
  </script>

  <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('/service-worker.js')
          .then(() => console.log("✅ Service Worker registrado com sucesso"))
          .catch((err) => console.error("❌ Erro ao registrar o Service Worker:", err));
      });
    }
  </script>

</body>
</html>
