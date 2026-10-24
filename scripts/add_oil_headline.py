
"""Weston Life oil market card: Brent first, WTI second."""

import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DAY = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")

START = "<!-- OIL-HEADLINE-START -->"
END = "<!-- OIL-HEADLINE-END -->"

BRENT = "https://tradingeconomics.com/commodity/brent-crude-oil"
WTI = "https://tradingeconomics.com/commodity/crude-oil"


def strip_old(text):
    return re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        "",
        text,
        flags=re.S,
    )


def main():
    index_file = ROOT / "index.html"
    daily_file = ROOT / ("news-" + DAY + ".html")

    index = strip_old(index_file.read_text(encoding="utf-8"))
    daily = strip_old(daily_file.read_text(encoding="utf-8"))

    card = f"""{START}
<div class="wl-story wl-oil"
     style="border-left:5px solid #b91c1c;background:#fff6f3;
            display:block;padding:18px;border-radius:8px">

  <div style="font:700 24px Georgia,serif;color:#a52c24">
    国际油价
  </div>
  <div style="font:700 13px Arial,sans-serif;color:#a52c24;
              margin:5px 0 14px">
    GLOBAL OIL PRICES
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;
              gap:12px">

    <a href="{BRENT}" target="_blank"
       rel="noopener noreferrer"
       style="display:block;padding:14px 10px;
              border:1px solid #e7cbbd;border-radius:8px;
              background:white;text-decoration:none;color:#263c36">
      <strong style="display:block;font:700 19px Arial,sans-serif">
        Brent
      </strong>
      <span style="display:block;font:12px Arial,sans-serif">
        布伦特原油
      </span>
      <span style="display:block;margin-top:10px;
                   color:#b91c1c;font:700 13px Arial,sans-serif">
        查看最新行情 →
      </span>
    </a>

    <a href="{WTI}" target="_blank"
       rel="noopener noreferrer"
       style="display:block;padding:14px 10px;
              border:1px solid #e7cbbd;border-radius:8px;
              background:white;text-decoration:none;color:#263c36">
      <strong style="display:block;font:700 19px Arial,sans-serif">
        WTI
      </strong>
      <span style="display:block;font:12px Arial,sans-serif">
        美国原油
      </span>
      <span style="display:block;margin-top:10px;
                   color:#b91c1c;font:700 13px Arial,sans-serif">
        查看最新行情 →
      </span>
    </a>
  </div>

  <div style="font:12px Arial,sans-serif;color:#766b64;
              margin-top:12px">
    单位：美元/桶 · 点击查看价格、涨跌幅和更新时间
  </div>
</div>
{END}"""

    detail = f"""{START}
<article class="item" id="story-oil"
         style="border-top:5px solid #b91c1c">
  <h3 style="color:#a52c24">国际油价 / Global Oil Prices</h3>
  <p>布伦特原油与WTI美国原油最新市场行情。</p>
  <p>Brent and WTI crude oil market quotations.</p>
  <p><a href="{BRENT}" target="_blank"
        rel="noopener noreferrer">Brent 最新行情 ↗</a></p>
  <p><a href="{WTI}" target="_blank"
        rel="noopener noreferrer">WTI 最新行情 ↗</a></p>
  <p>价格及更新时间以行情提供方为准。</p>
</article>
{END}"""

    home_heading = re.search(
        r'<h2 class="wl-column-title world">.*?</h2>',
        index,
        flags=re.S,
    )
    daily_heading = re.search(
        r'<h2>World News / Global</h2>\s*<div class="news">',
        daily,
    )

    if not home_heading or not daily_heading:
        raise RuntimeError(
            "News headings not found. No files changed."
        )

    index = (
        index[:home_heading.end()]
        + card
        + index[home_heading.end():]
    )

    daily = (
        daily[:daily_heading.end()]
        + detail
        + daily[daily_heading.end():]
    )

    index_file.write_text(index, encoding="utf-8")
    daily_file.write_text(daily, encoding="utf-8")

    print("Oil card updated. Existing 15 stories preserved.")


if __name__ == "__main__":
    main()
