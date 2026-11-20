#!/usr/bin/env python3
"""Weston Life — publish one numbered poem every 2 days, from #6 to #100.

Book pages/illustrations are shipped as ZIP archives in the repository root.
The source PDF is never committed by this script. API credentials are read
from GitHub Secrets, never logged or written to the public site.
"""
from __future__ import annotations
import argparse
import base64
from datetime import date, datetime, timedelta
import html
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo
import zipfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'poetry-auto'
SOURCE_BUNDLES = ['poetry-source-pages-1.zip', 'poetry-source-pages-2.zip']
COVERS_BUNDLE = 'poetry-book-illustrations.zip'
ANCHOR = date(2026, 11, 19)  # #5 already published this day
PUBLIC_RAW = 'https://raw.githubusercontent.com/westonlife/westonlife-news/main/poetry-auto/'
# Page numbers in the user-supplied 190-page book, NOT poem numbers.
PAGE_STARTS = [
    9,10,11,13,15,16,18,20,21,23,25,26,28,30,33,34,35,37,38,39,
    40,41,43,44,46,47,49,53,56,57,58,59,66,67,68,70,72,73,76,79,
    80,82,83,84,86,87,88,90,92,93,95,96,97,99,101,102,103,104,105,107,
    108,110,110,112,113,114,116,117,120,121,121,123,125,126,129,131,132,134,136,137,
    140,141,144,145,147,148,150,152,154,156,157,166,168,172,176,179,181,184,186,188,
]
assert len(PAGE_STARTS) == 100 and PAGE_STARTS[5] == 16
KNOWN = {6:'咏鹅',7:'春晓',8:'宿建德江',9:'过故人庄',10:'咏柳'}


def today_ny():
    return datetime.now(ZoneInfo('America/New_York')).date()


def due_number(day:date) -> int:
    return min(100, max(5, 5 + (day-ANCHOR).days//2))


def current_published() -> int:
    latest = OUT / 'latest.json'
    if not latest.exists(): return 5
    data = json.loads(latest.read_text(encoding='utf-8'))
    return int(data['number'])


def image_bytes(zips:list[zipfile.ZipFile], entry:str):
    for z in zips:
        try:return z.read(entry)
        except KeyError: continue
    raise FileNotFoundError(f'Missing book image in source bundles: {entry}')


def poem_pages(number):
    begin = PAGE_STARTS[number-1]
    end = PAGE_STARTS[number] - 1 if number<100 else 190
    # Same original page can contain two poems; extract and distinguish by number.
    return list(range(begin, max(begin,end)+1))


def vision_extract(client, number, images):
    title_hint = KNOWN.get(number, '')
    prompt = f'''你是一名中文古籍编辑，正在整理用户本人提供的《100诗词》扫描原书。请仅根据附件页面忠实整理**第{number}首**。
原书目录此首起始页为{PAGE_STARTS[number-1]}，参考题名“{title_hint}”。截图可能包含前一首或下一首，要明确区分诗歌编号与PDF页码。
请返回**纯 JSON 对象**（无 markdown）：
{{"number":{number},"title":"题目","author":"作者/时代（不确定则写作者不详）","poem_text":"完整原诗（保留换行）","translation":"忠实通俗译文","background":"作者和创作背景，严格区分史实与传说","analysis":"结合书中讲解的赏析","explanation_script":"连贯中文配音稿，包括原诗引入、逐句译文、作者、历史背景、赏析，至少250字；不能增写未经证实的史实","legibility_ok":true}}
严格要求：逐字核实诗文，绝不猜不清楚的字。若页面模糊或属于另一个诗编号，legibility_ok=false并说明原因。书本并非可靠史料，背景中争议或错误需保守表达。不得假造朝代、作者或史实。
对于很长的诗，必须完整抄录，不得用省略号。只回 JSON。'''
    content = [{'type':'input_text','text':prompt}]
    for pic in images:
        content.append({'type':'input_image','image_url':'data:image/jpeg;base64,'+base64.b64encode(pic).decode('ascii'),'detail':'high'})
    response = client.responses.create(model=os.getenv('POETRY_VISION_MODEL','gpt-4.1'),input=[{'role':'user','content':content}],max_output_tokens=10000)
    raw=response.output_text.strip()
    if raw.startswith('```'):
        raw=re.sub(r'^```(?:json)?\s*|\s*```$', '', raw, flags=re.I)
    item=json.loads(raw)
    if not item.get('legibility_ok'):raise ValueError(f'AI flagged illegible page for poem {number}; publish cancelled')
    if int(item.get('number',0))!=number:raise ValueError('wrong poem number returned')
    minimums = {'title':1,'author':1,'poem_text':8,'translation':12,'background':20,'analysis':20,'explanation_script':100}
    for key, minimum in minimums.items():
        if not isinstance(item.get(key),str) or len(item[key].strip()) < minimum:
            raise ValueError(f'missing/invalid source field {key}')
    if title_hint and title_hint not in item['title']:
        raise ValueError(f'Expected {title_hint} but received {item["title"]}; publish cancelled')
    if ('……' in item['poem_text'] or '...' in item['poem_text']):
        raise ValueError('poem likely truncated; publish cancelled')
    return item


def speech_chunks(text,max_chars=1450):
    units=re.split(r'(?<=[。！？；;\n])',text)
    result=[];chunk=''
    for u in units:
        if len(u)>max_chars:
            if chunk:result.append(chunk);chunk=''
            result.extend(u[i:i+max_chars] for i in range(0,len(u),max_chars))
        elif len(chunk)+len(u)>max_chars:
            result.append(chunk);chunk=u
        else:chunk+=u
    if chunk:result.append(chunk)
    return [x for x in result if x.strip()]


def synthesize(client, text, path,kind):
    texts=speech_chunks(text)
    # Save every segment before concatenation: a failure never publishes half audio.
    with tempfile.TemporaryDirectory() as tmp:
        paths=[]
        for ix,section in enumerate(texts):
            seg=Path(tmp)/f'{ix:02d}.mp3'
            response=client.audio.speech.create(
                model=os.getenv('POETRY_TTS_MODEL','gpt-4o-mini-tts'),
                voice=os.getenv('POETRY_TTS_VOICE','alloy'),
                input=section,
                instructions=('中文普通话，清晰、舒缓、有古诗节奏，诗句间稍作停顿。' if kind=='recitation'
                              else '中文普通话，温和自然，像讲解中国诗词历史文化的老师，吐字清楚。'),
                response_format='mp3')
            response.write_to_file(seg)
            paths.append(seg)
        if len(paths)==1:shutil.copyfile(paths[0],path)
        else:
            concat=Path(tmp)/'concat.txt'
            concat.write_text('\n'.join(f"file '{p}'" for p in paths),encoding='utf-8')
            proc=subprocess.run(['ffmpeg','-nostdin','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-y',str(path)],capture_output=True,text=True)
            if proc.returncode:raise RuntimeError(f'ffmpeg concat failed: {proc.stderr[-300:]}')
    if not path.exists() or path.stat().st_size<1024: raise RuntimeError(f'Empty audio {path}')


def html_page(number, title):
    h=html.escape(title)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第{number}首《{h}》｜诗词里的中国｜Weston Life</title>
<style>body{{margin:0;color:#29372d;background:#faf8f2;font-family:"Songti SC","Noto Serif SC",Georgia,serif;line-height:1.85}}.wrap{{max-width:860px;margin:auto;padding:30px 20px 70px}}a{{color:#365b47}}.tag{{text-align:center;color:#9b6c4c}}h1{{font-size:clamp(30px,6vw,46px);text-align:center}}h2{{color:#365b47;font-weight:500;border-bottom:1px solid #dbe3da}}.cover{{display:block;max-width:min(100%,760px);width:100%;height:auto;margin:24px auto;border-radius:10px}}.panel{{background:#fff;padding:22px;border-radius:14px;margin:22px auto;border:1px solid #e5e0d4}}.verse{{white-space:pre-line;text-align:center;font-size:clamp(21px,3vw,27px);line-height:2}}audio{{width:100%}}.sub{{text-align:center;color:#777}}footer{{font-size:13px;color:#777;text-align:center;padding:30px}}@media(max-width:600px){{.panel{{padding:16px}}}}</style></head><body><main class="wrap"><p><a href="/poetry.html">← 返回《诗词里的中国》与历史目录</a></p><p class="tag">第{number}首 / CHINA IN 100 POEMS</p><h1 id="title">{h}</h1><div id="item"><p>正在加载诗歌内容…</p></div></main><footer>Weston Life · 诗词里的中国 · AI 辅助朗读与整理，原文以图书为准</footer><script src="/poetry-auto/poetry-rotation.js" defer></script></body></html>'''


def ensure_site_scripts():
    # The existing counter.js tag and other code are never modified.
    tag='<script defer src="/poetry-auto/poetry-rotation.js"></script>'
    for name in ['index.html','poetry.html']:
        path=ROOT/name
        if not path.exists():raise FileNotFoundError(name)
        s=path.read_text('utf-8')
        if tag in s:continue
        pos=s.rfind('</body>')
        if pos<0:raise ValueError(f'Cannot locate </body> in {name}')
        updated=s[:pos]+tag+'\n'+s[pos:]
        if name=='index.html' and s.count('/counter.js')!=updated.count('/counter.js'):
            raise ValueError('Counter reference changed: refused')
        path.write_text(updated,encoding='utf-8')


def publish(number,day):
    from openai import OpenAI
    key=os.getenv('OPENAI_API_KEY')
    if not key:raise RuntimeError('OPENAI_API_KEY is not set; nothing was published')
    client=OpenAI(api_key=key,timeout=180,max_retries=2)
    with zipfile.ZipFile(ROOT/COVERS_BUNDLE) as cv:
        cover=cv.read(f'covers/{number:03d}.jpg')
    with zipfile.ZipFile(ROOT/SOURCE_BUNDLES[0]) as z1,zipfile.ZipFile(ROOT/SOURCE_BUNDLES[1]) as z2:
        pages=poem_pages(number)
        images=[image_bytes([z1,z2],f'book_pages/{p:03d}.jpg') for p in pages]
    print(f'Source poem #{number} spans page(s): {pages}. Calling vision service...')
    item=vision_extract(client,number,images)
    data_dir=OUT/'data';media=OUT/'media';data_dir.mkdir(parents=True,exist_ok=True);media.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        rec=Path(td)/'rec.mp3'; expl=Path(td)/'expl.mp3'
        poem_text='第'+str(number)+'首，'+item['title']+'。'+item['author']+'。\n'+item['poem_text']
        explanation=item['explanation_script']
        print('Creating two Mandarin MP3 recordings...')
        synthesize(client,poem_text,rec,'recitation')
        synthesize(client,explanation,expl,'explanation')
        shutil.copyfile(rec,media/f'{number:03d}-recitation.mp3')
        shutil.copyfile(expl,media/f'{number:03d}-explanation.mp3')
    (media/f'{number:03d}-cover.jpg').write_bytes(cover)
    record={k:item[k].strip() for k in ['title','author','poem_text','translation','background','analysis','explanation_script']}
    record.update(number=number,release_date=day.isoformat(),book_pages=pages,
        cover=f'{PUBLIC_RAW}media/{number:03d}-cover.jpg',
        recitation=f'{PUBLIC_RAW}media/{number:03d}-recitation.mp3',
        explanation=f'{PUBLIC_RAW}media/{number:03d}-explanation.mp3',
        url=f'/poetry-auto/poem.html?n={number:03d}')
    (data_dir/f'{number:03d}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n','utf-8')
    index=[]
    for f in sorted(data_dir.glob('[0-9][0-9][0-9].json'),reverse=True):
        x=json.loads(f.read_text('utf-8'))
        index.append({k:x[k] for k in ['number','title','author','release_date','cover','url']})
    (OUT/'archive.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n','utf-8')
    (OUT/'latest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n','utf-8')
    ensure_site_scripts()
    print(f'Published poem #{number}: {record["title"]}; cover + two MP3s + archive indexed')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--date',help='YYYY-MM-DD, test or manual run date (NY local)')
    p.add_argument('--dry-run',action='store_true')
    args=p.parse_args()
    now=date.fromisoformat(args.date) if args.date else today_ny()
    target=due_number(now);last=current_published();next_num=last+1
    print(f'NY date={now} / due through=#{target} / published=#{last} / next=#{next_num}')
    if next_num>100:print('All 100 poems complete. No changes.');return
    if args.dry_run:
        scheduled=ANCHOR+timedelta(days=2*(next_num-5))
        print(f'DRY RUN ONLY: next poem #{next_num}, scheduled {scheduled}, book pages {poem_pages(next_num)}')
        return
    if next_num>target:print('Not yet scheduled. No changes.');return
    publish(next_num,now)

if __name__=='__main__':main()
