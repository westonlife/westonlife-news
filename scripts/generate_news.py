"""Weston Life: verified daily bilingual news publisher (Python standard library)."""
import html
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
BOSTON = ZoneInfo("America/New_York")
# Weston Life 2026-10-22: five local articles and ten U.S./world articles.
# Each query is under NewsAPI's free-text query limit. Sources are shown explicitly.
LOCAL_QUERIES = [
    '("Weston" AND "Massachusetts") OR "Weston MA"',
    '("Weston" AND ("school" OR "Select Board" OR "construction" OR "leaf blower"))',
    '("Boston" OR "Massachusetts") AND ("schools" OR "housing" OR "local government" OR "town meeting" OR "community")',
    '("Waltham" OR "Lexington" OR "Newton" OR "Wellesley") AND "Massachusetts"',
    '("Boston" OR "Massachusetts") AND ("events" OR "exhibition" OR "festival" OR "real estate")',
]
WORLD_QUERIES = [
    '("Iran" AND ("United States" OR "war" OR "Middle East")) OR "Hormuz"',
    '("Nasdaq" OR "S&P 500" OR "QQQ" OR "Federal Reserve" OR "Treasury yield")',
    '("Nvidia" OR "Microsoft" OR "Google" OR "Broadcom" OR "Tesla") AND ("AI" OR "earnings" OR "stocks")',
    '("OpenAI" OR "artificial intelligence" OR "AI technology" OR "robotics")',
    '("China" AND ("economy" OR "technology" OR "art" OR "culture" OR "dance"))',
    '("United States" OR "U.S.") AND ("economy" OR "policy" OR "Congress")',
    '("Harvard" OR "MIT" OR "college admissions" OR "SAT" OR "AP exams")',
    '("global economy" OR "international relations" OR "oil prices" OR "world news")',
]
TOPICS = [("Weston / Boston / Massachusetts", "", 5), ("World News / Global", "", 10)]
LOCAL_HINTS = ("massachusetts", "boston", "weston", "waltham", "lexington", "wellesley", "newton", "needham", "cambridge", "middlesex", "natick", "wayland", "belmont", "brookline", "metrowest", "framingham")
LOCAL_HIGH_PRIORITY = ("weston", "school committee", "school building", "leaf blower", "town meeting", "select board", "planning board", "building project", "zoning", "college", "graduation")
WORLD_FOCUS = ("iran", "israel", "war", "middle east", "oil", "nasdaq", "stock", "wall street", "fed", "federal reserve", "nvidia", "microsoft", "google", "broadcom", "tesla", "openai", "artificial intelligence", "china", "university", "admissions")
BLOCKED_DOMAINS = ("slashdot.org", "alltoc.com")

def get_json(url, headers=None, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers=headers or {}, method="POST" if data else "GET")
    with urlopen(request, timeout=35) as response:
        return json.loads(response.read().decode("utf-8"))

def _fetch_news(query, cutoff, key, page_size=80):
    params = urlencode({"q": query, "language": "en", "sortBy": "publishedAt",
                        "pageSize": page_size, "from": cutoff, "apiKey": key})
    try:
        result = get_json("https://newsapi.org/v2/everything?" + params)
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"News search temporarily unavailable: {exc}", file=sys.stderr)
        return []
    if result.get("status") != "ok":
        print("News search error: " + str(result.get("message", "unknown")), file=sys.stderr)
        return []
    return result.get("articles") or []


OFFICIAL_LOCAL_RSS = [
    "https://www.westonschools.org/high/feed/",
    "https://www.westonschools.org/feed/",
    "https://www.westonma.gov/RSSFeed.aspx?CID=Latest-Town-News-1&ModID=1",
    "https://www.westonma.gov/RSSFeed.aspx?CID=School-Committee-34&ModID=65",
]


def _feed_articles(url):
    """Read officially provided RSS. Fail open so one feed never breaks publication."""
    if os.getenv("WESTONLIFE_SKIP_RSS") == "1":
        return []
    try:
        req = Request(url, headers={"User-Agent":"WestonLife/1.0 (community-news-aggregator)"})
        with urlopen(req, timeout=16) as response:
            content = response.read(1_000_000)
        tree = ElementTree.fromstring(content)
        articles = []
        for item in tree.findall('.//item')[:30]:
            title = (item.findtext('title') or '').strip()
            desc = re.sub('<[^>]+>', ' ', html.unescape(item.findtext('description') or ''))
            link = (item.findtext('link') or '').strip()
            try:
                stamp = parsedate_to_datetime(item.findtext('pubDate')).astimezone(timezone.utc)
            except (ValueError, TypeError, AttributeError):
                continue
            if not link.startswith('https://') or not title:
                continue
            articles.append({"title": title, "description": desc[:500], "content": desc[:500],
                             "url": link, "publishedAt": stamp.isoformat(),
                             "source": {"name": "Weston High School" if "/high/" in url else ("Weston Public Schools" if "westonschools" in url else "Town of Weston")},
                             "urlToImage": ""})
        return articles
    except (OSError, ElementTree.ParseError, ValueError) as exc:
        print(f"Optional Weston official RSS source unavailable: {exc}", file=sys.stderr)
        return []


def _article_record(article, seen, local=False):
    url = (article.get("url") or "").strip()
    title = (article.get("title") or "").strip()
    desc = (article.get("description") or "").strip()
    parsed = urlparse(url)
    domain = (parsed.hostname or "").lower()
    if (not title or title == "[Removed]" or "[Removed]" in desc
        or parsed.scheme != "https" or not parsed.netloc
        or any(domain == b or domain.endswith("." + b) for b in BLOCKED_DOMAINS)):
        return None
    dedup = re.sub(r"[^a-z0-9]+", "", title.lower())[:85]
    if url in seen or dedup in seen:
        return None
    blob = (title + " " + desc + " " + (article.get("content") or "") + " " + (article.get("source") or {}).get("name", "")).lower()
    if local and not any(x in blob for x in LOCAL_HINTS):
        return None
    # Weston also names towns in other states. Avoid false "Weston, MA" matches.
    if "weston" in blob and not any(x in blob for x in ("massachusetts", "weston, ma", "boston", "middlesex", "waltham", "wellesley", "lexington")) and not domain.endswith(("westonma.gov", "westonschools.org")):
        return None
    published = article.get("publishedAt") or ""
    try:
        stamp = datetime.fromisoformat(published.replace("Z", "+00:00"))
    except ValueError:
        return None
    if stamp > datetime.now(timezone.utc) + timedelta(hours=4):
        return None
    seen.add(url)
    seen.add(dedup)
    score_terms = LOCAL_HIGH_PRIORITY if local else WORLD_FOCUS
    score = 1.0 + sum(2.2 if x == "weston" else 0.65 for x in score_terms if x in blob)
    if local and "weston" in blob:
        score += 7
    score += max(0, 4 - (datetime.now(timezone.utc)-stamp).total_seconds()/86400)
    return ({"title": title, "description": desc[:500], "url": url,
             "source": (article.get("source") or {}).get("name") or domain,
             "published": published, "image": article.get("urlToImage") or ""}, score)


def _collect(queries, minimum, local=False, days=3):
    key = os.environ["NEWS_API_KEY"]
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds").replace("+00:00", "Z")
    results = []
    seen = set()
    per_query = []
    for query in queries:
        query_rows = []
        for article in _fetch_news(query, cutoff, key):
            candidate = _article_record(article, seen, local=local)
            if candidate:
                results.append(candidate)
                query_rows.append(candidate)
        if query_rows:
            per_query.append(max(query_rows, key=lambda pair: pair[1]))
    if local:
        for feed in OFFICIAL_LOCAL_RSS:
            for article in _feed_articles(feed):
                try:
                    posted = datetime.fromisoformat(article['publishedAt'])
                except ValueError:
                    continue
                if posted < datetime.now(timezone.utc) - timedelta(days=days):
                    continue
                candidate = _article_record(article, seen, local=True)
                if candidate:
                    # School/town website sources are directly attributable.
                    rec, score = candidate
                    results.append((rec, score+1.8))
    results.sort(key=lambda pair: pair[1], reverse=True)
    # World headlines should cover several interests rather than 10 stories on one event.
    if not local:
        choices = per_query + [r for r in results if r not in per_query]
    else:
        choices = results
    return [row for row, score in choices[:minimum]]


def discover():
    # Rural government topics may not have a story daily: look back a week locally,
    # but show publication dates. Never fabricate entries to reach a quota.
    local = _collect(LOCAL_QUERIES, 5, local=True, days=7)
    world = _collect(WORLD_QUERIES, 25, local=False, days=3)
    # Match the requested split; avoid publishing a half-filled "15 stories" edition.
    if len(local) < 5 or len(world) < 10:
        raise RuntimeError(f"Only {len(local)} local and {len(world)} world stories found; "
                           "previous edition left unchanged. Check NewsAPI plan, quota or sources.")
    local_urls = {x["url"] for x in local}
    world = [x for x in world if x["url"] not in local_urls]
    if len(world) < 10:
        raise RuntimeError("Duplicate global stories detected; previous edition unchanged")
    return [("Weston / Boston / Massachusetts", local[:5]),
            ("World News / Global", world[:10])]


def summarize(articles):
    key = os.environ["OPENAI_API_KEY"]
    prompt = ("You are an editor. For every indexed news item, write faithful brief bilingual summaries "
              "grounded ONLY in the provided title/description. Do not infer facts, dates or details. "
              "Write concise neutral Chinese title and 1 sentence Chinese summary; "
              "English title and 1 sentence English summary. If description is empty, summarize title only. "
              "Output strictly JSON object with 'items' array; every item has integer 'id' and "
              "strings 'zh_title','zh_summary','en_title','en_summary'. Include every ID once. "
              "Never write personal opinions or pretend to be the website owner.\n" +
              json.dumps(articles, ensure_ascii=False))
    result = get_json("https://api.openai.com/v1/chat/completions",
                      headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
                      payload={"model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                               "temperature": 0.1,
                               "response_format": {"type": "json_object"},
                               "messages": [{"role": "user", "content": prompt}]})
    text = result["choices"][0]["message"]["content"]
    items = json.loads(text)["items"]
    mapping = {int(x["id"]): x for x in items}
    if set(mapping) != {a["id"] for a in articles}:
        raise ValueError("Incomplete AI summary; no files changed")
    for item in mapping.values():
        for field in ("zh_title", "zh_summary", "en_title", "en_summary"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError("Invalid AI result; no files changed")
    return mapping

def safe(text):
    return html.escape(str(text), quote=True)

def render(groups, summaries, date):
    sections = []
    counter = 0
    for section, entries in groups:
        cards = []
        for article in entries:
            counter += 1
            summary = summaries[counter]
            photo = safe_photo(article.get("image", ""))
            if not photo:
                raise RuntimeError(f"Full article {counter} has no verified photo")
            stale = f'<p class="stale">暂无更新 / No New Updates · 最后检查 / Checked: {safe(date)}</p>' if article.get("stale") else ''
            cards.append(f'''<article class="item" id="story-{counter}"><div class="num">{counter:02d}</div>
{stale}<img class="story-photo" src="{safe(photo)}" alt="新闻照片 / Source photo" loading="lazy">
<h3 class="zh-title">{safe(summary['zh_title'])}</h3><p class="en en-title">{safe(summary['en_title'])}</p>
<p class="zh-summary">{safe(summary['zh_summary'])}</p><p class="en-summary">{safe(summary['en_summary'])}</p>
<p class="meta">{safe(article['source'])} · {safe(article['published'][:10])}</p>
<a href="{safe(article['url'])}" target="_blank" rel="noopener noreferrer">原始报道 / Original source ↗</a></article>''')
        sections.append(f'<h2>{safe(section)}</h2><div class="news">{"".join(cards)}</div>')
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{safe(date)} 每日新闻 | Weston Life</title>
<style>
body{{margin:0;background:#faf6ee;color:#30352c;font-family:Georgia,serif;line-height:1.6}}
header{{background:#eee9d9;text-align:center;padding:48px 20px}}
header h1{{font-size:clamp(42px,8vw,80px);color:#425b42;margin:10px 0}}
main{{max-width:1140px;margin:auto;padding:24px}}h2{{font-size:30px;margin:46px 0 18px;border-bottom:1px solid #ccc;padding-bottom:10px}}
.news{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}
.item{{background:white;padding:24px;border:1px solid #e8dfcf;border-radius:12px}}
.item h3{{font-size:21px;margin:4px 0}}.item .story-photo{{display:block;width:100%;max-height:340px;object-fit:cover;border-radius:8px;margin:10px 0}}.item .stale{{font:bold 13px Arial,sans-serif;color:#9d4d28}}.en{{color:#596e53;font-weight:bold}}
.num,.meta{{font:13px Arial,sans-serif;color:#8a6337}}a{{color:#52715e}}footer{{text-align:center;padding:36px}}
@media(max-width:700px){{.news{{grid-template-columns:1fr}}}}
</style></head><body><header><div>Weston Life</div><p>DAILY NEWS · 每日新闻简报</p><h1>{safe(date)}</h1></header>
<main><a href="index.html">← Weston Life 首页 / Back to home</a>
<p>Independent AI-assisted summaries of linked reports. Headlines, dates and source URLs are supplied by NewsAPI; summaries are not independent verification of full articles. Please read original reports for details.</p>
{''.join(sections)}</main><footer>Weston Life · {safe(date)} · News digest</footer></body></html>'''

def safe_photo(url):
    # Use only HTTPS images
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        return ""
    return url


def homepage_panel(groups, summaries, date, filename):
    # Individual HTML cards
    all_items = []
    number = 0
    for section, rows in groups:
        for article in rows:
            number += 1
            summary = summaries[number]
            photo = safe_photo(article.get("image", ""))
            if not photo:
                raise RuntimeError(f"Story {number} has no valid downloaded photo")
            image_html = (f'<img src="{safe(photo)}" alt="新闻来源配图 / Source image" '
                          f'loading="lazy" decoding="async">')
            stale = ('<span class="wl-stale">暂无更新 / No New Updates</span>'
                     f'<small class="wl-checked">最后检查 / Checked: {safe(date)}</small>') if article.get("stale") else ''
            all_items.append(f'''<a class="wl-story" href="{filename}#story-{number}" aria-label="{safe(summary['zh_title'])}">
<span class="wl-index">{number:02d}</span><div class="wl-photo">{image_html}</div>
<div class="wl-copy">{stale}<strong>{safe(summary['zh_title'])}</strong><span class="wl-en">{safe(summary['en_title'])}</span>
<span class="wl-source">{safe(article['source'])} · {safe(article['published'][:10])}</span></div></a>''')
    local = "".join(all_items[:5])
    world = "".join(all_items[5:])
    display_date = safe(date)
    return f'''<!-- WESTON-LIFE-AUTO-START -->
<style>
/* This replaces the fixed daily poster ONLY. Original lifestyle chapters stay intact. */
#today-cover, #daily-news {{display:none !important}}
#wl-auto {{font-family:Georgia,'Times New Roman',serif;background:#fffaf2;color:#283b30;padding:0 14px 28px;max-width:1140px;margin:0 auto 30px;box-sizing:border-box}}
#wl-auto * {{box-sizing:border-box}}
#wl-auto .wl-masthead {{position:relative;text-align:center;background:linear-gradient(135deg,#fff6e3 0%,#f4ecda 48%,#dce9dc 100%);padding:35px 10px 30px;border-bottom:4px solid #c87335;overflow:hidden}}
#wl-auto .wl-masthead:before {{content:'🍁';position:absolute;font-size:90px;left:3%;top:5px;opacity:.55}}
#wl-auto .wl-masthead:after {{content:'🍂';position:absolute;font-size:85px;right:3%;bottom:0;opacity:.5}}
#wl-auto .wl-logo {{font-style:italic;font-size:clamp(42px,8vw,78px);line-height:1.1;color:#315c41}}
#wl-auto .wl-logo em {{color:#b3582b;font-weight:400}}
#wl-auto .wl-kicker {{letter-spacing:.28em;font:13px Arial,sans-serif;margin:6px 0;color:#385943}}
#wl-auto .wl-date {{font:14px Arial,sans-serif;color:#725338;margin-top:9px}}
#wl-auto .wl-tagline {{font:italic 14px Georgia,serif;color:#aa6239;margin:10px 0 0}}
#wl-auto .wl-columns {{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:16px}}
#wl-auto .wl-column-title {{font:bold 15px Arial,sans-serif;color:#945126;background:#faebd9;border-radius:7px;padding:11px;margin:0 0 8px}}
#wl-auto .wl-column-title.world {{color:#315e83;background:#e8f2fa}}
#wl-auto .wl-story {{position:relative;display:grid;grid-template-columns:104px 1fr;gap:12px;text-decoration:none;color:#233b32 !important;background:white;border-bottom:1px solid #e9e1d7;padding:10px 8px 10px 12px;min-height:105px}}
#wl-auto .wl-story:hover {{background:#fff4e4}}
#wl-auto .wl-photo {{height:84px;border-radius:6px;overflow:hidden;background:#ece7dc}}
#wl-auto .wl-photo img {{width:100%;height:100%;object-fit:cover;display:block}}
#wl-auto .wl-stale {{display:block;color:#9d4d28;font:bold 12px Arial,sans-serif;margin:0 0 3px}}
#wl-auto .wl-checked {{display:block;font:10px Arial,sans-serif;color:#80786d;margin-bottom:4px}}
#wl-auto .wl-index {{position:absolute;top:5px;left:2px;background:#df8a39;color:white;border-radius:100%;font:700 13px Arial,sans-serif;padding:6px;z-index:1}}
#wl-auto .wl-copy strong {{display:block;font-size:15px;line-height:1.4}}
#wl-auto .wl-en {{display:block;font-size:12px;line-height:1.4;color:#44644e;margin-top:5px}}
#wl-auto .wl-source {{display:block;font:11px Arial,sans-serif;color:#7a796f;margin-top:6px}}
#wl-auto .wl-editorial {{margin-top:19px;display:flex;gap:18px;align-items:center;background:#fff3e5;border-top:3px solid #dc985a;border-radius:8px;padding:14px}}
#wl-auto .wl-editorial img {{width:105px;height:118px;object-fit:cover;border-radius:8px}}
#wl-auto .wl-editorial h3 {{color:#9d4d28;font-size:23px;margin:0 0 6px}}
#wl-auto .wl-editorial p {{font-size:14px;line-height:1.5;margin:4px 0}}
#wl-auto .wl-cta {{text-align:center;padding:18px 4px 2px;font-size:15px}}
#wl-auto .wl-cta a {{color:#29593d;text-decoration:underline}}
@media(max-width:720px) {{#wl-auto .wl-columns {{grid-template-columns:1fr}} #wl-auto .wl-story {{grid-template-columns:112px 1fr}} #wl-auto .wl-editorial img {{width:80px;height:95px}}}}
</style>
<section id="wl-auto" aria-label="Weston Life 每日新闻">
<header class="wl-masthead"><div class="wl-logo">Weston<em>Life</em></div><div class="wl-kicker">DAILY NEWS · 每日新闻简报</div>
<div class="wl-date">{display_date} · Boston / Massachusetts</div><div class="wl-tagline">A More Informed, Brighter New England</div></header>
<div class="wl-columns"><div><h2 class="wl-column-title">📍 波士顿 · 马萨诸塞州 | BOSTON & MASSACHUSETTS</h2>{local}</div>
<div><h2 class="wl-column-title world">🌐 美国 · 全球 | U.S. & WORLD</h2>{world}</div></div>
<div class="wl-editorial"><img src="assets/coco_portrait_original.jpeg" alt="可可豆子 · Coco Bean" onerror="this.style.display='none'">
<div><h3>可可豆子的今日观点 ♡</h3><p><em>Coco Bean’s View Today</em></p>
<p>观点栏目独立于自动新闻摘要；在本人撰写或确认前，不自动生成署名个人观点。</p>
<p><em>Personal commentary is published separately from AI-assisted news summaries.</em></p></div></div>
<div class="wl-cta"><a href="{filename}">阅读今日完整新闻 / Read the full edition →</a></div>
</section>
<!-- WESTON-LIFE-AUTO-END -->'''


def update_index(index_text, date, filename, panel):
    # Replace the prior generated panel, preserving the full original website.
    index_text = re.sub(r'<!-- WESTON-LIFE-AUTO-START -->.*?<!-- WESTON-LIFE-AUTO-END -->',
                        '', index_text, flags=re.S)
    body = re.search(r'<body\b[^>]*>', index_text, re.I)
    if not body:
        raise RuntimeError("Cannot locate HTML body; leaving existing site unchanged")
    index_text = index_text[:body.end()] + '\n' + panel + '\n' + index_text[body.end():]
    # Add only new-day archive links; do not duplicate existing ones.
    if f'href="{filename}"' not in re.sub(r'<!-- WESTON-LIFE-AUTO-START -->.*?<!-- WESTON-LIFE-AUTO-END -->', '', index_text, flags=re.S):
        match = re.search(r'<section\b[^>]*\bid=["\']news-archive["\'][^>]*>', index_text, re.I)
        if match:
            entry = f'<p class="wl-archive-entry"><a href="{safe(filename)}">{safe(date)} · 每日新闻 / Daily News ↗</a></p>'
            index_text = index_text[:match.end()] + entry + index_text[match.end():]
    return index_text

def main():
    missing = [x for x in ("OPENAI_API_KEY", "NEWS_API_KEY") if not os.environ.get(x)]
    if missing:
        raise RuntimeError("Missing credentials: " + ", ".join(missing))
    today = datetime.now(BOSTON).strftime("%Y-%m-%d")
    filename = f"news-{today}.html"
    index_path = ROOT / "index.html"
    index = index_path.read_text(encoding="utf-8")
    groups = discover()
    articles = []
    for section, entries in groups:
        for article in entries:
            articles.append({"id": len(articles) + 1, "section": section,
                             "title": article["title"], "description": article["description"]})
    summaries = summarize(articles)
    page = render(groups, summaries, today)
    panel = homepage_panel(groups, summaries, today, filename)
    index_updated = update_index(index, today, filename, panel)
    (ROOT / filename).write_text(page, encoding="utf-8")
    if index_updated != index:
        index_path.write_text(index_updated, encoding="utf-8")
    print(f"Published {len(articles)} sourced stories to {filename}; archive updated")

# Keep the existing Chinese/English toggle that was added in October 2026.
_base_homepage = homepage_panel
_base_render = render
LANG_CSS = """
<style>
.wl-langbar{display:flex;justify-content:center;gap:12px;padding:16px 8px;position:relative;z-index:5}
.wl-langbar button{font:bold 20px Arial,sans-serif;padding:12px 22px;min-width:120px;border:2px solid #315c41;border-radius:10px;background:white;color:#315c41;cursor:pointer}
.wl-langbar button.active{background:#315c41;color:white}
html[data-wl-lang="zh"] #wl-auto .wl-en{display:none}
html[data-wl-lang="en"] #wl-auto .wl-copy strong{display:none}
html[data-wl-lang="zh"] .item .en-title,html[data-wl-lang="zh"] .item .en-summary{display:none !important}
html[data-wl-lang="en"] .item .zh-title,html[data-wl-lang="en"] .item .zh-summary{display:none !important}
/* Override legacy p:nth-of-type toggles when a stale-label paragraph is present. */
html[data-wl-lang="zh"] .item .zh-title,html[data-wl-lang="zh"] .item .zh-summary{display:block !important}
html[data-wl-lang="en"] .item .en-title,html[data-wl-lang="en"] .item .en-summary{display:block !important}
html[data-wl-lang="zh"] #wl-school .school-en{display:none}
html[data-wl-lang="en"] #wl-school .school-zh{display:none}
</style>
"""
LANG_BAR = """<nav class="wl-langbar" aria-label="Choose language"><button type="button" data-wl-choice="zh">中文</button><button type="button" data-wl-choice="en">English</button></nav>"""
LANG_SCRIPT = """
<script>(function(){
var lang="zh";try{lang=localStorage.getItem("westonlife-lang")==="en"?"en":"zh"}catch(e){}
function choose(value){lang=value==="en"?"en":"zh";
document.documentElement.dataset.wlLang=lang;
document.documentElement.lang=lang==="en"?"en":"zh-CN";
try{localStorage.setItem("westonlife-lang",lang)}catch(e){}
document.querySelectorAll("[data-wl-choice]").forEach(function(b){b.classList.toggle("active",b.dataset.wlChoice===lang);b.setAttribute("aria-pressed",String(b.dataset.wlChoice===lang))});
var names={".wl-kicker":["每日新闻简报","DAILY NEWS"],".wl-column-title:not(.world)":["📍 Weston · 波士顿 · 马萨诸塞州","📍 WESTON / BOSTON / MASSACHUSETTS"],".wl-column-title.world":["🌐 美国 · 全球","🌐 U.S. & WORLD"],".wl-editorial h3":["可可豆子的今日观点 ♡","Coco Bean's View Today"],".wl-cta a":["阅读今日完整新闻 →","Read Full Edition →"]};
Object.keys(names).forEach(function(sel){var el=document.querySelector("#wl-auto "+sel);if(el)el.textContent=names[sel][lang==="en"?1:0]});
}
document.addEventListener("click",function(e){var b=e.target.closest("[data-wl-choice]");if(b)choose(b.dataset.wlChoice)});
choose(lang);
})();</script>
"""

def homepage_panel(groups, summaries, date, filename):
    panel = _base_homepage(groups, summaries, date, filename)
    panel = panel.replace('<header class="wl-masthead">', '<header class="wl-masthead">' + LANG_BAR, 1)
    return LANG_CSS + panel + LANG_SCRIPT

def render(groups, summaries, date):
    page = _base_render(groups, summaries, date)
    page = page.replace("<body><header>", "<body><header>" + LANG_BAR, 1)
    page = page.replace("</head>", LANG_CSS + "</head>", 1)
    page = page.replace("</body>", LANG_SCRIPT + "</body>", 1)
    return page

# Weston School Watch — placed ABOVE the original Weston travel expert feature.
SCHOOL_2025_URL = "https://www.westonma.gov/DocumentCenter/View/42263/Report-of-the-School-Committee-PDF#page=8"
SCHOOL_2024_URL = "https://www.westonschools.org/wp-content/uploads/2025/02/2024-Report-of-the-Weston-Public-Schools-Final.pdf#page=16"
SCHOOL_PROFILE_URL = "https://www.westonschools.org/high/wp-content/uploads/sites/4/2024/01/WHS-School-Profile-25-26-FINAL.10.15.25.pdf"

SCHOOL_COLLEGES_2025 = [
    ("Northeastern University", 6), ("UMass Amherst", 6), ("Boston College", 5),
    ("Colgate University", 5), ("Cornell University", 5), ("Boston University", 4),
    ("University of Connecticut", 4), ("University of Virginia", 4),
    ("Harvard University", 3), ("Carnegie Mellon University", 3),
    ("Dartmouth College", 3), ("Purdue University", 3), ("Middlebury College", 3),
    ("Massachusetts Institute of Technology", 2), ("New York University", 2),
    ("Columbia University", 1), ("Princeton University", 1), ("Yale University", 1),
    ("University of Pennsylvania", 1),
]
SCHOOL_COLLEGES_2024 = [
    ("Harvard University", 5), ("MIT", 1), ("Stanford University", 3),
    ("Yale University", 2), ("Cornell University", 2), ("Dartmouth College", 3),
    ("Princeton University", 1), ("University of Pennsylvania", 1),
    ("New York University", 2), ("Northeastern University", 12),
    ("Boston College", 6), ("UMass Amherst", 5), ("University of Michigan", 5)
]

def school_cards(rows):
    return "".join(f'<div class="school-row"><span>{safe(name)}</span><strong>{n}</strong></div>' for name,n in rows)


def school_watch_html(date, local_stories=None, school_stories=None):
    # Historical data is labelled 2025/2024 and is NOT falsely presented as new that day.
    # A genuine dated school headline, when present in today's local articles, is displayed above it.
    latest = ""
    for art in (school_stories or []) + (local_stories or []):
        txt = (art.get("title", "") + " " + art.get("description", "")).lower()
        if art.get("official_school") or ("weston" in txt and any(k in txt for k in ("school", "student", "education", "building", "graduation"))):
            latest = f"""<p class="school-latest school-zh">最新学校消息：<a href="{safe(art['url'])}" target="_blank" rel="noopener noreferrer">{safe(art['title'])}</a> <small>({safe(art['published'][:10])})</small></p>
<p class="school-latest school-en">Latest school update: <a href="{safe(art['url'])}" target="_blank" rel="noopener noreferrer">{safe(art['title'])}</a> <small>({safe(art['published'][:10])})</small></p>"""
            break
    return f"""<!-- WESTON-SCHOOL-START -->
<style>
#wl-school{{font-family:Georgia,'Times New Roman',serif;background:#f5f5ed;border:1px solid #d9decd;max-width:1100px;margin:22px auto;padding:22px 26px;border-radius:14px;color:#283b30}}
#wl-school h2{{font-size:clamp(26px,4vw,35px);margin:6px 0 8px;color:#315d44}}
#wl-school .school-kicker{{font:12px Arial,sans-serif;letter-spacing:.2em;color:#8a6e42}}
#wl-school .school-stats{{display:flex;flex-wrap:wrap;gap:14px;margin:16px 0}}
#wl-school .school-stat{{flex:1 1 150px;background:#fff;border-radius:9px;padding:15px;border:1px solid #e0e2d8}}
#wl-school .school-stat strong{{font:700 29px Arial,sans-serif;color:#366a51;display:block}}
#wl-school .school-stat span{{font:13px Arial,sans-serif}}
#wl-school .school-schools{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:5px 24px;margin:14px 0}}
#wl-school .school-row{{display:flex;justify-content:space-between;border-bottom:1px solid #dfe3d8;padding:5px 0;font:13px Arial,sans-serif;gap:10px}}
#wl-school .school-row strong{{font-size:15px;color:#315d44}}
#wl-school a{{text-decoration:underline;color:#315d44}}
#wl-school summary{{cursor:pointer;color:#315d44;margin-top:12px}}
#wl-school .school-notes{{color:#60685b;font:12px/1.6 Arial,sans-serif}}
@media(max-width:600px){{#wl-school{{padding:16px}}#wl-school .school-schools{{grid-template-columns:1fr}}}}
</style>
<section id="wl-school" aria-label="Weston Schools News">
<div class="school-kicker">WESTON LIFE · WESTON SCHOOLS</div>
<h2><span class="school-zh">🎓 Weston校园动态</span><span class="school-en">🎓 Weston School Watch</span></h2>
{latest}
<h3 class="school-zh" style="margin:8px 0">Weston高中升学榜：2025届毕业生去哪了？</h3>
<h3 class="school-en" style="margin:8px 0">Where Did Weston High School's Class of 2025 Go to College?</h3>
<p class="school-zh">据Weston镇2026年学校委员会报告，2025届毕业生中约97%继续升学，就读于96所高等教育机构。以下为部分院校的实际入读人数，非录取通知书数量。</p>
<p class="school-en">According to the Town's 2026 School Committee report, about 97% of the Class of 2025 continued their education at 96 institutions. Counts below are matriculations, not offers of admission.</p>
<div class="school-stats"><div class="school-stat"><strong>169</strong><span class="school-zh">2026镇报告中的2025届毕业人数</span><span class="school-en">Class of 2025, town-report count</span></div>
<div class="school-stat"><strong>97%</strong><span class="school-zh">继续接受教育</span><span class="school-en">Continued education</span></div>
<div class="school-stat"><strong>96</strong><span class="school-zh">入读院校数量</span><span class="school-en">Different institutions</span></div></div>
<div class="school-schools">{school_cards(SCHOOL_COLLEGES_2025)}</div>
<p class="school-zh"><a href="{safe(SCHOOL_2025_URL)}" target="_blank" rel="noopener noreferrer">查看2025届完整96所院校去向（官方PDF，第29页） ↗</a></p>
<p class="school-en"><a href="{safe(SCHOOL_2025_URL)}" target="_blank" rel="noopener noreferrer">View complete 2025 college list (Town report, p. 29) ↗</a></p>
<details><summary><span class="school-zh">查看2024届大学去向对比（13所）</span><span class="school-en">Compare Class of 2024 destinations (13 colleges)</span></summary>
<div class="school-schools">{school_cards(SCHOOL_COLLEGES_2024)}</div>
<p><a href="{safe(SCHOOL_2024_URL)}" target="_blank" rel="noopener noreferrer">2024 official report / 2024届官方报告 ↗</a></p></details>
<p class="school-notes school-zh">资料年份：2025届去向，公布于2026年。注意：2025–26官方高中概况另列170名毕业生；上文采用同一份2026年镇报告的169人及院校明细，不混用口径。学校并非每天公布新升学数据。</p>
<p class="school-notes school-en">The 2025 cohort was reported in the 2026 Town Report. A separate WHS profile lists 170 graduates; this feature consistently uses the town report's count of 169. Admissions outcomes do not change daily.</p>
</section>
<!-- WESTON-SCHOOL-END -->"""

_base_update_index = update_index

def update_index(index_text, date, filename, panel):
    # Remove previous school-watch block so each day's refresh remains idempotent.
    index_text = re.sub(r'<!-- WESTON-SCHOOL-START -->.*?<!-- WESTON-SCHOOL-END -->', '', index_text, flags=re.S)
    index_text = _base_update_index(index_text, date, filename, panel)
    travel = re.search(r'<div[^>]*>\s*<p[^>]*>\s*WESTON LIFE\s*·\s*COMMUNITY STORIES\s*</p>', index_text, flags=re.I)
    if not travel:
        raise RuntimeError("Original Weston travel section not found; website left unchanged")
    school = school_watch_html(date, getattr(update_index, '_local_stories', []), getattr(update_index, '_school_stories', []))
    return index_text[:travel.start()] + school + '\n' + index_text[travel.start():]

# Build the school-note as part of the same daily run without changing the rest of the pipeline.
_original_discover = discover

def discover():
    groups = _original_discover()
    update_index._local_stories = groups[0][1]
    school_stories = []
    for a in _feed_articles("https://www.westonschools.org/feed/"):
        try:
            stamp = datetime.fromisoformat(a["publishedAt"])
        except ValueError:
            continue
        if stamp >= datetime.now(timezone.utc) - timedelta(days=21):
            school_stories.append({"title":a["title"], "description":a["description"],
                                   "url":a["url"], "published":a["publishedAt"], "official_school": True})
    school_stories.sort(key=lambda a:a["published"], reverse=True)
    update_index._school_stories = school_stories
    return groups


# ===== Weston Life 2026-10-22: strict editorial slots and photo safety =====
# Each story must have a real, independently downloadable article photo.
# Never use a logo, blank image, or a story from a different section to fill a slot.
from hashlib import sha256
from html.parser import HTMLParser
from urllib.parse import urljoin

PHOTO_DIR = ROOT / "assets" / "news"
STATE_PATH = ROOT / "news_state.json"

# Five local positions + ten international/U.S. positions; never re-rank between them.
NEWS_SLOTS = [
    {"name": "Weston 本地新闻 / Weston Local", "local": True, "days": 7,
     "query": '("Weston, MA" OR "Weston Massachusetts" OR "Weston Mass.")',
     "must": (("weston",),)},
    {"name": "Weston High School 校园动态 / WHS", "local": True, "days": 14,
     "query": '("Weston High School" OR "WHS Weston" OR "Weston Public Schools")',
     "must": (("weston",), ("high school", "whs", "/high/", "class of 202", "secondary school", "high school students"))},
    {"name": "Weston 镇政府 / Town Government", "local": True, "days": 14,
     "query": '("Weston" AND "Massachusetts" AND ("Select Board" OR "Town" OR "planning" OR "meeting"))',
     "must": (("weston",), ("town", "board", "government", "municipal", "planning", "meeting", "zoning", "council"))},
    {"name": "波士顿城市动态 / Boston City", "local": True, "days": 7,
     "query": '("Boston" AND ("city hall" OR "mayor" OR "festival" OR "events" OR "community"))',
     "must": (("boston",), ("mayor", "city", "festival", "event", "government", "exhibition", "community", "museum"))},
    {"name": "麻州活动 / Massachusetts Events", "local": True, "days": 7,
     "query": '("Massachusetts" AND ("event" OR "festival" OR "exhibition" OR "weekend"))',
     "must": (("massachusetts", "mass.", "ma ", "new england"), ("event", "festival", "exhibition", "concert", "museum", "fair", "weekend", "activity", "activities"))},
    {"name": "美国与伊朗 / U.S.–Iran", "local": False, "days": 5,
     "query": '("Iran" AND ("United States" OR "US" OR "Trump" OR "Washington"))',
     "must": (("iran", "tehran", "iranian"), ("united states", "u.s.", " u.s ", "us ", "american", "washington", "trump", "white house", "pentagon"))},
    {"name": "俄乌战争 / Russia–Ukraine", "local": False, "days": 5,
     "query": '("Ukraine" AND ("Russia" OR "Putin" OR "war"))',
     "must": (("ukraine", "ukrainian", "kyiv"), ("russia", "russian", "putin", "kremlin", "war", "drone", "strike"))},
    {"name": "中国重要新闻 / China", "local": False, "days": 5,
     "query": '("China" AND ("economy" OR "policy" OR "technology" OR "government"))',
     "must": (("china", "chinese", "beijing", "shanghai"),)},
    {"name": "美国股市及经济 / U.S. Markets", "local": False, "days": 5,
     "query": '("Wall Street" OR "Nasdaq" OR "S&P 500" OR "Treasury yields" OR "Federal Reserve")',
     "must": (("stocks", "stock market", "wall street", "nasdaq", "s&p", "qqq", "spy", "treasury", "bond yield", "federal reserve", "interest rate", "fed ", "dow jones"),)},
    {"name": "重点股票与公司 / Major Companies", "local": False, "days": 5,
     "query": '("Nvidia" OR "Microsoft" OR "Alphabet" OR "Broadcom" OR "Tesla" OR "Apple")',
     "must": (("nvidia", "microsoft", "alphabet", "google", "broadcom", "tesla", "apple", "amazon", "meta platforms", "amd", "tsmc"),)},
    {"name": "AI技术突破 / AI Breakthroughs", "local": False, "days": 5,
     "query": '("artificial intelligence" AND ("breakthrough" OR "research" OR "robotics" OR "model"))',
     "must": (("artificial intelligence", "ai ", " ai", "robotics", "machine learning", "neural", "llm"), ("breakthrough", "research", "discovery", "scientists", "robot", "model", "innovation", "new technology"))},
    {"name": "AI科技企业 / AI Companies", "local": False, "days": 5,
     "query": '("OpenAI" OR "Anthropic" OR "Google DeepMind" OR "Meta AI" OR "Microsoft AI")',
     "must": (("openai", "anthropic", "deepmind", "meta ai", "microsoft ai", "chatgpt", "gemini", "claude"),)},
    {"name": "美国重要新闻 / U.S. News", "local": False, "days": 5,
     "query": '("United States" AND ("Congress" OR "White House" OR "Supreme Court" OR "federal"))',
     "must": (("united states", "u.s.", "white house", "congress", "supreme court", "american", "federal government"),)},
    {"name": "美国大学与升学 / Higher Education", "local": False, "days": 14,
     "query": '("university admissions" OR "college admissions" OR "Harvard University" OR "MIT" OR "SAT exam")',
     "must": (("university", "college", "admissions", "campus", "harvard", "mit", "students", "scholarships"),)},
    {"name": "房地产市场 / Real Estate", "local": False, "days": 5,
     "query": '("housing market" OR "mortgage rates" OR "home sales" OR "real estate market")',
     "must": (("housing", "real estate", "mortgage", "home prices", "home sales", "property market"),)},
]

class _OGImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() != "meta":
            return
        d = dict((k.lower(), v) for k, v in attrs if k)
        if (d.get("property", "").lower() in ("og:image", "og:image:url") or
                d.get("name", "").lower() in ("twitter:image", "twitter:image:src")):
            if d.get("content"):
                self.images.append(d["content"])


def _image_from_article_page(url):
    """Only use images expressly associated with this article by the publisher."""
    try:
        parsed = urlparse(url)
        if parsed.scheme != "https":
            return []
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 WestonLifeNews/1.0"})
        with urlopen(req, timeout=9) as res:
            if "html" not in res.headers.get("Content-Type", "").lower():
                return []
            page = res.read(200_000).decode("utf-8", errors="ignore")
        p = _OGImageParser()
        p.feed(page)
        return [urljoin(url, candidate) for candidate in p.images]
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"No article photo metadata: {url}: {exc}", file=sys.stderr)
        return []


def _photo_extension(blob):
    if blob.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if blob.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if blob[:4] == b"RIFF" and blob[8:12] == b"WEBP":
        return ".webp"
    if blob[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    return ""


def _save_real_photo(url):
    """Cache publisher's actual raster image within the site; reject broken URLs."""
    if not url or urlparse(url).scheme != "https":
        return ""
    basename = urlparse(url).path.lower().rsplit("/", 1)[-1]
    if any(term in basename for term in ("placeholder", "favicon", "site-logo", "no-image", "default-image", "brand-logo", "spacer")):
        return ""
    digest = sha256(url.encode("utf-8")).hexdigest()[:24]
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    for ext in (".jpg", ".png", ".webp", ".gif"):
        saved = PHOTO_DIR / (digest + ext)
        if saved.exists() and saved.stat().st_size > 5000:
            return saved.relative_to(ROOT).as_posix()
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 WestonLifeNews/1.0",
                                    "Accept": "image/avif,image/webp,image/png,image/jpeg,image/gif,*/*;q=0.4"})
        with urlopen(req, timeout=10) as res:
            content_type = res.headers.get("Content-Type", "").lower()
            if content_type and not content_type.startswith("image/") and "octet-stream" not in content_type:
                return ""
            data = res.read(4_000_001)
        ext = _photo_extension(data)
        if not ext or len(data) < 5000 or len(data) > 4_000_000:
            return ""
        target = PHOTO_DIR / (digest + ext)
        target.write_bytes(data)
        return target.relative_to(ROOT).as_posix()
    except (OSError, ValueError) as exc:
        print(f"Photo unavailable {url}: {exc}", file=sys.stderr)
        return ""


def _complete_photo(article):
    """The story itself must have its own image; no unrelated substitute."""
    img = article.get("image", "")
    if img.startswith("assets/news/"):
        path = ROOT / img
        if path.is_file() and path.stat().st_size > 5000 and _photo_extension(path.read_bytes()[:16]):
            return img
    # New material: from NewsAPI article preview, then publisher's own og:image.
    original = img if img.startswith("https://") else ""
    candidates = ([original] if original else []) + _image_from_article_page(article["url"])
    for u in dict.fromkeys(candidates):
        photo = _save_real_photo(u)
        if photo:
            return photo
    return ""


def _matching(slot, art):
    """Match headline/description, not search result URL keywords from unrelated stories."""
    source = str(art.get("source") or "")
    title = str(art.get("title") or "")
    description = str(art.get("description") or "")
    host = (urlparse(art.get("url") or "").hostname or "").lower()
    official = host == "westonma.gov" or host.endswith(".westonma.gov") or \
               host == "westonschools.org" or host.endswith(".westonschools.org")
    blob = (title + " " + description + " " + source).lower()
    if official:
        blob += " weston massachusetts "
        if "/high/" in art.get("url", ""):
            blob += " high school whs "
    if slot["local"] and not any(k in blob for k in LOCAL_HINTS):
        return False
    if slot is NEWS_SLOTS[1]:
        # Weston High School vs other 'Weston High School' names outside MA.
        if not official and not any(k in blob for k in ("massachusetts", "weston, ma", "boston", "weston public schools")):
            return False
    return all(any(word in blob for word in alternatives) for alternatives in slot["must"])


def _official_slot_entries(i):
    urls = []
    if i == 1:
        urls = ["https://www.westonschools.org/high/feed/", "https://www.westonschools.org/feed/"]
    elif i == 2:
        urls = ["https://www.westonma.gov/RSSFeed.aspx?CID=Latest-Town-News-1&ModID=1"]
    elif i == 0:
        urls = ["https://www.westonschools.org/feed/",
                "https://www.westonma.gov/RSSFeed.aspx?CID=Latest-Town-News-1&ModID=1"]
    if not urls:
        return []
    items = []
    for url in urls:
        for raw in _feed_articles(url):
            # Official school/municipal feeds may have titles such as "Autumn Concert".
            # The source domain establishes the Weston, MA jurisdiction; no invented article facts.
            record = dict(raw)
            record["description"] = ((raw.get("description") or "") +
                                     " (Official Weston, Massachusetts notice)").strip()
            rec = _article_record(record, set(), local=True)
            if rec:
                item = rec[0]
                items.append(item)
    return items


def _load_previous():
    if not STATE_PATH.is_file():
        return {}
    try:
        obj = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return obj.get("slots", {}) if isinstance(obj.get("slots"), dict) else {}
    except (OSError, ValueError, AttributeError):
        return {}


def _newer(a, old):
    """Only replace an existing article with a different, demonstrably newer report."""
    if not old:
        return True
    if a["url"] == old.get("url"):
        return False
    try:
        a_time = datetime.fromisoformat(a["published"].replace("Z", "+00:00"))
        old_time = datetime.fromisoformat(old["published"].replace("Z", "+00:00"))
        return a_time > old_time
    except (ValueError, KeyError, TypeError):
        return False


def _get_slot_candidate(slot_index, slot, old, used):
    key = os.environ["NEWS_API_KEY"]
    cutoff = (datetime.now(timezone.utc) - timedelta(days=slot["days"])).isoformat(timespec="seconds").replace("+00:00", "Z")
    raw_items = _fetch_news(slot["query"], cutoff, key, page_size=45)
    pool = _official_slot_entries(slot_index) if slot["local"] else []
    checked = set()
    for raw in raw_items:
        record = _article_record(raw, checked, local=slot["local"])
        if record:
            pool.append(record[0])
    # Prefer more recent updates from original sources. Official posts win ties.
    pool.sort(key=lambda a: a["published"], reverse=True)
    for art in pool[:22]:
        if art["url"] in used or not _matching(slot, art) or not _newer(art, old):
            continue
        if slot_index == 0:
            clue = (art.get("title", "") + " " + art.get("description", "")).lower()
            # Specific school/town stories should be reserved for #2/#3 when applicable.
            if any(t in clue for t in ("high school", "school committee", "select board", "planning board")):
                continue
        try:
            when = datetime.fromisoformat(art["published"].replace("Z", "+00:00"))
            if when < datetime.now(timezone.utc) - timedelta(days=slot["days"]):
                continue
        except ValueError:
            continue
        photo = _complete_photo(art)
        if photo:
            art["image"] = photo
            art["stale"] = False
            return art
    return None


def discover():
    """Fill 15 fixed editorial positions. Reserve school and town sources first."""
    old_state = _load_previous()
    used, results = set(), [None] * len(NEWS_SLOTS)
    # The Weston catch-all slot must not consume school/town news first.
    priority = [1, 2, 0, 3, 4] + list(range(5, len(NEWS_SLOTS)))
    for i in priority:
        slot = NEWS_SLOTS[i]
        number = str(i + 1)
        prior = old_state.get(number) or {}
        old = prior.get("article") if prior.get("topic") == slot["name"] else None
        candidate = _get_slot_candidate(i, slot, old, used)
        if not candidate and old and old.get("url") not in used and _matching(slot, old):
            photo = _complete_photo(old)
            if photo:
                candidate = dict(old, image=photo, stale=True)
        if not candidate:
            raise RuntimeError(
                f"Slot {i+1} [{slot['name']}] has no relevant, pictured report "
                "and no saved report. Keeping old website; NEVER substituting another topic. "
                "First run may require an existing on-topic source with a photograph.")
        candidate["topic"] = slot["name"]
        used.add(candidate["url"])
        results[i] = candidate
        print(f"Slot {i+1:02d}: {'PRESERVED / NO UPDATE' if candidate.get('stale') else 'NEW'}: "
              f"{candidate['title'][:80]}")
    update_index._local_stories = results[:5]
    update_index._school_stories = [results[1]]
    return [("Weston / Boston / Massachusetts", results[:5]),
            ("World News / Global", results[5:])]


_old_summarize_for_photos = summarize

def summarize(articles):
    saved = _load_previous()
    fresh = []
    result = {}
    for article in articles:
        number = article["id"]
        prior = saved.get(str(number)) or {}
        # The summary of an unchanged article must remain unchanged too.
        if article.get("stale") and prior.get("summary"):
            result[number] = prior["summary"]
        else:
            fresh.append(article)
    if fresh:
        result.update(_old_summarize_for_photos(fresh))
    if set(result) != {a["id"] for a in articles}:
        raise RuntimeError("Incomplete translated content; website unchanged")
    return result


def safe_photo(url):
    if not isinstance(url, str):
        return ""
    if url.startswith("assets/news/"):
        path = ROOT / url
        if path.is_file() and path.stat().st_size > 5000:
            return url
    return ""


def main():
    missing = [x for x in ("OPENAI_API_KEY", "NEWS_API_KEY") if not os.environ.get(x)]
    if missing:
        raise RuntimeError("Missing credentials: " + ", ".join(missing))
    today = datetime.now(BOSTON).strftime("%Y-%m-%d")
    filename = f"news-{today}.html"
    index_path = ROOT / "index.html"
    index = index_path.read_text(encoding="utf-8")
    groups = discover()
    rows = [x for _, a in groups for x in a]
    if len(rows) != 15 or any(not safe_photo(a.get("image", "")) for a in rows):
        raise RuntimeError("Exactly 15 real downloaded photos required; no HTML files changed")
    articles = [{"id": i, "section": NEWS_SLOTS[i-1]["name"],
                 "title": a["title"], "description": a["description"], "stale": a.get("stale")}
                for i, a in enumerate(rows, 1)]
    summaries = summarize(articles)
    page = render(groups, summaries, today)
    panel = homepage_panel(groups, summaries, today, filename)
    index_updated = update_index(index, today, filename, panel)
    # Compute all content before changing any pages.
    state = {"checked_at": today, "slots": {str(i): {"topic": NEWS_SLOTS[i-1]["name"],
                "article": {k: v for k,v in a.items() if k != "stale"},
                "summary": summaries[i]} for i, a in enumerate(rows, 1)}}
    (ROOT / filename).write_text(page, encoding="utf-8")
    if index_updated != index:
        index_path.write_text(index_updated, encoding="utf-8")
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Published exactly 15 pictured stories to {filename}; "
          f"{sum(not a.get('stale') for a in rows)} new, "
          f"{sum(bool(a.get('stale')) for a in rows)} preserved with no-update labels")


def offline_self_check():
    assert len(NEWS_SLOTS) == 15
    assert sum(s["local"] for s in NEWS_SLOTS) == 5
    sample = {"title": "Weston High School hosts community event", "description": "Weston, Massachusetts public schools notice", "url": "https://www.westonschools.org/high/news/", "source": "Weston High School"}
    assert _matching(NEWS_SLOTS[1], sample)
    assert not _matching(NEWS_SLOTS[6], sample)
    assert not _matching(NEWS_SLOTS[1], {**sample, "title": "Weston, Florida school team", "description": "Florida district", "url":"https://example.com/school", "source":"Florida"})
    assert _newer({"url":"https://a.com", "published":"2026-10-22T13:00:00Z"},
                  {"url":"https://b.com", "published":"2026-10-22T12:00:00+00:00"})
    assert not _newer({"url":"https://a.com", "published":"2026-10-22T11:00:00Z"},
                      {"url":"https://b.com", "published":"2026-10-22T12:00:00+00:00"})
    print("PASS: 15 fixed slots, local first, topic screening, chronological updates")


if __name__ == "__main__":
    try:
        if "--check" in sys.argv:
            offline_self_check()
            sys.exit(0)
        main()
    except (OSError, HTTPError, URLError, KeyError, ValueError, RuntimeError) as exc:
        print(f"PUBLISHING FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
