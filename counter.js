/* Weston Life shared visitor counter. Independent module. */
(function () {
  'use strict';
  if (window.__westonlifeSharedCounterLoaded) return;
  window.__westonlifeSharedCounterLoaded = true;
  const KEY = 'westonlife_org_global_visits_20261108_30082_v1';
  const BASE = 30071; // First successful hit returns 1, displays 30082.
  const ENDPOINT = 'https://countapi.mileshilliard.com/api/v1/';
  function init() {
    document.querySelectorAll('#wl-counter-28885, #wl-counter, #wl-popularity').forEach(el => { el.style.setProperty('display','none','important'); });
    let el = document.getElementById('westonlife-global-counter');
    if (!el) {
      el = document.createElement('div');
      el.id = 'westonlife-global-counter';
      el.setAttribute('aria-label', 'Weston Life shared visitor count');
      document.body.appendChild(el);
    }
    el.style.cssText = 'position:fixed;top:5px;left:5px;z-index:2147483647;background:transparent;border:0;box-shadow:none;color:#315c41;padding:3px 5px;font:600 13px Arial,sans-serif;pointer-events:none;';
    el.textContent = '人气值：读取中…';
    fetch(ENDPOINT + 'hit/' + KEY, {cache:'no-store'})
      .then(r => {if(!r.ok) throw Error('HTTP '+r.status);return r.json();})
      .then(data => {if(!Number.isSafeInteger(Number(data.value))) throw Error('Invalid counter'); el.textContent = '人气值：' + (BASE + 11*Number(data.value)).toLocaleString('en-US');})
      .catch(() => {
        fetch(ENDPOINT + 'get/' + KEY, {cache:'no-store'})
          .then(r => {if(!r.ok) throw Error('Unavailable');return r.json();})
          .then(data => {el.textContent = '人气值：' + (BASE + 11*Number(data.value)).toLocaleString('en-US');})
          .catch(() => {el.textContent = '人气值：暂不可用';});
      });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();
