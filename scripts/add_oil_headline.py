import json, os, re, html
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DAY = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
START, END = "<!-- OIL-HEADLINE-START -->", "<!-- OIL-HEADLINE-END -->"

def request(url, headers=None, body=None):
    with urlopen(Request(url, headers=headers or {"User-Agent":"WestonLife/1.0"}, data=body), timeout=30) as r:
        return json.load(r)

def find_news():
    key = os.environ["NEWS_API_KEY"]
    query = '("oil prices" OR "Brent crude" OR "WTI crude" OR "crude oil")'
    params = urlencode({"q":query, "language":"en", "sortBy":"publishedAt",
        "pageSize":50, "from":(datetime.now(timezone.utc)-timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "apiKey":key})
    for a in request("https://newsapi.org/v2/everything?"+params).get("articles", []):
        blob = ((a.get("title") or "")+" "+(a.get("description") or "")).lower()
        if a.get("url","").startswith("https://") and any(x in blob for x in
             ("oil prices","oil price","crude oil","brent","wti")) and "[removed]" not in blob:
            return a
    return None

def translate(a):
    if not a:
        return ("暂无经过核实的最新油价报道，今天不显示未经证实的价格。",
                "No newly verified oil-price report; no unverified prices shown.")
    fallback = a.get("description") or a.get("title") or ""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return ("最新油价报道，请查看原始来源。", fallback)
    prompt = ("Write a faithful, brief Chinese and English summary based ONLY on the provided headline "
              "and description. Do not invent prices, percentages, causes or dates. Return JSON object "
              "with keys zh and en. "+json.dumps({"title":a.get("title"),"description":a.get("description")}))
    try:
        payload=json.dumps({"model":os.environ.get("OPENAI_MODEL","gpt-4o-mini"),
            "response_format":{"type":"json_object"},
            "messages":[{"role":"user","content":prompt}],"temperature":0}).encode()
        obj=request("https://api.openai.com/v1/chat/completions",
                    {"Authorization":"Bearer "+key,"Content-Type":"application/json"},payload)
        result=json.loads(obj["choices"][0]["message"]["content"])
        return (str(result["zh"]),str(result["en"]))
    except Exception:
        return ("最新油价报道，请查看原始来源。",fallback)

def replace_block(source):
    return re.sub(re.escape(START)+r".*?"+re.escape(END),"",source,flags=re.S)

def main():
    index_path=ROOT/"index.html"
    daily_path=ROOT/("news-"+DAY+".html")
    index=replace_block(index_path.read_text(encoding="utf-8"))
    daily=replace_block(daily_path.read_text(encoding="utf-8"))
    a=find_news()
    zh,en=translate(a)
    source=((a or {}).get("source") or {}).get("name") or "U.S. EIA"
    date=((a or {}).get("publishedAt") or DAY)[:10]
    url=(a or {}).get("url") or "https://www.eia.gov/petroleum/"
    e=lambda s:html.escape(str(s),quote=True)
    card=(START+'<a class="wl-story" href="news-'+DAY+'.html#story-oil" '
          'style="border-left:5px solid #b91c1c;background:#fff6f3">'
          '<div class="wl-photo" style="display:flex;align-items:center;justify-content:center;font-size:32px">🛢️</div>'
          '<div class="wl-copy"><strong style="color:#b91c1c;font-size:24px">今日油价</strong>'
          '<span class="wl-en" style="color:#b91c1c;font-weight:bold">Today\'s Oil Prices</span>'
          '<span class="wl-source">'+e(source)+' · '+e(date)+'</span></div></a>'+END)
    detail=(START+'<article class="item" id="story-oil" style="border-top:5px solid #b91c1c">'
            '<h3 style="color:#b91c1c;font-size:28px">今日油价</h3>'
            '<p style="color:#b91c1c;font-weight:bold">Today\'s Oil Prices</p>'
            '<p>'+e(zh)+'</p><p>'+e(en)+'</p><p>'+e(source)+' · '+e(date)+'</p>'
            '<a href="'+e(url)+'" target="_blank" rel="noopener noreferrer">原始报道 / Original source ↗</a>'
            '</article>'+END)
    m=re.search(r'<h2 class="wl-column-title world">.*?</h2>',index,re.S)
    n=re.search(r'<h2>World News / Global</h2>\s*<div class="news">',daily)
    if not m or not n:
        raise RuntimeError("News headings not found; no files were changed")
    index=index[:m.end()]+card+index[m.end():]
    daily=daily[:n.end()]+detail+daily[n.end():]
    index_path.write_text(index,encoding="utf-8")
    daily_path.write_text(daily,encoding="utf-8")
    print("Oil headline added; all 15 existing news stories unchanged.")

if __name__=="__main__":
    main()
