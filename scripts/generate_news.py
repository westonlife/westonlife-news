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

ROOT = Path(__file__).resolve().parent.parent
BOSTON = ZoneInfo("America/New_York")
TOPICS = [
    ("Boston / Massachusetts", 'Boston OR Massachusetts OR "New England"', 5),
    ("United States / World", 'US economy OR technology OR oil OR Ukraine OR Middle East', 5),
]

def get_json(url, headers=None, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers=headers or {}, method="POST" if data else "GET")
    with urlopen(request, timeout=35) as response:
        return json.loads(response.read().decode("utf-8"))

def discover():
    key = os.environ["NEWS_API_KEY"]
    cutoff = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(timespec="seconds").replace("+00:00", "Z")
    groups = []
    seen = set()
    for section, terms, limit in TOPICS:
        params = urlencode({"q": terms, "language": "en", "sortBy": "publishedAt", "pageSize": 50,
                            "from": cutoff, "apiKey": key})
        result = get_json("https://newsapi.org/v2/everything?" + params)
        if result.get("status") != "ok":
            raise RuntimeError("NewsAPI request failed: " + str(result.get("message", "unknown")))
        selected = []
        for article in result.get("articles", []):
            url = article.get("url", "")
            title = article.get("title", "")
            parsed = urlparse(url)
            if (not title or title == "[Removed]" or not parsed.scheme == "https" or not parsed.netloc
                    or url in seen or "[Removed]" in article.get("description", "")):
                continue
            published = article.get("publishedAt", "")
            try:
                timestamp = datetime.fromisoformat(published.replace("Z", "+00:00"))
                if timestamp < datetime.now(timezone.utc) - timedelta(days=3):
                    continue
            except ValueError:
                continue
            seen.add(url)
            selected.append({"title": title, "description": (article.get("description") or "")[:500],
                             "url": url, "source": (article.get("source") or {}).get("name", ""),
                             "published": published, "image": article.get("urlToImage") or ""})
            if len(selected) >= limit:
                break
        groups.append((section, selected))
    if sum(len(rows) for _, rows in groups) < 4:
        raise RuntimeError("Not enough recent sourced articles; keeping previous edition unchanged")
    return groups

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
            cards.append(f'''<article class="item" id="story-{counter}"><div class="num">{counter:02d}</div>
<h3>{safe(summary['zh_title'])}</h3><p class="en">{safe(summary['en_title'])}</p>
<p>{safe(summary['zh_summary'])}</p><p>{safe(summary['en_summary'])}</p>
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
.item h3{{font-size:21px;margin:4px 0}}.en{{color:#596e53;font-weight:bold}}
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
            image_html = (f'<img src="{safe(photo)}" alt="新闻来源配图 / Source image" '
                          f'loading="lazy" referrerpolicy="no-referrer" '
                          f'onerror="this.style.display=\'none\'">') if photo else '<div class="wl-img-fallback">Weston Life</div>'
            all_items.append(f'''<a class="wl-story" href="{filename}#story-{number}" aria-label="{safe(summary['zh_title'])}">
<span class="wl-index">{number:02d}</span><div class="wl-photo">{image_html}</div>
<div class="wl-copy"><strong>{safe(summary['zh_title'])}</strong><span class="wl-en">{safe(summary['en_title'])}</span>
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
#wl-auto .wl-img-fallback {{height:100%;display:flex;justify-content:center;align-items:center;background:#d9e7dc;color:#4f7558;font-style:italic;text-align:center;font-size:13px}}
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

if __name__ == "__main__":
    try:
        main()
    except (OSError, HTTPError, URLError, KeyError, ValueError, RuntimeError) as exc:
        print(f"PUBLISHING FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
