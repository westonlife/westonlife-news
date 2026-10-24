"""Weston Life oil market card: Brent first, WTI second; no invented quotes."""
import html
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DAY = datetime.now(ZoneInfo('America/New_York')).strftime('%Y-%m-%d')
START = '<!-- OIL-HEADLINE-START -->'
END = '<!-- OIL-HEADLINE-END -->'
BRENT = 'https://tradingeconomics.com/commodity/brent-crude-oil'
WTI = 'https://tradingeconomics.com/commodity/crude-oil'


def strip_old(text):
    return re.sub(re.escape(START) + r'.*?' + re.escape(END), '', text, flags=re.S)


def main():
    index_file = ROOT / 'index.html'
    daily_file = ROOT / ('news-' + DAY + '.html')
    index = strip_old(index_file.read_text(encoding='utf-8'))
    daily = strip_old(daily_file.read_text(encoding='utf-8'))
    # Quote providers show live prices; do not pretend static figures are live.
    card = f'''{START}
<div class="wl-story wl-oil" style="border-left:5px solid #b91c1c;background:#fff9f4;display:block;padding:15px 18px;min-height:0">
  <div style="font:700 23px Georgia,serif;color:#a52c24;margin-bottom:4px">å½éåæ²¹ä»·æ ¼</div>
  <div style="font:700 12px Arial,sans-serif;letter-spacing:.12em;color:#785c4d;margin-bottom:12px">GLOBAL OIL PRICES</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">
    <a href="{BRENT}" target="_blank" rel="noopener noreferrer" style="display:block;padding:12px 10px;border:1px solid #e7cbbd;border-radius:8px;background:white;text-decoration:none;color:#263c36">
      <strong style="display:block;font:700 17px Arial,sans-serif">Brent</strong><span style="font:12px Arial,sans-serif">å¸ä¼¦ç¹åæ²¹</span><span style="display:block;margin-top:9px;color:#b91c1c;font:700 13px Arial,sans-serif">æ¥çææ°æ¥ä»· â</span>
    </a>
    <a href="{WTI}" target="_blank" rel="noopener noreferrer" style="display:block;padding:12px 10px;border:1px solid #e7cbbd;border-radius:8px;background:white;text-decoration:none;color:#263c36">
      <strong style="display:block;font:700 17px Arial,sans-serif">WTI</strong><span style="font:12px Arial,sans-serif">ç¾å½åæ²¹</span><span style="display:block;margin-top:9px;color:#b91c1c;font:700 13px Arial,sans-serif">æ¥çææ°æ¥ä»· â</span>
    </a>
  </div>
  <div style="font:11px Arial,sans-serif;color:#766b64;margin-top:10px">ç¾åï¼æ¡¶ Â· å®æ¶ä»·æ ¼ä¸æ¶¨è·å¹è¯·ç¹å»è¡æé¾æ¥ / USD per barrel Â· Tap for live quotes</div>
</div>{END}'''
    detail = f'''{START}
<article class="item" id="story-oil" style="border-top:5px solid #b91c1c">
<h3 style="color:#a52c24">å½éåæ²¹ä»·æ ¼ / Global Oil Prices</h3>
<p>å½éæ²¹ä»·åºåï¼Brent å¸ä¼¦ç¹åæ²¹ä¸ WTI ç¾å½åæ²¹ãç¹å»ä»¥ä¸é¾æ¥æ¥çææ°æ¥ä»·ãæ¶¨è·å¹åæ¥ä»·æ¶é´ã</p>
<p>International crude benchmarks: Brent and WTI. Open the quote pages for the latest price, daily change and timestamp.</p>
<p><a href="{BRENT}" target="_blank" rel="noopener noreferrer">Brent å¸ä¼¦ç¹åæ²¹ Â· å®æ¶è¡æ â</a></p>
<p><a href="{WTI}" target="_blank" rel="noopener noreferrer">WTI ç¾å½åæ²¹ Â· å®æ¶è¡æ â</a></p>
<p style="font-size:12px;color:#666">Weston Life does not independently provide a live market-data feed. Quotes are displayed by the linked providers.</p>
</article>{END}'''
    m = re.search(r'<h2 class="wl-column-title world">.*?</h2>', index, re.S)
    n = re.search(r'<h2>World News / Global</h2>\s*<div class="news">', daily)
    if not m or not n:
        raise RuntimeError('News headings not found; files not changed')
    index = index[:m.end()] + card + index[m.end():]
    daily = daily[:n.end()] + detail + daily[n.end():]
    index_file.write_text(index, encoding='utf-8')
    daily_file.write_text(daily, encoding='utf-8')
    print('Oil price card updated: Brent first, WTI second; existing 15 stories preserved.')

if __name__ == '__main__':
    main()
