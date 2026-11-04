/* Weston Life counter: each browser starts at 28,885 and adds 11 per homepage load.
   Browser-local count, NOT a synchronized global total. */
(function () {
  'use strict';
  if (window.__wlCounter28885) return;
  window.__wlCounter28885 = true;
  var KEY = 'westonlife-popularity-28885-plus11-v1';
  var START = 28885;
  var STEP = 11;
  function run() {
    // Hide only the legacy counter, without changing articles or language controls.
    var legacy = document.getElementById('wl-counter');
    if (legacy) legacy.style.setProperty('display', 'none', 'important');
    var legacyLabel = document.getElementById('wl-popularity');
    if (legacyLabel && !legacy) {
      var parent = legacyLabel.parentElement;
      if (parent) parent.style.setProperty('display', 'none', 'important');
    }
    var display = document.getElementById('wl-counter-28885');
    if (!display) {
      display = document.createElement('div');
      display.id = 'wl-counter-28885';
      display.setAttribute('aria-live', 'polite');
      display.style.cssText = 'position:fixed;top:8px;left:8px;z-index:2147483647;background:#fffaf0;color:#315c41;border:1px solid #d9cbb0;border-radius:8px;padding:7px 11px;font:600 14px Arial,sans-serif;box-shadow:0 2px 8px #0002;pointer-events:none';
      document.body.appendChild(display);
    }
    var last = START - STEP;
    try {
      var stored = Number(localStorage.getItem(KEY));
      if (Number.isSafeInteger(stored) && stored >= START && stored < Number.MAX_SAFE_INTEGER - STEP) last = stored;
    } catch (_) {}
    var next = last + STEP;
    try { localStorage.setItem(KEY, String(next)); } catch (_) {}
    display.textContent = '人气值：' + next.toLocaleString('en-US');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, {once:true});
  else run();
})();
