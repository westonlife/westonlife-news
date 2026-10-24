"""Weston Life: independent Massachusetts real-estate desk, inserted BEFORE school.
Source: Redfin City/State Market Tracker + publisher RSS + Niche 2027 ranks.
No guessed sold figures, bedroom popularity, or substituted list prices.
"""
from __future__ import annotations
import csv, gzip, html, io, re, sys, os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from xml.etree import ElementTree
from email.utils import parsedate_to_datetime

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
DATA_HOME = "https://www.redfin.com/news/data-center/downloads/"
BASE = "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/"
CITY_URL = BASE + "city_market_tracker.tsv000.gz"
STATE_URL = BASE + "state_market_tracker.tsv000.gz"
TARGET = ["Weston", "Wellesley", "Lexington", "Newton", "Brookline", "Needham", "Boston", "Cambridge",
          "Belmont", "Winchester", "Wayland", "Natick", "Concord", "Westwood", "Dover", "Sherborn",
          "Waltham", "Arlington", "Medfield", "Bedford", "Hopkinton", "Milton", "Shrewsbury", "Framingham"]
CITY_SET = set(TARGET)
RANKS = [
    (1, "Dover–Sherborn"), (2, "Needham"), (3, "Brookline"), (4, "Lexington"),
    (5, "Hopkinton"), (6, "Weston"), (7, "Belmont"), (8, "Westborough"),
    (9, "Winchester"), (10, "Wayland"), (11, "Newton"), (17, "Wellesley")
]
NICHESOURCE = "https://www.boston.com/news/education/2026/10/23/best-school-districts-massachusetts-niche/"
MAR_SOURCE = "https://bostonagentmagazine.com/2026/10/14/mar-september-data-2026/"
REDFIN_WESTON = "https://www.redfin.com/city/29572/MA/Weston/housing-market"
FEEDS = [
    ("Boston Agent Magazine", "https://bostonagentmagazine.com/feed/"),
    ("Banker & Tradesman", "https://bankerandtradesman.com/feed/"),
    ("Boston Real Estate Times", "https://bostonrealestatetimes.com/feed/"),
]
# These are September 2026 SOURCE-DATED fallback highlights, not claimed as current.
FALLBACK_REPORTS = [
    ("2026年9月麻州独栋成交量同比增加4.8%，公寓减少6.4%", "MA September 2026: single-family sales up 4.8%, condo sales down 6.4%", MAR_SOURCE, "Boston Agent Magazine", "2026-10-14"),
    ("Weston 2026年9月成交39套，成交价中位数约$227.4万", "Weston: 39 homes sold in September 2026; median sale price ~$2.274M", REDFIN_WESTON, "Redfin", "2026-09"),
]


def esc(x): return html.escape(str(x), quote=True)

def nfloat(x):
    try: return float(str(x).replace(",", "")) if str(x).strip().upper() not in ("NA", "", "NONE", "NULL") else None
    except (ValueError, TypeError): return None

def amt(x):
    v = nfloat(x)
    if v is None: return "—"
    if v >= 1_000_000: return f"${v/1_000_000:,.2f}M"
    if v >= 1_000: return f"${v/1_000:,.0f}K"
    return f"${v:,.0f}"

def dollars(x):
    v = nfloat(x)
    return f"${v:,.0f}" if v is not None else "—"

def integer(x):
    v = nfloat(x)
    return f"{round(v):,}" if v is not None else "—"

def cols(row):
    return {k.lower().replace(' ', '_').strip(): v for k,v in row.items() if k}

def row_kind(row):
    raw = str(row.get('property_type') or '').lower()
    if 'all residential' in raw: return 'all'
    if 'single family' in raw: return 'single'
    if 'condo' in raw or 'co-op' in raw: return 'condo'
    if 'townhouse' in raw: return 'townhouse'
    if 'multi-family' in raw: return 'multifamily'
    return ''

def city_name(row):
    value = (row.get('city') or row.get('region') or row.get('region_name') or '').strip()
    # region value may be 'Weston, MA' or a Redfin label.
    return value.split(',')[0].strip()

def current_month(row):
    p = str(row.get('period_duration', '')).strip()
    return not p or p == '1' or p.lower() == 'month'

def fetch_table(url, wanted):
    """Scan compressed monthly TSV without materializing all U.S. records."""
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 WestonLife/1.0 public-data-aggregator', 'Accept': 'application/gzip'})
    output = {}
    with urlopen(req, timeout=150) as res:
        with gzip.GzipFile(fileobj=res) as decompressed:
            reader = csv.DictReader(io.TextIOWrapper(decompressed, encoding='utf-8', errors='replace'), delimiter='\t')
            for raw in reader:
                a = cols(raw)
                if (a.get('state_code') or '').upper() != 'MA' and (a.get('state') or '').lower() not in ('massachusetts', 'ma'):
                    continue
                if not current_month(a): continue
                day = (a.get('period_end') or '')[:10]
                if not re.fullmatch(r'20\d{2}-\d{2}-\d{2}', day): continue
                if day > datetime.now(timezone.utc).date().isoformat(): continue
                kind = row_kind(a)
                if not kind: continue
                city = city_name(a) if wanted == 'city' else 'Massachusetts'
                if wanted == 'city' and city not in CITY_SET: continue
                key = (city, kind)
                if key not in output or day > output[key].get('period_end','')[:10]:
                    a['period_end'] = day
                    output[key] = a
    return output

def source_page(a):
    ident = str(a.get('table_id') or '').strip()
    city = city_name(a)
    if ident.isdigit() and city:
        slug = re.sub(r'[^A-Za-z0-9]+', '-', city).strip('-')
        return f'https://www.redfin.com/city/{ident}/MA/{slug}/housing-market'
    return DATA_HOME

def real_estate_news():
    result = []
    for publisher, rss in FEEDS:
        try:
            req = Request(rss, headers={'User-Agent':'Mozilla/5.0 WestonLife/2.0'})
            with urlopen(req, timeout=9) as f:
                parsed = ElementTree.fromstring(f.read(600000))
            for item in parsed.findall('.//item')[:45]:
                title = html.unescape((item.findtext('title') or '').strip())
                link = (item.findtext('link') or '').strip()
                blob = title.lower()
                if not any(x in blob for x in ('housing','real estate','home sales','home price','condo','mortgage','residential','property market','home market', 'housing market')):
                    continue
                if not link.startswith('https://'): continue
                try:
                    date = parsedate_to_datetime(item.findtext('pubDate')).date()
                except (TypeError, ValueError): continue
                if date < datetime.now(timezone.utc).date()-timedelta(days=31) or date > datetime.now(timezone.utc).date(): continue
                result.append((title, title, link, publisher, str(date)))
        except (OSError, ValueError, ElementTree.ParseError) as ex:
            print('RSS unavailable '+publisher+': '+str(ex)[:90])
    dedup = {}
    for n in sorted(result, key=lambda x: x[4], reverse=True):
        dedup.setdefault(n[2], n)
    return list(dedup.values())[:4] or FALLBACK_REPORTS

def html_block(city_data, state_data):
    # No estimates: a failed API fetch displays only sourced September 2026 highlights.
    city_all = [city_data[(c,'all')] for c in TARGET if (c,'all') in city_data]
    city_all.sort(key=lambda a: (TARGET.index(city_name(a))))
    statewide = state_data.get(('Massachusetts','all'))
    period = max((a['period_end'] for a in city_all), default=None)
    city_rows=[]
    for a in city_all:
        city = city_name(a)
        sold = integer(a.get('homes_sold'))
        median = amt(a.get('median_sale_price'))
        ppsf = dollars(a.get('median_ppsf'))
        days = integer(a.get('median_dom'))
        page = source_page(a)
        city_rows.append(f'<tr><td><a href="{esc(page)}" target="_blank" rel="noopener noreferrer">{esc(city)} ↗</a></td><td>{sold}</td><td>{median}</td><td>{ppsf}</td><td>{days}</td><td>{esc(a["period_end"][:7])}</td></tr>')
    if not city_rows:
        city_rows=['<tr><td><a href="'+esc(REDFIN_WESTON)+'" target="_blank" rel="noopener noreferrer">Weston ↗</a></td><td>39</td><td>$2.27M</td><td>$518</td><td>66</td><td>2026-09</td></tr>']
        city_caveat='Redfin 批量下载尚未成功；目前仅展示已核实的 Weston 2026年9月数据，其他城市暂不填写。'
    else:
        city_caveat=f'数据期：截至 {esc(period[:7])} 的最近月度数据；每城市行另显示其所属月份。' if period else ''
    state_html = (
        f'<div class="mre-stat"><strong>{integer(statewide.get("homes_sold"))}</strong><span>麻州住宅成交套数 / MA homes sold</span></div>'
        f'<div class="mre-stat"><strong>{amt(statewide.get("median_sale_price"))}</strong><span>麻州成交价中位数 / MA median sale price</span></div>'
        f'<div class="mre-stat"><strong>{dollars(statewide.get("median_ppsf"))}</strong><span>麻州每平方英尺成交价中位数 / median $/sq.ft.</span></div>'
        if statewide else
        '<div class="mre-stat"><strong>$670K</strong><span>2026年9月麻州独栋成交价中位数（MAR，不是均价）</span></div>'
        '<div class="mre-stat"><strong>$525K</strong><span>2026年9月麻州公寓成交价中位数（MAR）</span></div>'
        '<div class="mre-stat"><strong>+4.8%</strong><span>2026年9月麻州独栋成交套数同比变化（MAR）</span></div>'
    )
    # Compare popular structure categories based on CLOSED SALES, never invent 3-bed/4-bed counts.
    type_names = [('single','独栋住宅 / Single-family'),('condo','公寓 / Condo/Co-op'),('townhouse','联排住宅 / Townhouse'),('multifamily','多户住宅 / Multi-family')]
    # Count only cities with a common latest reported month, not cross-month aggregates.
    type_counts=[]
    if period:
        for kind,label in type_names:
            val=sum(nfloat(city_data[(c,kind)].get('homes_sold')) or 0 for c in TARGET if (c,kind) in city_data and city_data[(c,kind)]['period_end'][:7]==period[:7])
            if val: type_counts.append((label,int(round(val))))
    type_counts.sort(key=lambda x:x[1],reverse=True)
    if type_counts:
        types = ''.join(f'<li><span>{esc(label)}</span><strong>{n:,}套</strong></li>' for label,n in type_counts)
        type_note = '统计范围仅为上表所列城市、同一数据月份；是住宅类别成交量，不是卧室数的户型排名。'
    else:
        types = '<li><span>可查看独栋、联排、公寓、多户住宅的实际销量</span><a href="'+DATA_HOME+'" target="_blank" rel="noopener noreferrer">Redfin数据 ↗</a></li>'
        type_note = '公开汇总数据尚不足以判断三卧、四卧哪种最畅销，因此不编造热门卧室数。'
    ranks=''.join(f'<span class="mre-rank"><em>{num:02d}</em>{esc(name)}</span>' for num,name in RANKS)
    news=''.join(f'<li><a href="{esc(link)}" target="_blank" rel="noopener noreferrer">{esc(zh)}</a><small>{esc(src)} · {esc(date)}</small></li>' for zh,en,link,src,date in real_estate_news())
    return f'''<!-- WESTON-MA-REAL-ESTATE-START -->
<style>
#wl-ma-realestate{{max-width:1100px;margin:35px auto 22px;padding:26px;background:#fbf8f1;color:#253b30;border:1px solid #d5ddd0;border-radius:14px;font-family:Georgia,'Times New Roman',serif;box-sizing:border-box}}
#wl-ma-realestate *{{box-sizing:border-box}}
#wl-ma-realestate h2{{font-size:clamp(30px,4vw,43px);color:#315c41;margin:7px 0 10px}}
#wl-ma-realestate h3{{font-size:22px;color:#315c41;margin:30px 0 10px}}
#wl-ma-realestate .mre-intro{{font:14px/1.7 Arial,sans-serif;color:#657463}}
#wl-ma-realestate .mre-stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:18px 0}}
#wl-ma-realestate .mre-stat{{background:white;border:1px solid #dfe4d8;padding:18px;border-radius:9px}}
#wl-ma-realestate .mre-stat strong{{font:bold clamp(19px,3vw,28px) Arial,sans-serif;color:#345f45;display:block}}
#wl-ma-realestate .mre-stat span{{font:12px/1.5 Arial,sans-serif;color:#677367;display:block;margin-top:9px}}
#wl-ma-realestate .mre-tablewrap{{overflow-x:auto}}
#wl-ma-realestate table{{border-collapse:collapse;width:100%;min-width:670px;font:13px Arial,sans-serif;background:white}}
#wl-ma-realestate td,#wl-ma-realestate th{{border-bottom:1px solid #e1e6db;padding:12px 9px;text-align:right;white-space:nowrap}}
#wl-ma-realestate td:first-child,#wl-ma-realestate th:first-child{{text-align:left}}
#wl-ma-realestate th{{background:#e9eee6;color:#365a42}}
#wl-ma-realestate a{{color:#28634a;text-decoration:underline;text-underline-offset:2px}}
#wl-ma-realestate .mre-notes{{font:12px/1.75 Arial,sans-serif;color:#637066}}
#wl-ma-realestate .mre-ranks{{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}}
#wl-ma-realestate .mre-rank{{background:#fff;border:1px solid #e1e3d9;border-radius:7px;padding:11px;font:14px Arial,sans-serif}}
#wl-ma-realestate .mre-rank em{{color:#b37837;margin-right:10px;font-style:normal;font-weight:700}}
#wl-ma-realestate .mre-types{{list-style:none;padding:0;margin:0}}
#wl-ma-realestate .mre-types li{{display:flex;justify-content:space-between;border-bottom:1px solid #ddd;padding:10px 2px;gap:10px}}
#wl-ma-realestate .mre-news{{padding-left:18px;font-size:15px;line-height:1.5}}
#wl-ma-realestate .mre-news li{{margin:12px 0}}
#wl-ma-realestate .mre-news small{{display:block;font:11px Arial,sans-serif;color:#727b70;margin:4px 0}}
@media(max-width:690px){{#wl-ma-realestate{{padding:18px}}#wl-ma-realestate .mre-stats{{grid-template-columns:1fr}}#wl-ma-realestate .mre-ranks{{grid-template-columns:1fr 1fr}}}}
</style>
<section id="wl-ma-realestate" aria-label="Massachusetts Real Estate Market">
<div style="color:#9c7146;letter-spacing:.12em;font:12px Arial,sans-serif">WESTON LIFE · PROPERTY MARKET</div>
<h2>🏡 MA 房地产市场 <span style="font-size:.55em;font-weight:400">Massachusetts Real Estate</span></h2>
<p class="mre-intro">MA各城市最近成交数据、房价、学区与热门住宅类型。数据按原始统计月份显示，不用挂牌价冒充成交价。</p>
<div class="mre-stats">{state_html}</div>
<p class="mre-notes">数据来源：<a href="{esc(DATA_HOME)}" target="_blank" rel="noopener noreferrer">Redfin Data Center</a> / <a href="{esc(MAR_SOURCE)}" target="_blank" rel="noopener noreferrer">Massachusetts Association of REALTORS（经 Boston Agent Magazine 报道）</a>。均为中位成交价（median），不是平均成交价（mean）；仅在来源明确提供时显示。</p>
<h3>各 City 最新成交 / Latest Closed Sales by City</h3>
<div class="mre-tablewrap"><table><thead><tr><th>City 城市</th><th>成交套数</th><th>成交价中位数</th><th>$/sq.ft.</th><th>挂牌天数中位数</th><th>月份</th></tr></thead><tbody>{''.join(city_rows)}</tbody></table></div>
<p class="mre-notes">{city_caveat} 口径：Redfin All Residential，成交套数为月度实际成交；本栏目不把所列城市中位价简单平均当作整个地区的真实平均总价。<a href="{esc(DATA_HOME)}" target="_blank" rel="noopener noreferrer">查看完整数据与方法 ↗</a></p>
<h3>学区排名 / School District Rankings</h3>
<p class="mre-notes">2027 年 Niche 麻州公立学区排行榜（2026年9月发布）；以下显示前十名及 Newton、Wellesley。排名属于 Niche 的评价，不是官方州教育厅排名。</p>
<div class="mre-ranks">{ranks}</div>
<p class="mre-notes"><a href="{esc(NICHESOURCE)}" target="_blank" rel="noopener noreferrer">Boston.com：2027 Niche MA 学区排名（2026-10-23） ↗</a></p>
<h3>哪类住宅成交最活跃 / Most Active Home Types</h3>
<ul class="mre-types">{types}</ul><p class="mre-notes">{type_note}</p>
<h3>MA 房地产新闻 / Local Property Headlines</h3>
<ul class="mre-news">{news}</ul>
<p class="mre-notes">数据随 Redfin 月度数据和媒体源更新；各条新闻点击在新标签页打开，不跳转至 Google 新闻搜索页。</p>
</section>
<!-- WESTON-MA-REAL-ESTATE-END -->'''


def update_home(index, panel):
    index = re.sub(r'\n*<!-- WESTON-MA-REAL-ESTATE-START -->.*?<!-- WESTON-MA-REAL-ESTATE-END -->\n*', '', index, flags=re.S)
    # School block is inserted dynamically by news script, so anchor before DAILY school section.
    anchors = ['<!-- WESTON-SCHOOL-DAILY-START -->', '<section id="wl-school-today"', '<!-- WESTON-SCHOOL-START -->', '<section id="wl-school"']
    for anchor in anchors:
        at = index.find(anchor)
        if at >= 0:
            return index[:at] + panel + '\n' + index[at:]
    raise RuntimeError('Cannot find Weston school section; website unchanged to avoid placing content incorrectly')


def main():
    if not INDEX.exists(): raise FileNotFoundError(INDEX)
    city, state = {}, {}
    try:
        city = fetch_table(CITY_URL, 'city')
        print('Redfin city dataset: %d matching city-type series' % len(city))
    except Exception as exc:
        print('City table unavailable; show dated verified sources only: '+str(exc)[:150])
    try:
        state = fetch_table(STATE_URL, 'state')
        print('Redfin state dataset: %d matching series' % len(state))
    except Exception as exc:
        print('State table unavailable; show dated verified MAR fallback only: '+str(exc)[:150])
    original = INDEX.read_text('utf-8')
    updated = update_home(original, html_block(city,state))
    if updated != original:
        INDEX.write_text(updated, 'utf-8')
    print('MA real estate block inserted directly BEFORE Today Weston School; cities=%d' % len([x for x in city if x[1]=='all']))

if __name__ == '__main__':
    main()
