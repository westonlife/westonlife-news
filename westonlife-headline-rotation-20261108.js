/* Rotates existing headline and existing Top Stories every 8 seconds.
   Read-only for news content. Does not touch visitor counter or storage. */
(function () {
  'use strict';
  function init() {
    var fixed = document.getElementById('wl-market-headline-20261106');
    var news = document.getElementById('wl-auto');
    if (!news || document.getElementById('wl-rotating-headline-2026')) return;
    var top = Array.prototype.slice.call(news.querySelectorAll('.wl-features > a.wl-feature'));
    if (!top.length) return;
    var items = [];
    if (fixed) items.push({href:fixed.getAttribute('href'),img:fixed.querySelector('img')?.getAttribute('src'),zh:fixed.querySelector('.wl-market-zh')?.textContent,en:fixed.querySelector('.wl-market-en')?.textContent,source:'WESTON LIFE · FEATURE'});
    top.forEach(function (a) {items.push({href:a.getAttribute('href'),img:a.querySelector('img')?.getAttribute('src'),zh:a.querySelector('.wl-feature-zh')?.textContent,en:a.querySelector('.wl-feature-en')?.textContent,source:a.querySelector('small')?.textContent||'TOP STORY'});});
    if (items.length < 2) return;
    var css=document.createElement('style');css.textContent='#wl-rotating-headline-2026{display:block;max-width:1180px;margin:24px auto;background:white;border:1px solid #ded8cb;color:#263b30;text-decoration:none}#wl-rotating-headline-2026 img{display:block;width:100%;height:clamp(210px,36vw,460px);object-fit:cover}#wl-rotating-headline-2026 .wl-r-body{padding:20px 25px}#wl-rotating-headline-2026 h2{font:700 clamp(24px,4vw,40px)/1.25 Georgia,serif;margin:10px 0}#wl-rotating-headline-2026 small{color:#8b5637;font:12px Arial,sans-serif}#wl-rotating-headline-2026 .wl-r-en{display:none}html[data-wl-lang="en"] #wl-rotating-headline-2026 .wl-r-zh{display:none}html[data-wl-lang="en"] #wl-rotating-headline-2026 .wl-r-en{display:block}#wl-rotating-headline-controls{display:flex;justify-content:center;align-items:center;gap:16px;margin:-14px auto 18px}#wl-rotating-headline-controls button{border:1px solid #b7c4b4;background:white;border-radius:8px;padding:7px 15px;cursor:pointer;color:#31533e}';document.head.appendChild(css);
    var a=document.createElement('a');a.id='wl-rotating-headline-2026';a.setAttribute('aria-label','Rotating top news');
    a.innerHTML='<img alt="新闻头条配图"><div class="wl-r-body"><small></small><h2 class="wl-r-zh"></h2><h2 class="wl-r-en"></h2></div>';
    var controls=document.createElement('div');controls.id='wl-rotating-headline-controls';controls.innerHTML='<button type="button" data-step="-1" aria-label="Previous headline">‹ 上一条</button><span aria-live="off"></span><button type="button" data-step="1" aria-label="Next headline">下一条 ›</button>';
    var target=fixed||news.querySelector('.wl-breaking');if(!target)return;target.parentNode.insertBefore(a,target);a.insertAdjacentElement('afterend',controls);
    if(fixed)fixed.style.display='none';
    var i=0,paused=false;
    function show(){var d=items[i];a.href=d.href||'#';a.querySelector('img').src=d.img||'';a.querySelector('small').textContent=d.source;a.querySelector('.wl-r-zh').textContent=d.zh||d.en||'';a.querySelector('.wl-r-en').textContent=d.en||d.zh||'';controls.querySelector('span').textContent=(i+1)+' / '+items.length;}
    controls.addEventListener('click',function(e){var b=e.target.closest('button[data-step]');if(!b)return;i=(i+Number(b.dataset.step)+items.length)%items.length;show();});
    [a,controls].forEach(function(n){n.addEventListener('mouseenter',function(){paused=true});n.addEventListener('mouseleave',function(){paused=false});n.addEventListener('focusin',function(){paused=true});n.addEventListener('focusout',function(){paused=false});});
    document.addEventListener('visibilitychange',function(){paused=document.hidden});
    show();setInterval(function(){if(!paused){i=(i+1)%items.length;show();}},8000);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
