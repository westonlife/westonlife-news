/* Weston Life poetry rotation. Only changes the poetry sections. */
(function () {
  'use strict';
  const raw = 'https://raw.githubusercontent.com/westonlife/westonlife-news/main/poetry-auto/';
  const cache = '?v=' + Math.floor(Date.now() / 300000);
  async function getJSON(name) {
    const r = await fetch(raw + name + cache, { cache: 'no-store' });
    if (!r.ok) throw new Error(name + ': HTTP ' + r.status);
    return r.json();
  }
  function el(tag, text) { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; return n; }
  function link(title, href) { const a = el('a', title); a.href = href; return a; }
  function homepage(item) {
    const root = document.getElementById('china-poems');
    if (!root) return;
    const existing = root.querySelector('img');
    if (existing && item.cover) { existing.src = item.cover; existing.alt = '第' + item.number + '首《' + item.title + '》'; }
    let latest = root.querySelector('#poetry-latest-current');
    if (!latest) { latest = el('div'); latest.id = 'poetry-latest-current'; latest.style.cssText = 'margin:18px auto;font-size:21px;font-weight:600;color:#8b2929'; const image = root.querySelector('img'); if (image) image.insertAdjacentElement('afterend', latest); else root.prepend(latest); }
    latest.replaceChildren(link('最新发布：第' + item.number + '首《' + item.title + '》', item.url));
    const old = root.querySelector('a[href="/qibushi.html"]');
    if (old) { old.textContent = '阅读最新诗歌：第' + item.number + '首《' + item.title + '》 →'; old.href = item.url; }
  }
  function archive(items) {
    if (!location.pathname.endsWith('/poetry.html')) return;
    let root = document.getElementById('poetry-auto-archive');
    if (!root) { root = el('section'); root.id = 'poetry-auto-archive'; root.style.cssText = 'max-width:900px;margin:35px auto;padding:20px;background:#fffaf2;border-radius:12px'; document.body.append(root); }
    root.replaceChildren(el('h2', '最新发布与历史诗歌'));
    for (const item of items) {
      const p = el('p'); p.style.cssText = 'padding:12px 0;border-bottom:1px solid #ddd';
      p.append(link('第' + item.number + '首《' + item.title + '》 · ' + (item.author || '') + ' · ' + (item.release_date || ''), item.url));
      root.append(p);
    }
  }
  function paragraph(parent, label, value) { if (!value) return; parent.append(el('h2', label)); const p = el('p', value); p.style.whiteSpace = 'pre-line'; parent.append(p); }
  function audio(parent, label, url) { if (!url) return; parent.append(el('h2', label)); const player = el('audio'); player.controls = true; player.preload = 'none'; player.src = url; parent.append(player); }
  async function detail() {
    const host = document.getElementById('item'); if (!host) return;
    const n = Number(new URLSearchParams(location.search).get('n'));
    if (!Number.isInteger(n) || n < 6 || n > 100) { host.textContent = '诗歌编号无效。'; return; }
    const item = await getJSON('data/' + String(n).padStart(3, '0') + '.json');
    document.title = '第' + n + '首《' + item.title + '》｜诗词里的中国';
    const heading = document.getElementById('title'); if (heading) heading.textContent = item.title;
    host.replaceChildren();
    if (item.cover) { const pic = el('img'); pic.src = item.cover; pic.alt = '《' + item.title + '》原书插画'; pic.className = 'cover'; host.append(pic); }
    const verse = el('div', item.poem_text || ''); verse.className = 'panel verse'; host.append(verse);
    const author = el('p', item.author || ''); author.className = 'sub'; host.append(author);
    audio(host, '诗歌朗诵', item.recitation);
    paragraph(host, '白话译文', item.translation);
    paragraph(host, '作者与创作背景', item.background);
    paragraph(host, '赏析', item.analysis);
    audio(host, '完整讲解朗诵', item.explanation);
  }
  async function start() {
    try {
      if (document.getElementById('item')) { await detail(); return; }
      const item = await getJSON('latest.json'); homepage(item);
      if (location.pathname.endsWith('/poetry.html')) archive(await getJSON('archive.json'));
    } catch (e) { console.error('Poetry auto-display error:', e); const host = document.getElementById('item'); if (host) host.textContent = '诗歌暂时无法加载，请稍后刷新。'; }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
