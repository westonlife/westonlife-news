// Weston Life / fixed two-day headline / no changes to existing news feeds
(function(){
  'use strict';
  if (document.getElementById('wl-learjet-headline-2026')) return;
  var expire = Date.parse('2026-11-04T00:00:00-05:00'); // 11/2 + 11/3 Boston dates
  if (Date.now() >= expire) return;
  var title='赴巴哈马途中坠毁，9人遇难：一架22年机龄的Learjet 60，在结冰与乱流中发出最后爬升请求';
  var intro='11月1日，一架从美国飞往巴哈马的 Learjet 60 在佛罗里达坠毁，机上9人全部遇难。飞机已有22年机龄，机组失事前报告结冰、乱流与降水，并提出最后一次爬升请求。事故原因仍待官方调查。';
  function safe(t){var e=document.createElement('span');e.textContent=t;return e.innerHTML;}
  function install(){
    if (Date.now() >= expire) return true;
    if (document.getElementById('wl-learjet-headline-2026')) return true;
    var panel=document.getElementById('wl-auto');
    if (!panel) return false;
    // Insert immediately before existing breaking news / news columns without changing or deleting them.
    var next=panel.querySelector('.wl-breaking, .wl-columns, .wl-news-grid, .wl-news-list, .wl-stories');
    if (!next) return false;
    var style=document.createElement('style');style.id='wl-learjet-headline-style';
    style.textContent='#wl-learjet-headline-2026{max-width:1120px;margin:20px auto 24px;padding:18px;background:#fffdf8;border-top:5px solid #a56151;box-shadow:0 7px 20px #253e3014;font-family:Georgia,"Songti SC",serif;box-sizing:border-box} #wl-learjet-headline-2026 *{box-sizing:border-box} #wl-learjet-headline-2026 .wlh-flex{display:grid;grid-template-columns:minmax(210px,35%) 1fr;gap:22px;align-items:center} #wl-learjet-headline-2026 img{width:100%;height:230px;object-fit:cover;border-radius:8px;display:block} #wl-learjet-headline-2026 h2{font-size:clamp(22px,3vw,32px);line-height:1.45;color:#214734;margin:12px 0} #wl-learjet-headline-2026 p{font-size:15px;line-height:1.75;color:#5f665f} #wl-learjet-headline-2026 a{text-decoration:none;color:inherit;display:block} #wl-learjet-headline-2026 .wlh-tag{font:700 12px Arial,sans-serif;color:#ad5c4b;letter-spacing:.08em} #wl-learjet-headline-2026 .wlh-more{font:700 14px Arial,sans-serif;color:#1f694b} #wl-learjet-headline-2026 .wlh-credit{font:11px Arial,sans-serif;color:#75746a} @media(max-width:680px){#wl-learjet-headline-2026 .wlh-flex{grid-template-columns:1fr} #wl-learjet-headline-2026 img{height:auto;max-height:300px}}';
    document.head.appendChild(style);
    var card=document.createElement('section');card.id='wl-learjet-headline-2026';
    card.innerHTML='<div class="wlh-flex"><a href="/news/news-2026-11-01-learjet-bahamas-crash.html" aria-label="点击阅读全文"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Lear_Jet_60.jpg/1280px-Lear_Jet_60.jpg" alt="Learjet 60同型号真实资料照片，非事故机" loading="eager"><div class="wlh-credit">同型号资料图 · CoZiegler / CC BY-SA 4.0</div></a><a href="/news/news-2026-11-01-learjet-bahamas-crash.html"><div class="wlh-tag">重大新闻 · TOP STORY · 11月2—3日</div><h2>'+safe(title)+'</h2><p>'+safe(intro)+'</p><span class="wlh-more">阅读全文 / Read full story →</span></a></div>';
    next.parentNode.insertBefore(card,next);
    return true;
  }
  if(install())return;
  var ob=new MutationObserver(function(){if(install())ob.disconnect();});
  ob.observe(document.documentElement,{childList:true,subtree:true});
  document.addEventListener('DOMContentLoaded',install);
  window.addEventListener('load',install);
})();
