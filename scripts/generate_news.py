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
                             "published": published})
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
            cards.append(f'''<article class="item"><div class="num">{counter:02d}</div>
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

def update_index(index_text, date, filename):
    new_entry = (f'<a href="{filename}" style="display:block;padding:16px 0">'
                 f'{date} · 今日新闻 / Daily News ↗</a>')
    if f'href="{filename}"' in index_text:
        return index_text
    match = re.search(r'<section\b[^>]*\bid=["\']news-archive["\'][^>]*>', index_text, re.I)
    if not match:
        raise RuntimeError("Cannot find news-archive section in index.html; no files changed")
    closing = index_text.find("</section>", match.end())
    if closing < 0:
        raise RuntimeError("Unclosed news archive section; no files changed")
    return index_text[:closing] + new_entry + index_text[closing:]

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
    index_updated = update_index(index, today, filename)
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
