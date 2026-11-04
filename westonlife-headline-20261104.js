/* Weston Life 2026-11-04 headline only. No counter code. */
(function(){
  function mount(){
    var host=document.querySelector('#wl-auto');
    if(!host || document.getElementById('wl-election-headline-20261104')) return;
    var card=document.createElement('a');
    card.id='wl-election-headline-20261104';
    card.href='/news/election-accounts-2026.html';
    card.setAttribute('aria-label','竞选失败后，究竟有哪些帐要算？');
    card.innerHTML='<img src="/assets/trump-musk-editorial.png" alt="特朗普与马斯克乘坐飞机的政治讽刺插画；非真实事件照片" loading="eager">'+
      '<div class="wl-election-text"><span class="wl-election-kicker">NOVEMBER 4, 2026 · TOP STORY / 今日头条</span>'+
      '<h2 class="wl-election-zh">竞选失败后，究竟有哪些帐要算？</h2>'+
      '<h2 class="wl-election-en">After the Election Defeat, What Accounts Remain to Be Settled?</h2>'+
      '<p class="wl-election-zh">选举结果、特朗普的国会压力、马斯克的调查风险与华尔街的重新定价。</p>'+
      '<p class="wl-election-en">Election results, congressional scrutiny, Musk’s regulatory exposure, and the implications for Wall Street.</p>'+
      '<small>政治讽刺艺术创作 · 非真实航空事故照片 / Editorial illustration, not a real aviation incident</small></div>';
    var style=document.createElement('style');
    style.textContent='#wl-election-headline-20261104{display:block;max-width:1180px;margin:24px auto 30px;color:#222;background:#fff;border:1px solid #dedede;text-decoration:none;box-shadow:0 8px 30px #0000000b}#wl-election-headline-20261104 img{display:block;width:100%;height:auto;max-height:650px;object-fit:cover}#wl-election-headline-20261104 .wl-election-text{padding:clamp(18px,3vw,34px)}#wl-election-headline-20261104 .wl-election-kicker{font:700 12px Arial,sans-serif;letter-spacing:.12em;color:#a33b30}#wl-election-headline-20261104 h2{font:700 clamp(29px,4.5vw,54px)/1.2 Georgia,serif;margin:13px 0}#wl-election-headline-20261104 p{font:18px/1.7 Arial,sans-serif;margin:0 0 12px}#wl-election-headline-20261104 small{font:12px/1.5 Arial,sans-serif;color:#777}#wl-election-headline-20261104 .wl-election-en{display:none}html[data-wl-lang="en"] #wl-election-headline-20261104 .wl-election-zh{display:none}html[data-wl-lang="en"] #wl-election-headline-20261104 .wl-election-en{display:block}';
    document.head.appendChild(style);
    var target=host.querySelector('.wl-breaking');
    if(target) target.parentNode.insertBefore(card,target); else host.insertBefore(card,host.firstChild);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();

/* Weston Life language-only repair, 2026-11-04. Counter untouched. */
(function(){
  function sync(lang){
    lang=lang==='en'?'en':'zh';
    document.documentElement.setAttribute('data-wl-lang',lang);
    document.documentElement.lang=lang==='en'?'en':'zh-CN';
    document.querySelectorAll('[data-wl-choice]').forEach(function(b){
      b.classList.toggle('active',b.getAttribute('data-wl-choice')===lang);
      b.setAttribute('aria-pressed',String(b.getAttribute('data-wl-choice')===lang));
    });
    try{localStorage.setItem('westonlife-lang',lang)}catch(e){}
  }
  function init(){
    var css=document.createElement('style');
    css.textContent='html[data-wl-lang="en"] #wl-election-headline-20261104 .wl-election-zh{display:none!important}html[data-wl-lang="en"] #wl-election-headline-20261104 .wl-election-en{display:block!important}html[data-wl-lang="zh"] #wl-election-headline-20261104 .wl-election-en{display:none!important}html[data-wl-lang="zh"] #wl-election-headline-20261104 .wl-election-zh{display:block!important}';
    document.head.appendChild(css);
    document.addEventListener('click',function(e){
      var b=e.target.closest&&e.target.closest('[data-wl-choice]');
      if(!b)return;
      var lang=b.getAttribute('data-wl-choice');
      setTimeout(function(){sync(lang)},0);
    });
    var lang='zh';try{lang=localStorage.getItem('westonlife-lang')||'zh'}catch(e){}
    sync(lang);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
