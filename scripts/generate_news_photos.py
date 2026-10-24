"""Weston Life newsroom: image-quality checked entrypoint for generate_news.py.

Place alongside scripts/generate_news.py and change the workflow command from
    python scripts/generate_news.py
to
    python scripts/generate_news_photos.py

This preserves all 15 fixed editorial slots, translations, oil-card generation,
and state persistence in the original program. It rejects image-only graphics and
hides placeholder *pictures* while preserving honest 'No New Updates' notices.

The existing OPENAI_API_KEY and NEWS_API_KEY workflow secrets are reused.
"""
import base64
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import generate_news as news

QUALITY_CACHE = news.ROOT / "news_photo_quality.json"
MAX_NEW_CHECKS = int(os.getenv("WESTONLIFE_MAX_PHOTO_CHECKS", "35"))
MODEL = os.getenv("WESTONLIFE_IMAGE_MODEL", "gpt-4o-mini")
_new_checks = 0


def _load_quality_cache():
    try:
        records = json.loads(QUALITY_CACHE.read_text(encoding="utf-8"))
        return records if isinstance(records, dict) else {}
    except (FileNotFoundError, ValueError, OSError):
        return {}


_quality = _load_quality_cache()


def _image_size(data):
    """Small no-dependency geometry checks; unknown size is reviewed by vision."""
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP" and data[12:16] == b"VP8X" and len(data) >= 30:
        return int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1
    if data.startswith(b"\xff\xd8"):
        p = 2
        while p + 10 < len(data):
            if data[p] != 0xff:
                break
            marker = data[p + 1]
            if marker in (0xd8, 0xd9, 0x01):
                p += 2
                continue
            seglen = int.from_bytes(data[p + 2:p + 4], "big")
            if seglen < 2:
                break
            if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf):
                return int.from_bytes(data[p + 7:p + 9], "big"), int.from_bytes(data[p + 5:p + 7], "big")
            p += 2 + seglen
    return None


def _image_is_good(image_path, article):
    global _new_checks
    path = news.ROOT / image_path
    if not path.is_file() or path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        return False
    try:
        raw = path.read_bytes()
    except OSError:
        return False
    if len(raw) < 8_000 or len(raw) > 4_000_000:
        return False
    dims = _image_size(raw)
    if dims:
        w, h = dims
        if w < 400 or h < 230 or w / max(h, 1) > 3.4 or h / max(w, 1) > 2.5:
            return False
    title = str(article.get("title") or "")
    identity = hashlib.sha256(raw + title.encode("utf-8")).hexdigest()
    if identity in _quality:
        return bool(_quality[identity])
    if _new_checks >= MAX_NEW_CHECKS:
        return False  # fail closed: never insert unchecked pictures
    _new_checks += 1
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}[path.suffix.lower()]
    prompt = (
        "You are a strict news photo editor. Evaluate whether this is a genuine photographic "
        "image suitable for illustrating the SPECIFIC headline below. Accept real photographed "
        "people, events, locations, scenes, products, buildings, or machines directly related to the story. "
        "Reject logos, branding, PR logo collages, infographics, charts, screenshots, photographs "
        "dominated by text, event flyers, promotional posters, illustrations, decorative graphics, "
        "article thumbnails with prominent wordmarks, or unrelated stock photos. "
        "Do not infer an association from the company logo alone. Return only JSON: "
        '{"accept": true/false}. Headline: ' + title[:280]
    )
    body = {
        "model": MODEL,
        "temperature": 0,
        "max_tokens": 60,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": "data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii"), "detail": "low"}},
        ]}],
    }
    try:
        request = Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=28) as response:
            result = json.loads(response.read().decode("utf-8"))
        answer = json.loads(result["choices"][0]["message"]["content"])
        allowed = answer.get("accept") is True
        _quality[identity] = allowed
        print(f"PHOTO {'OK' if allowed else 'SKIP'}: {image_path} for {title[:55]}")
        return allowed
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, OSError) as exc:
        print(f"Image review unavailable; no unverified photo accepted: {exc}", file=sys.stderr)
        return False


def _photo_with_quality(article):
    """Review all candidates, including cached ones, not just their filenames."""
    old = str(article.get("image") or "")
    if old.startswith("assets/news/") and _image_is_good(old, article):
        return old
    urls = []
    if old.startswith("https://"):
        urls.append(old)
    urls.extend(news._image_from_article_page(article["url"]))
    for url in dict.fromkeys(urls):
        photo = news._save_real_photo(url)
        if photo and _image_is_good(photo, article):
            return photo
    return ""


def _hide_placeholder_picture(markup):
    # The text-only card keeps its headline, category, link and update status.
    parts = re.split(r'(?=<a class="wl-story" href=)', markup)
    for i, part in enumerate(parts):
        if re.search(r'assets/news/slot-\d+-no-update\.svg', part):
            part = re.sub(
                r'<div class="wl-photo"><img\s+[^>]*src="assets/news/slot-\d+-no-update\.svg"[^>]*></div>',
                "", part, count=1,
            )
            part = part.replace('<a class="wl-story" ', '<a class="wl-story" style="grid-template-columns:1fr" ', 1)
            parts[i] = part
    return "".join(parts)


_original_homepage_panel = news.homepage_panel
_original_render = news.render


def _clean_homepage(*args, **kwargs):
    return _hide_placeholder_picture(_original_homepage_panel(*args, **kwargs))


def _clean_article_page(*args, **kwargs):
    result = _original_render(*args, **kwargs)
    return re.sub(r'<img class="story-photo" src="assets/news/slot-\d+-no-update\.svg"[^>]*>', '', result)


def main():
    news._complete_photo = _photo_with_quality
    news.homepage_panel = _clean_homepage
    news.render = _clean_article_page
    try:
        if "--check" in sys.argv:
            news.offline_self_check()
            print("PHOTO QUALITY PATCH: ready; existing photo, placeholder and layout hooks set")
        else:
            news.main()
    finally:
        QUALITY_CACHE.write_text(json.dumps(_quality, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
