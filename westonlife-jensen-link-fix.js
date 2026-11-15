/* Weston Life Jensen link: direct official campaign URL plus Safari fallback.
   Changes only #wl-jensen-headline-20261114. Never touches visitor counter or poems.
   NOTE: Site JavaScript cannot repair a remote site's HTTPS/TLS handshake
   or force iOS in-app browsers to hand off links to the Safari app.
*/
(function () {
  'use strict';
  var URL = 'https://standwithjensen.com/';
  var SECTION_ID = 'wl-jensen-headline-20261114';
  function makeAnchor(a, text) {
    a.href = URL;
    a.removeAttribute('target');
    a.rel = 'noopener noreferrer';
    if (text) a.textContent = text;
  }
  function update() {
    var section = document.getElementById(SECTION_ID);
    if (!section) return;
    var existing = section.querySelector('a.wl-jensen-link');
    if (existing) makeAnchor(existing, '进入 Stand with Jensen 联名签署 →');
    var gallery = section.querySelector('.wl-jensen-images');
    if (gallery && !document.getElementById('wl-jensen-direct-sign')) {
      var entry = document.createElement('a');
      entry.id = 'wl-jensen-direct-sign';
      entry.className = 'wl-jensen-link';
      makeAnchor(entry, '进入联名签署网站 · Sign the letter →');
      gallery.parentNode.insertBefore(entry, gallery);
    }
    var heading = section.querySelector('h2');
    if (heading) {
      var headLink = heading.querySelector('a');
      if (!headLink) {
        headLink = document.createElement('a');
        headLink.textContent = heading.textContent;
        headLink.style.cssText = 'color:inherit;text-decoration:none';
        heading.textContent = '';
        heading.appendChild(headLink);
      }
      makeAnchor(headLink);
    }
    if (!document.getElementById('wl-jensen-safari-help')) {
      var note = document.createElement('div');
      note.id = 'wl-jensen-safari-help';
      note.style.cssText = 'background:#15283b;color:#e9f2f6;border:1px solid #506477;border-radius:8px;padding:12px 14px;margin:10px 0 20px;font:14px/1.7 Arial,sans-serif';
      note.innerHTML = '<p style="margin:0 0 8px">如果手机内置浏览器提示「无法建立安全连接」，可复制网址，在 Safari 中单独打开：</p>' +
        '<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center">' +
        '<input aria-label="签署网站地址" readonly value="https://standwithjensen.com/" style="min-width:180px;flex:1;background:#fff;color:#182b3b;padding:10px;border:0;border-radius:5px;font:14px Arial,sans-serif" />' +
        '<button type="button" style="background:#a4d94a;color:#17230b;border:0;border-radius:5px;padding:10px 15px;font-weight:bold;cursor:pointer">复制网址 · Copy</button></div>' +
        '<p style="font-size:12px;color:#b7ccd9;margin:8px 0 0">这是第三方独立联名签署页面，非 NVIDIA 官方股东投票。无法建立安全连接时，请勿忽略安全警告。</p>';
      var btn = note.querySelector('button');
      btn.addEventListener('click', function () {
        function status(ok) {btn.textContent = ok ? '已复制，打开 Safari 粘贴网址' : '请长按左侧网址复制';}
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(URL).then(function(){status(true)},function(){status(false)});
        } else {
          var field = note.querySelector('input');
          field.focus(); field.select();
          var ok = false;
          try {ok = document.execCommand('copy');}catch(e){}
          status(ok);
        }
      });
      var entry = document.getElementById('wl-jensen-direct-sign');
      if (entry) entry.insertAdjacentElement('afterend', note);
      else if (gallery) gallery.parentNode.insertBefore(note, gallery);
      else section.appendChild(note);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', update, {once:true});
  else update();
})();
