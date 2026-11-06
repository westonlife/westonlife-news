/* Weston Life 2026-11-06 headline. Does not access counter or visitor storage. */
(function(){
 function mount(){
  var host=document.querySelector('#wl-auto');
  if(!host||document.getElementById('wl-market-headline-20261106'))return;
  var a=document.createElement('a');a.id='wl-market-headline-20261106';a.href='/market-article.html';
  a.innerHTML='<img src="/market-hero.svg" alt="美股下跌专题原创财经插画" loading="eager">'+
   '<div class="wl-market-headline-body"><small>2026-11-06 · TOP STORY / 今日头条</small>'+
   '<h2 class="wl-market-zh">美股黑色星期四：纳指暴跌5.5%，华尔街为何突然恐慌？</h2>'+
   '<h2 class="wl-market-en">Wall Street’s Black Thursday: Why Did the Nasdaq Plunge 5.5%?</h2>'+
   '<p class="wl-market-zh">从中期选举、人工智能估值到油价与利率，深度分析11月5日美股大跌的前因后果。</p>'+
   '<p class="wl-market-en">An in-depth look at the November 5 selloff, from election uncertainty and AI valuations to oil prices and interest rates.</p></div>';
  var style=document.createElement('style');style.textContent='#wl-market-headline-20261106{display:block;max-width:1180px;margin:24px auto 30px;color:#222;background:#fff;border:1px solid #dedede;text-decoration:none;box-shadow:0 8px 30px #0000000b}#wl-market-headline-20261106 img{display:block;width:100%;max-height:600px;object-fit:cover}#wl-market-headline-20261106 .wl-market-headline-body{padding:clamp(18px,3vw,34px)}#wl-market-headline-20261106 small{font:700 12px Arial,sans-serif;letter-spacing:.09em;color:#a33b30}#wl-market-headline-20261106 h2{font:700 clamp(28px,4.5vw,52px)/1.2 Georgia,serif;margin:13px 0}#wl-market-headline-20261106 p{font:18px/1.7 Arial,sans-serif}#wl-market-headline-20261106 .wl-market-en{display:none}html[data-wl-lang="en"] #wl-market-headline-20261106 .wl-market-zh{display:none!important}html[data-wl-lang="en"] #wl-market-headline-20261106 .wl-market-en{display:block!important}';document.head.appendChild(style);
  var target=host.querySelector('.wl-breaking');if(target)target.parentNode.insertBefore(a,target);else host.insertBefore(a,host.firstChild);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();
/* Preserve the language-choice synchronization present in the 2026-11-04 headline script. */
(function(){
 function sync(lang){lang=lang==='en'?'en':'zh';document.documentElement.setAttribute('data-wl-lang',lang);document.documentElement.lang=lang==='en'?'en':'zh-CN';document.querySelectorAll('[data-wl-choice]').forEach(function(b){b.classList.toggle('active',b.getAttribute('data-wl-choice')===lang);b.setAttribute('aria-pressed',String(b.getAttribute('data-wl-choice')===lang));});try{localStorage.setItem('westonlife-lang',lang)}catch(e){}}
 function init(){document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-wl-choice]');if(!b)return;var lang=b.getAttribute('data-wl-choice');setTimeout(function(){sync(lang)},0);});var lang='zh';try{lang=localStorage.getItem('westonlife-lang')||'zh'}catch(e){}sync(lang);}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
