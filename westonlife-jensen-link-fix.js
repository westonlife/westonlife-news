/* Weston Life: direct same-tab link to Stand with Jensen signature page.
   Scoped to the Jensen headline section. No counter or other content changes.
*/
(function () {
  'use strict';
  var DESTINATION = 'https://standwithjensen.com/';
  function fixJensenLinks() {
    var section = document.getElementById('wl-jensen-headline-20261114');
    if (!section) return;

    // The original link is after the photos. Keep it, but make it a direct visit.
    var existing = section.querySelector('a.wl-jensen-link');
    if (existing) {
      existing.href = DESTINATION;
      existing.removeAttribute('target');
      existing.rel = 'noopener noreferrer';
      existing.textContent = '进入联名签署页面 · Sign the letter →';
    }

    // Put a prominent entry ahead of the gallery for mobile readers.
    var gallery = section.querySelector('.wl-jensen-images');
    if (gallery && !document.getElementById('wl-jensen-direct-sign')) {
      var callToAction = document.createElement('a');
      callToAction.id = 'wl-jensen-direct-sign';
      callToAction.className = 'wl-jensen-link';
      callToAction.href = DESTINATION;
      callToAction.rel = 'noopener noreferrer';
      callToAction.textContent = '点击进入联名签署 · Sign the letter →';
      gallery.parentNode.insertBefore(callToAction, gallery);
    }

    // The headline also becomes a link without replacing any news content.
    var title = section.querySelector('h2');
    if (title && !title.querySelector('a')) {
      var titleLink = document.createElement('a');
      titleLink.href = DESTINATION;
      titleLink.rel = 'noopener noreferrer';
      titleLink.style.cssText = 'color:inherit;text-decoration:none';
      titleLink.textContent = title.textContent;
      title.textContent = '';
      title.appendChild(titleLink);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fixJensenLinks, {once:true});
  } else {
    fixJensenLinks();
  }
})();
