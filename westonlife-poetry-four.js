/* Weston Life · 诗词里的中国 · 2026-11-14 第四首更新
   仅更新首页 #china-poems 栏目，不动其他首页新闻、计数器、语言系统或文章。
*/
(function () {
  'use strict';
  function updatePoetryCard() {
    var card = document.getElementById('china-poems');
    if (!card) return;
    var cover = card.querySelector('img');
    if (cover) {
      cover.src = '/assets/taoyuanming-cover.jpg';
      cover.alt = '陶渊明采菊东篱下、南山菊花田园诗画';
      cover.style.objectFit = 'contain';
      cover.style.background = '#f7f3ea';
    }
    var title = card.querySelector('h2');
    if (title) title.textContent = '诗词里的中国';
    var english = card.querySelector('h3');
    if (english) english.textContent = 'China in 100 Poems';
    var notice = document.getElementById('wl-poetry-four-notice');
    if (!notice) {
      notice = document.createElement('p');
      notice.id = 'wl-poetry-four-notice';
      notice.setAttribute('aria-label', '今日诗词更新');
      notice.style.cssText = 'font-size:19px;line-height:1.7;font-weight:bold;color:#8b2929;background:#fff0df;border:1px solid #e4d0ba;border-radius:9px;padding:12px 18px;margin:19px auto;max-width:540px';
      notice.textContent = '今日更新 · 第四首《饮酒（其五）》｜陶渊明';
      if (english) english.insertAdjacentElement('afterend', notice);
      else if (title) title.insertAdjacentElement('afterend', notice);
      else card.insertBefore(notice, card.firstChild);
    }
    var allLinks = card.querySelectorAll('a');
    for (var i = 0; i < allLinks.length; i++) {
      var link = allLinks[i];
      var href = link.getAttribute('href') || '';
      if (href.indexOf('poetry.html') !== -1) {
        link.href = '/poetry.html#fourth';
        link.textContent = '进入《诗词里的中国》· 学习第四首 →';
      } else if (href.indexOf('qibushi.html') !== -1) {
        link.href = '/poetry.html#fourth';
        link.textContent = '今日第四首：陶渊明《饮酒（其五）》 →';
      }
    }
    if (cover) {
      var parent = cover.closest('a');
      if (parent) parent.href = '/poetry.html#fourth';
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', updatePoetryCard);
  else updatePoetryCard();
})();
