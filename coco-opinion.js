/* Coco Opinion - permanent editorial block, independent from daily news. */
(function(){
  function mount(){
    if(document.getElementById('coco-editorial-2026')) return;
    var style=document.createElement('style');style.textContent='#coco-editorial-2026{max-width:1180px;margin:30px auto;padding:16px;background:#fffaf5;border-top:5px solid #9e0019;border-bottom:1px solid #ddd}#coco-editorial-2026 img{display:block;width:100%;height:auto;border-radius:8px}#coco-editorial-2026 h2{color:#a50017!important;font:bold clamp(25px,4.5vw,46px)/1.3 Georgia,serif!important;margin:14px 0}#coco-editorial-2026 a{text-decoration:none}#coco-editorial-2026 p{color:#555}';document.head.appendChild(style);
    var panel=document.createElement('section');panel.id='coco-editorial-2026';panel.innerHTML='<p style="font-weight:bold;letter-spacing:2px;color:#8b1425">可可豆子的观点 ♡ · COCO’S PERSPECTIVE</p><a href="/coco-ukraine-2026.html"><img src="/assets/coco_ukraine_cover.png" alt="可可豆子俄乌战争观点封面"><h2>俄乌战争：一场关于历史、领土与国家命运的战争</h2></a><p>2026年10月23日 · 历史、俄罗斯与乌克兰、特朗普与美国立场 · <a href="/coco-ukraine-2026.html">阅读全文 →</a>　<a href="/coco-opinions.html">历年观点档案 →</a></p>';
    var school=document.querySelector('#wl-school, #coco-college, #weston-college, [id*="school"]');
    if(school&&school.parentNode){school.parentNode.insertBefore(panel,school);return;}
    var travel=Array.from(document.querySelectorAll('h1,h2,h3,p')).find(e=>/WESTON LIFE.*COMMUNITY STORIES|旅游专家|跋涉山水/i.test(e.textContent||''));
    if(travel){travel.parentNode.insertBefore(panel,travel);return;}
    var news=document.querySelector('#wl-auto, #daily-news, #news-archive');
    if(news){news.insertAdjacentElement('afterend',panel);return;}
    document.body.appendChild(panel);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();