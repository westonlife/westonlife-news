#!/usr/bin/env python3
"""Refresh public Weston school RSS notices; preserve old records and do not invent new ones.
This only writes school-notices.json, never changes index.html or existing news.
"""
import json
import re
import html
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from xml.etree import ElementTree
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'school-notices.json'
SOURCES=[
 ('Weston High School','https://www.westonschools.org/high/feed/'),
 ('Weston Public Schools','https://www.westonschools.org/feed/'),
 ('Weston Public Schools','https://www.westonschools.org/news/feed/'),
 ('Weston Middle School','https://www.westonschools.org/middle/feed/'),
]
CUTOFF=datetime.now(timezone.utc)-timedelta(days=120)
TRANSLATED={
 'picture retake day 10/27/2026':'10月27日：高中补拍学生照片',
 'class of 2027 chipotle fundraiser 10/24':'10月24日：2027届学生筹款活动',
 'senior class lynch creek fundraiser':'高四毕业班 Lynch Creek 筹款通知',
}

def previous():
 try:
  data=json.loads(OUTPUT.read_text(encoding='utf-8'))
  return data.get('notices',[]) if isinstance(data,dict) else []
 except (OSError,ValueError):return []

def valid(row):
 u=row.get('url','');host=urlparse(u).hostname or ''
 return (u.startswith('https://www.westonschools.org/') and host=='www.westonschools.org'
  and re.fullmatch(r'20\d\d-\d\d-\d\d',row.get('published',''))
  and bool(row.get('title','').strip()))

def readfeed(label,url):
 req=Request(url,headers={'User-Agent':'Mozilla/5.0 (WestonLife/1.0; public school news attribution)'})
 with urlopen(req,timeout=18) as f:data=f.read(1_000_000)
 root=ElementTree.fromstring(data)
 output=[]
 for item in root.findall('.//item')[:60]:
  title=html.unescape(re.sub(r'<[^>]+>',' ',item.findtext('title') or '')).strip()
  link=(item.findtext('link') or '').strip();datestr=item.findtext('pubDate') or ''
  try:d=parsedate_to_datetime(datestr);d=d if d.tzinfo else d.replace(tzinfo=timezone.utc)
  except (TypeError,ValueError,IndexError):continue
  if d<CUTOFF or d>datetime.now(timezone.utc)+timedelta(days=1):continue
  day=d.astimezone(timezone.utc).strftime('%Y-%m-%d')
  obj=dict(title=title,published=day,source=label,url=link)
  if TRANSLATED.get(title.lower()):obj['zh']=TRANSLATED[title.lower()]
  if valid(obj):output.append(obj)
 return output

def run():
 old=previous();new=[]
 for label,url in SOURCES:
  try:
   items=readfeed(label,url);new.extend(items);print(label, len(items))
  except Exception as exc:print('Feed unavailable:',label,repr(exc))
 if not new and old:
  print('No current feed data; preserving existing notice archive')
  return
 byurl={}
 for a in old:
  if valid(a):byurl[a['url']]=a
 for a in new:
  if valid(a):byurl[a['url']]={**byurl.get(a['url'],{}),**a}
 rows=sorted(byurl.values(),key=lambda a:(a['published'],a['title']),reverse=True)[:90]
 if not rows:raise RuntimeError('No verified Weston school notices found; nothing published')
 OUTPUT.write_text(json.dumps({'updated':datetime.now(timezone.utc).strftime('%Y-%m-%d'),'notices':rows},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print('Saved',len(rows),'notices')

if __name__=='__main__':run()
