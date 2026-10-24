/* Weston Life | Coco's Coffee | France 2026 | preserved Russia archive */
(function(){
  function mount(){
    if(document.getElementById('coco-editorial-2026')) return;
    var style=document.createElement('style');
    style.textContent=`
    #coco-editorial-2026{max-width:1180px;margin:36px auto;padding:22px;background:#fffaf5;border-top:5px solid #984144;border-bottom:1px solid #e1d7ca;color:#34443b;box-sizing:border-box;font-family:Georgia,"Noto Serif SC",serif}
    #coco-editorial-2026 *{box-sizing:border-box}
    #coco-editorial-2026 .coco-kicker{font:700 13px/1.6 Arial,sans-serif;letter-spacing:.11em;color:#8b3b36;margin:0 0 16px}
    #coco-editorial-2026 .coco-grid{display:grid;grid-template-columns:minmax(0,3fr) minmax(210px,1fr);gap:24px}
    #coco-editorial-2026 a{text-decoration:none;color:inherit}
    #coco-editorial-2026 a:hover{text-decoration:underline}
    #coco-editorial-2026 .coco-main img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:8px}
    #coco-editorial-2026 h2{color:#983d3b!important;font:500 clamp(27px,4vw,45px)/1.3 Georgia,"Noto Serif SC",serif!important;margin:16px 0 9px!important}
    #coco-editorial-2026 p{font-size:15px;line-height:1.7;color:#5b5e55;margin:8px 0}
    #coco-editorial-2026 .coco-portrait{display:block;width:100%;max-height:255px;object-fit:cover;object-position:top;border-radius:8px}
    #coco-editorial-2026 .coco-archive-label{font:700 14px Arial,sans-serif;color:#7f503e;margin:14px 0 7px}
    #coco-editorial-2026 .coco-old{display:block;padding:13px 12px;background:#f2eadf;border-radius:8px;font:14px/1.6 Arial,sans-serif!important;color:#465444!important}
    #coco-editorial-2026 .coco-all{display:block;margin-top:14px;color:#91423e;font:13px Arial,sans-serif;text-decoration:underline}
    #coco-editorial-2026 .coco-credit{font:11px/1.6 Arial,sans-serif;color:#8b857b;margin-top:6px}
    @media(max-width:720px){#coco-editorial-2026{margin:22px 12px;padding:15px}#coco-editorial-2026 .coco-grid{grid-template-columns:1fr}#coco-editorial-2026 .coco-aside{display:grid;grid-template-columns:105px 1fr;column-gap:13px}#coco-editorial-2026 .coco-portrait{height:135px;grid-row:span 3}#coco-editorial-2026 .coco-archive-label{margin:0}#coco-editorial-2026 .coco-old{align-self:start}#coco-editorial-2026 .coco-all{grid-column:1/-1}}
    `;
    document.head.appendChild(style);
    var panel=document.createElement('section');panel.id='coco-editorial-2026';
    panel.setAttribute('aria-label','可可豆子的咖啡');
    panel.innerHTML=`<p class="coco-kicker">☕ 可可豆子的咖啡 · COCO'S COFFEE</p>
    <div class="coco-grid">
      <article class="coco-main"><a href="/coco-france-2026.html">
        <img src="/assets/coco_france_hero.webp" alt="AI插画：法国游行示意图" loading="lazy">
        <h2>2026法国更大规模的游行：一场“饮鸩止渴”的社会困局</h2>
        </a><p>2026年10月24日 · 41万人走上街头：当教育、物价、税负与债务同时逼近财政边界。</p>
        <a style="color:#953f39;font-weight:bold" href="/coco-france-2026.html">阅读全文 →</a>
        <div class="coco-credit">封面为AI创作示意图，非现场实拍；新闻来源：Associated Press。</div>
      </article>
      <aside class="coco-aside"><img class="coco-portrait" src="/assets/coco_portrait_2026.webp" alt="可可豆子水彩头像" loading="lazy">
        <div class="coco-archive-label">历史第二篇 · 2026年10月23日</div>
        <a class="coco-old" href="/coco-ukraine-2026.html">俄乌战争：一场关于历史、领土与国家命运的战争 →</a>
        <a class="coco-all" href="/coco-opinions.html">查看全部历史文章 →</a>
      </aside>
    </div>`;
    var school=document.querySelector('#wl-school, #coco-college, #weston-college, [id*="school"]');
    if(school&&school.parentNode){school.parentNode.insertBefore(panel,school);return;}
    var travel=Array.from(document.querySelectorAll('h1,h2,h3,p')).find(e=>/WESTON LIFE.*COMMUNITY STORIES|旅游专家|跋涉山水/i.test(e.textContent||''));
    if(travel){travel.parentNode.insertBefore(panel,travel);return;}
    var news=document.querySelector('#wl-auto, #daily-news, #news-archive');
    if(news){news.insertAdjacentElement('afterend',panel);return;}
    document.body.appendChild(panel);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount); else mount();
})();
