/* Weston Life | Confirmed 2026-11-14 FAA headline photo placement.
   - Keeps the original aviation article untouched.
   - Removes the misplaced top-of-page FAA banner when present.
   - Adds the confirmed FAA title and two original article photos as home story #1.
   - Moves the existing three-screenshot Jensen signing section to home story #2.
   - Never reads or modifies counters or pre-existing stories.
*/
(function () {
  'use strict';

  var ARTICLE_URL = 'faa-ground-stop-2026-11-14-westonlife.html';
  var CONFIRMED_TITLE = '美国航班大面积停飞，原因究竟是什么？AI替代人工、人为因素，还是软件系统老旧？';
  var CONFIRMED_DECK = '官方解释指向通信系统故障，但故障背后的技术、管理和成本因素仍值得追问。AI应用、人工操作与系统老化，究竟哪些有证据支持？';
  var FAA_ID = 'wl-faa-confirmed-top-story-20261114';
  var JENSEN_ID = 'wl-jensen-headline-20261114';

  function init() {
    var area = document.querySelector('#wl-auto .wl-breaking .wl-features');
    if (!area) return;

    // Remove only the incorrectly positioned dark banner from the old placement.
    Array.prototype.forEach.call(document.querySelectorAll('body > a[href="' + ARTICLE_URL + '"]'), function (node) {
      if (node.querySelector('div') && node.textContent.indexOf('美国航空大面积停飞') !== -1) {
        node.parentNode.removeChild(node);
      }
    });

    var style = document.createElement('style');
    style.textContent = '\n' +
      '#wl-auto .wl-features>#' + FAA_ID + '{grid-column:1/-1;display:block;padding:17px 20px;background:#fff;color:#283b30;border:2px solid #d8be9b;border-radius:11px;text-decoration:none;}' +
      '#wl-auto #' + FAA_ID + ':hover{background:#fff9ef;}' +
      '#wl-auto #' + FAA_ID + ' .wl-faa-title{font:700 clamp(23px,3.5vw,36px)/1.38 Georgia,"PingFang SC","Microsoft YaHei",serif;margin:7px 0 11px;display:block;color:#203b34;}' +
      '#wl-auto #' + FAA_ID + ' .wl-faa-deck{display:block;font:15px/1.7 Arial,"PingFang SC",sans-serif;color:#516457;}' +
      '#wl-auto #' + FAA_ID + ' .wl-faa-photos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:15px 0 6px;}' +
      '#wl-auto #' + FAA_ID + ' .wl-faa-photos img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block;border-radius:8px;}' +
      '#wl-auto #' + FAA_ID + ' .wl-faa-meta{display:block;font:13px Arial,sans-serif;margin:10px 0 2px;color:#6b746b;}' +
      '#wl-auto #' + JENSEN_ID + '{grid-column:1/-1;max-width:none;width:100%;margin:0 0 8px;}' +
      '@media(max-width:720px){#wl-auto .wl-features>#' + FAA_ID + '{padding:13px;}#wl-auto #' + FAA_ID + ' .wl-faa-photos{gap:8px;}}';
    document.head.appendChild(style);

    var card = document.getElementById(FAA_ID);
    if (!card) {
      card = document.createElement('a');
      card.className = 'wl-feature';
      card.id = FAA_ID;
      card.href = ARTICLE_URL;
      card.setAttribute('aria-label', CONFIRMED_TITLE + '。点击阅读完整报道');

      var rank = document.createElement('span');
      rank.className = 'wl-feature-rank';
      rank.textContent = '01 · TOP STORY · WESTON LIFE 深度调查与整理';
      card.appendChild(rank);

      var title = document.createElement('strong');
      title.className = 'wl-faa-title';
      title.textContent = CONFIRMED_TITLE;
      card.appendChild(title);

      var deck = document.createElement('span');
      deck.className = 'wl-faa-deck';
      deck.textContent = CONFIRMED_DECK;
      card.appendChild(deck);

      var photos = document.createElement('span');
      photos.className = 'wl-faa-photos';
      photos.setAttribute('aria-label', '原定的两张新闻照片');
      card.appendChild(photos);

      var meta = document.createElement('small');
      meta.className = 'wl-faa-meta';
      meta.textContent = 'Weston Life · 2026-11-14 · 点击查看完整报道';
      card.appendChild(meta);
      area.insertBefore(card, area.firstChild);
    }

    // The Jensen section was already assembled with the exact three uploaded screenshots.
    // Move it into the existing news section without editing its screenshots or link.
    var jensen = document.getElementById(JENSEN_ID);
    if (jensen && jensen.previousElementSibling !== card) {
      area.insertBefore(jensen, card.nextSibling);
    }

    // Reuse images actually embedded in the approved detailed article; no new photo lookup.
    var grid = card.querySelector('.wl-faa-photos');
    if (!grid || grid.children.length) return;
    fetch(ARTICLE_URL, { credentials: 'same-origin' }).then(function (response) {
      if (!response.ok) throw new Error('Article fetch status ' + response.status);
      return response.text();
    }).then(function (markup) {
      var page = new DOMParser().parseFromString(markup, 'text/html');
      var sources = page.querySelectorAll('.xueshang-news-story .xs-photos figure img');
      if (sources.length !== 2) throw new Error('Expected two original article images');
      Array.prototype.forEach.call(sources, function (source) {
        var image = document.createElement('img');
        image.src = source.getAttribute('src');
        image.alt = source.getAttribute('alt') || '原定报道照片';
        image.decoding = 'async';
        image.loading = 'eager';
        grid.appendChild(image);
      });
    }).catch(function (err) {
      console.warn('Weston Life: unable to display original aviation photos:', err);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
