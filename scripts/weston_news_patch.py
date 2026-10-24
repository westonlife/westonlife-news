#!/usr/bin/env python3
"""Post-generation Weston Life daily repair; run after generate_news and add_oil_headline.
Preserves the original website, archives, articles and input sources. stdlib only.
"""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
from urllib.parse import urlparse
import re
import os

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT/'index.html'
TODAY = datetime.now().astimezone().strftime('%Y-%m-%d')
# GitHub workflow runs on UTC; Boston date is used by the upstream generator.
try:
    from zoneinfo import ZoneInfo
    TODAY = datetime.now(ZoneInfo('America/New_York')).strftime('%Y-%m-%d')
except ImportError:
    pass
NEWS = ROOT/f'news-{TODAY}.html'
LEAF_DAY = '2026-10-23'
LEAF_URL = 'https://westonobserver.org/gas-leaf-blower-ban-proposed/'
LEAF_PHOTO = 'https://dxy0ub64f43cw.cloudfront.net/wp-content/uploads/2026/10/22115615/TownGreenFall2025-1024x683.jpg'
# Verified Oct. 22–23, 2026 fallback reports. Use only within a reasonable news horizon.
FALLBACKS = [
  {'title':'10月22日隔夜要闻：美股与科技企业动态','en':'Futu: Overnight market and tech company headlines','summary':'富途牛牛公开新闻汇总了美股市场、人工智能公司财报与大宗商品的主要消息。','en_summary':'A publicly accessible Futu article rounds up US market, technology earnings and commodity developments.','url':'https://news.futunn.com/post/1001863220','source':'富途牛牛（转载新浪财经）','date':'2026-10-22','image':'assets/news/9616929c4dd8789c6a3d1c46.gif'},
  {'title':'国际油价走高，美股周五承压','en':'Wall Street loses ground under pressure from rising oil prices','summary':'美联社报道，10月23日美国股市受油价上扬影响收低，投资者关注能源成本与科技投资。','en_summary':'AP reports Wall Street declined on Oct. 23 as higher oil prices weighed on markets.','url':'https://apnews.com/article/7b47ef3b037bfba4e34f685329b9b963','source':'Associated Press','date':'2026-10-23','image':'assets/news/527122470b35477633dec675.jpg'},
  {'title':'AI概念股回调与原油上涨牵动全球市场','en':'Sharp drops for AI stocks overwhelm markets worldwide as oil prices jump','summary':'美联社报道，人工智能相关股票下跌与石油价格上涨同时影响全球股市。','en_summary':'AP discusses declines in AI-related shares alongside rising oil prices and worldwide market moves.','url':'https://apnews.com/article/33767691a4a0730b96d6f0c5100ea9b2','source':'Associated Press','date':'2026-10-22','image':'assets/news/e3d1baa47312f39075e6f0dd.jpg'}
]

def e(s): return escape(str(s),quote=True)

def source_url(html):
    match=re.search(r'<a href="(https://[^"]+)"[^>]*>原始报道',html)
    return match.group(1) if match else ''

def archive_pool(exclude):
    """Use dated actual original publisher stories from past news pages, never home-page pointers."""
    out=[]
    pages=sorted(ROOT.glob('news-20??-??-??.html'),reverse=True)
    for page in pages[:20]:
        if page == NEWS: continue
        for card in re.findall(r'<article class="item" id="story-\d+">.*?</article>',page.read_text(encoding='utf-8'),flags=re.S):
            url=source_url(card)
            if not url or url in exclude or 'news.google.com' in url: continue
            img=re.search(r'<img class="story-photo" src="([^"]+)"',card)
            if not img: continue
            image=img.group(1)
            if image.startswith('assets/') and not (ROOT/image).exists(): continue
            title=re.search(r'<h3 class="zh-title">(.*?)</h3>',card,re.S)
            en=re.search(r'<p class="en en-title">(.*?)</p>',card,re.S)
            z=re.search(r'<p class="zh-summary">(.*?)</p>',card,re.S)
            ens=re.search(r'<p class="en-summary">(.*?)</p>',card,re.S)
            meta=re.search(r'<p class="meta">(.*?)</p>',card,re.S)
            if not all([title,en,z,ens,meta]): continue
            date_match=re.search(r'(20\d\d-\d\d-\d\d)',meta.group(1))
            if not date_match: continue
            try: age=(datetime.strptime(TODAY,'%Y-%m-%d')-datetime.strptime(date_match.group(1),'%Y-%m-%d')).days
            except ValueError: continue
            if age<0 or age>14: continue
            title_text=re.sub('<[^>]+>','',title.group(1))
            en_text=re.sub('<[^>]+>','',en.group(1))
            # Local stories must not be used to fill global positions.
            meta_source=re.sub('<[^>]+>','',meta.group(1).split(' · ')[0])
            if any(word in (title_text+' '+en_text).lower() for word in ('weston','boston','massachusetts','waltham','newton ')):continue
            out.append({'title':title_text,'en':en_text,'summary':re.sub('<[^>]+>','',z.group(1)),'en_summary':re.sub('<[^>]+>','',ens.group(1)),
              'url':url,'source':meta_source,'date':date_match.group(1),'image':image})
            exclude.add(url)
    return out

def card_home(row,n):
    # Treat previously sourced thematic pictures as illustrations; never as actual publisher photos.
    is_fallback=row in FALLBACKS
    note='<small style="display:block;font:10px Arial;color:#777">栏目主题配图，并非该篇原始新闻照片</small>' if is_fallback else ''
    return (f'<a class="wl-story" href="news-{TODAY}.html#story-{n}" aria-label="{e(row["title"])}">'
      f'<span class="wl-index">{n:02d}</span><div class="wl-photo"><img src="{e(row["image"])}" alt="{e("栏目主题配图" if is_fallback else "来源配图")}" loading="lazy"></div>'
      f'<div class="wl-copy"><strong>{e(row["title"])}</strong><span class="wl-en">{e(row["en"])}</span>'
      f'<span class="wl-source">{e(row["source"])} · {e(row["date"])}</span>{note}</div></a>')

def card_full(row,n):
    note='<p class="meta">栏目主题配图，非原文新闻图片</p>' if row in FALLBACKS else ''
    return (f'<article class="item" id="story-{n}"><div class="num">{n:02d}</div>'
      f'<img class="story-photo" src="{e(row["image"])}" alt="{e("主题插画" if row in FALLBACKS else "新闻来源配图")}" loading="lazy">{note}'
      f'<h3 class="zh-title">{e(row["title"])}</h3><p class="en en-title">{e(row["en"])}</p>'
      f'<p class="zh-summary">{e(row["summary"])}</p><p class="en-summary">{e(row["en_summary"])}</p>'
      f'<p class="meta">{e(row["source"])} · {e(row["date"])}</p>'
      f'<a href="{e(row["url"])}" target="_blank" rel="noopener noreferrer">原始报道 / Original source ↗</a></article>')

def leaf_home():
    return (f'<a class="wl-story" href="news-{TODAY}.html#story-1" aria-label="Weston居民将表决燃油落叶吹风机限制提案">'
            f'<span class="wl-index">01</span><div class="wl-photo"><img src="{LEAF_PHOTO}" alt="Weston Observer：秋季Weston Town Green（历史图片）" loading="lazy"></div>'
            f'<div class="wl-copy"><strong>Weston居民将表决燃油落叶吹风机限制提案</strong><span class="wl-en">Weston residents to weigh gas-powered leaf blower restrictions</span>'
            f'<span class="wl-source">Weston Observer · {LEAF_DAY}</span></div></a>')

def leaf_full():
    return (f'<article class="item" id="story-1"><div class="num">01</div><img class="story-photo" src="{LEAF_PHOTO}" alt="Weston Town Green，图片来源Weston Observer；历史图片" loading="lazy">'
            f'<h3 class="zh-title">Weston居民将表决燃油落叶吹风机限制提案</h3><p class="en en-title">Residents will weigh in on gas-powered leaf blower ban</p>'
            f'<p class="zh-summary">据《Weston Observer》2026年10月23日报道，11月23日的特别镇民大会将讨论燃油落叶吹风机使用限制提案。提案拟限制使用时段，且计划在2030年全面禁止燃油型号；目前仍为待表决提案。</p>'
            f'<p class="en-summary">The Weston Observer reported on Oct. 23 that a proposed gas-powered leaf-blower bylaw is slated for the Nov. 23 Special Town Meeting. It would restrict operating hours and phase out gas-powered models by 2030 if approved.</p>'
            f'<p class="meta">Weston Observer · {LEAF_DAY}</p><a href="{LEAF_URL}" target="_blank" rel="noopener noreferrer">原始报道 / Original source ↗</a></article>')

def patch():
    if not INDEX.exists() or not NEWS.exists(): print('No generated homepage / edition to enhance');return
    index=INDEX.read_text(encoding='utf-8'); news=NEWS.read_text(encoding='utf-8')
    hi=index.find('<!-- WESTON-LIFE-AUTO-START -->');he=index.find('<!-- WESTON-LIFE-AUTO-END -->',hi)
    if hi<0 or he<0:print('No generated panel; skip safely');return
    front=index[hi:he]
    # Leaf story is a specific replacement on Oct. 24, not an indefinite front-page item.
    if TODAY == '2026-10-24':
        front,n=re.subn(r'<a class="wl-story"[^>]*aria-label="[^"]*(?:转运站|Transfer Station)[^"]*".*?</a>',leaf_home(),front,count=1,flags=re.S|re.I)
        news,m=re.subn(r'<article class="item" id="story-1">.*?</article>',leaf_full(),news,count=1,flags=re.S)
        print('Leaf blower local story replaced: ',n,m)
    count=len(re.findall(r'<a class="wl-story"\b',front))
    world_count=len(re.findall(r'<a class="wl-story"\b',front[front.find('wl-column-title world'):]))
    if count<15 and world_count<10:
        used=set(re.findall(r'href="(https://[^\"]+)"[^>]*>原始报道',news))
        extra=[]
        if (datetime.strptime(TODAY,'%Y-%m-%d')-datetime(2026,10,22)).days in range(0,11):
            for row in FALLBACKS:
                if row['url'] not in used and (not row['image'].startswith('assets/') or (ROOT/row['image']).exists()):
                    extra.append(row);used.add(row['url'])
        extra.extend(archive_pool(used))
        available=10-world_count
        extra=extra[:available]
        if extra:
            new_home=''.join(card_home(row,count+pos+1) for pos,row in enumerate(extra))
            end_world=front.find('</div></div>\n<div class="wl-editorial">')
            if end_world < 0:end_world=front.find('</div></div>\n<div class="wl-editorial"')
            if end_world<0:
                print('Home layout has changed: not adding cards to unrecognized section')
            else:
                front=front[:end_world]+new_home+front[end_world:]
                new_full=''.join(card_full(row,count+pos+1) for pos,row in enumerate(extra))
                stop=news.rfind('</article>')
                if stop>=0:news=news[:stop+len('</article>')]+new_full+news[stop+len('</article>'):]
                print('Added %d published articles; current visible total=%d' % (len(extra),count+len(extra)))
    index=index[:hi]+front+index[he:]
    INDEX.write_text(index,encoding='utf-8');NEWS.write_text(news,encoding='utf-8')
    print('Weston Life postprocessor finished:',TODAY)

if __name__=='__main__':patch()
