/* Weston Life: add Tesla Cybercab as third TOP STORIES feature only.
   No visitor counter, poetry, Jensen, or other homepage logic is altered. */
(function () {
  'use strict';
  var CARD_ID = 'wl-robotaxi-feature-20261114';
  function install() {
    if (document.getElementById(CARD_ID)) return;
    var grid = document.querySelector('#wl-auto .wl-features');
    if (!grid) return;
    var existing = grid.querySelectorAll('a.wl-feature');
    if (existing.length < 2) return;
    var card = document.createElement('a');
    card.id = CARD_ID;
    card.className = 'wl-feature';
    card.href = 'robotaxi-cybercab-2026-11-14.html';
    card.setAttribute('aria-label', '马斯克 Robotaxi 开售，阅读全文');
    card.innerHTML = '<img src="assets/news/musk-robotaxi-20261114.png" alt="金色 Cybercab：Tesla Robotaxi 科技新闻主题插图" loading="eager">' +
      '<span class="wl-feature-rank">03 · TECH STORY</span>' +
      '<strong class="wl-feature-zh">马斯克 Robotaxi 开售：德州率先试水，1000 美元定金</strong>' +
      '<strong class="wl-feature-en">Tesla Cybercab sales open to select customers: $1,000 deposit in Texas</strong>' +
      '<small>Weston Life · 2026-11-14</small>';
    /* Insert before the old third item, preserving all other cards. */
    grid.insertBefore(card, existing[2] || null);
    /* The old third card moves to the fourth position. */
    var oldThird = existing[2];
    if (oldThird) {
      var label = oldThird.querySelector('.wl-feature-rank');
      if (label && /^03\b/.test(label.textContent.trim())) {
        label.textContent = label.textContent.replace(/^03/, '04');
      }
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install, {once:true});
  else install();
  window.addEventListener('load', install, {once:true});
})();
