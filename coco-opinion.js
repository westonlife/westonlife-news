/* Weston Life 2026-10-24: five requested homepage fixes. No login or tracking. */
(function(){
'use strict';
const LEAF={title:'Weston居民将表决燃油落叶吹风机限制提案',en:'Weston residents to vote on gas-powered leaf blower restrictions',date:'2026-10-23',source:'Weston Observer',url:'https://westonobserver.org/gas-leaf-blower-ban-proposed/',image:'https://dxy0ub64f43cw.cloudfront.net/wp-content/uploads/2026/10/22115615/TownGreenFall2025-1024x683.jpg'};
const EXTRAS=[
 {zh:'国际油价上涨拖累美股，标普500周五收低',en:'Wall Street loses ground under pressure from rising oil prices',src:'Associated Press',date:'2026-10-23',url:'https://apnews.com/article/7b47ef3b037bfba4e34f685329b9b963',img:'assets/news/527122470b35477633dec675.jpg'},
 {zh:'AI股票承压，全球股市与石油市场波动',en:'Sharp drops for AI stocks overwhelm markets worldwide as oil prices jump',src:'Associated Press',date:'2026-10-22',url:'https://apnews.com/article/33767691a4a0730b96d6f0c5100ea9b2',img:'assets/news/e3d1baa47312f39075e6f0dd.jpg'},
 {zh:'富途牛牛：10月22日隔夜市场与科技股消息',en:'Futu: Overnight market headlines and technology stocks',src:'富途牛牛 · 原文转载新浪财经',date:'2026-10-22',url:'https://news.futunn.com/post/1001863220',img:'assets/news/9616929c4dd8789c6a3d1c46.gif'}
];
function el(tag,html,cls){const n=document.createElement(tag);if(cls)n.className=cls;if(html!==undefined)n.innerHTML=html;return n}
function draw(){
 if(document.body.dataset.coco2026Fixed==='yes')return;
 const panel=document.getElementById('wl-auto');if(!panel)return;
 document.body.dataset.coco2026Fixed='yes';
 const style=el('style',`
 #wl-auto .wl-editorial.coco-upgraded{display:block!important;padding:19px!important;background:#fffaf5!important;border-top:5px solid #984144!important}
 #wl-auto .coco-kicker{font:700 15px Arial,sans-serif;color:#893b3a;letter-spacing:.08em;margin-bottom:15px}
 #wl-auto .coco-new-grid{display:grid;grid-template-columns:minmax(0,3fr) minmax(180px,1fr);gap:20px;align-items:start}
 #wl-auto .coco-new-grid>*{min-width:0}#wl-auto .coco-new-grid a{color:#8a3939;text-decoration:none}
 #wl-auto .coco-cover{display:block;width:100%;height:auto;max-height:none;aspect-ratio:16/9;object-fit:cover;border-radius:8px}
 #wl-auto .coco-new-grid h2{color:#8b3d3d;font:500 clamp(25px,4vw,40px)/1.35 Georgia,'Songti SC',serif;margin:15px 0 8px;overflow-wrap:anywhere}
 #wl-auto .coco-new-grid p{font:15px/1.7 Georgia,'Songti SC',serif;color:#5c6456;margin:8px 0}
 #wl-auto .coco-new-grid .coco-history{display:block;margin-top:10px;padding:14px;background:#f1e8dc;border-radius:8px;font:14px/1.6 Arial,sans-serif}
 #wl-auto .coco-new-grid .coco-portrait{width:120px;height:150px;max-width:100%;object-fit:cover;border-radius:8px}
 #wl-auto .coco-new-grid small{font:11px/1.6 Arial,sans-serif;color:#776f66}
 #wl-auto .wl-oil-inline{margin:15px 0;background:#fff8ef;border:1px solid #e2caba;border-radius:12px;padding:17px}
 #wl-auto .wl-oil-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
 #wl-auto .wl-oil-card{padding:14px;background:white;border:1px solid #ead6c7;border-radius:9px}
 #wl-auto .wl-oil-card strong{display:block;font:700 16px Arial,sans-serif;color:#314638}
 #wl-auto .wl-oil-card b{display:block;font:700 clamp(26px,5vw,38px)/1.3 Georgia,serif;color:#a54736}
 #wl-auto .wl-oil-card span{font:13px Arial,sans-serif;color:#9d3b2c}
 #wl-ma-realestate .wl-property-visual{background:#f3eee4;border:1px solid #d9cebd;border-radius:12px;padding:15px;margin:15px 0 19px;display:grid;grid-template-columns:35% 1fr;gap:17px;align-items:center}
 #wl-ma-realestate .wl-property-visual img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px}
 #wl-ma-realestate .wl-chart-row{display:grid;grid-template-columns:75px 1fr 80px;align-items:center;gap:8px;margin:10px 0;font:12px Arial,sans-serif}
 #wl-ma-realestate .wl-chart-track{background:#deddd1;border-radius:20px;overflow:hidden;height:15px}
 #wl-ma-realestate .wl-chart-fill{height:100%;background:#56866b;border-radius:20px}
 #wl-school .wl-school-cover{display:block;position:relative;max-width:1050px;margin:18px auto;padding:0;text-decoration:none;overflow:hidden;border-radius:12px;border:1px solid #e2d7c8;background:white}
 #wl-school .wl-school-cover img{display:block;width:100%;height:230px;object-fit:cover}
 #wl-school .wl-school-cover div{padding:17px 20px;color:#30533c;font:700 19px/1.5 Georgia,'Songti SC',serif}
 #wl-auto .wl-extra-note{display:block;font:10px Arial,sans-serif;color:#827d75;margin-top:4px}
 @media(max-width:720px){#wl-auto .coco-new-grid{display:flex;flex-direction:column;gap:20px}#wl-auto .coco-new-grid>*{width:100%;position:static}#wl-auto .coco-new-grid .coco-portrait{width:105px;height:130px;float:left;margin:0 14px 10px 0}#wl-ma-realestate .wl-property-visual{display:block}#wl-ma-realestate .wl-property-visual img{height:160px;margin-bottom:12px}#wl-school .wl-school-cover img{height:160px}}
 `);document.head.append(style);
 // 1. Replace out-of-date notice on the 2026-10-24 edition only.
 const date=panel.querySelector('.wl-date')?.textContent||'';
 const local=panel.querySelector('.wl-columns>div:first-child');
 if(date.includes('2026-10-24')&&local){
  const first=local.querySelector('a.wl-story');
  if(first&&(/转运站|transfer station/i).test(first.textContent)){
   first.href=LEAF.url;first.target='_blank';first.rel='noopener noreferrer';first.setAttribute('aria-label',LEAF.title);
   const pic=first.querySelector('img');if(pic){pic.src=LEAF.image;pic.alt='Weston Observer: 秋日Weston Town Green，历史图片';}
   const zh=first.querySelector('.wl-copy strong'),en=first.querySelector('.wl-en'),src=first.querySelector('.wl-source');
   if(zh)zh.textContent=LEAF.title;if(en)en.textContent=LEAF.en;if(src)src.textContent=LEAF.source+' · '+LEAF.date;
  }
 }
 // 2. Complete the 10 global slots on the homepage with dated, linked, attributed reports.
 if(date.includes('2026-10-24')){
  const world=panel.querySelector('.wl-columns>div:nth-child(2)');
  if(world){let rows=world.querySelectorAll('a.wl-story').length;
   for(const item of EXTRAS){if(rows>=10)break;
    if([...world.querySelectorAll('a.wl-story')].some(a=>a.href===item.url))continue;
    const rank=6+rows;const card=el('a',`<span class="wl-index">${String(rank).padStart(2,'0')}</span><div class="wl-photo"><img src="${item.img}" loading="lazy" alt="相关主题图像（并非该报道的原始配图）"></div><div class="wl-copy"><strong>${item.zh}</strong><span class="wl-en">${item.en}</span><span class="wl-source">${item.src} · ${item.date}</span><small class="wl-extra-note">主题配图 · 点击访问原始报道</small></div>`,'wl-story');card.href=item.url;card.target='_blank';card.rel='noopener noreferrer';world.append(card);rows++;
   }
  }
 }
 // 3. On the homepage show the latest confirmed Friday settlements (weekend markets closed).
 const oil=panel.querySelector('.wl-oil');
 if(oil&&date.includes('2026-10-24')){const content=el('div',`<div style="font:700 20px Georgia,serif;color:#9d3b2c;margin-bottom:6px">国际油价 · OIL MARKETS</div><div class="wl-oil-cards"><div class="wl-oil-card"><strong>Brent 布伦特原油</strong><b>$116.72</b><span>▲ +3.14%</span></div><div class="wl-oil-card"><strong>WTI 美国原油</strong><b>$103.27</b><span>▲ +3.82%</span></div></div><div style="margin-top:10px;font:12px/1.6 Arial;color:#806f64">2026-10-23 收盘结算价 · 美元/桶 · 数据来源：Reuters / NYMEX、ICE；周末并非实时交易价。每日自动发布后更新。</div>`,'wl-oil-inline');oil.replaceWith(content);}
 // Future-day oil prices: on-page TradingView quote widgets (automatically update if permitted by provider).
 if(oil&&!date.includes('2026-10-24')){
   const holder=el('div','<div style="font:700 19px Georgia,serif;color:#914135;margin-bottom:12px">国际油价 · Brent / WTI</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px" class="oil-quote-grid"><div class="tradingview-widget-container" data-symbol="TVC:UKOIL"><div class="tradingview-widget-container__widget"></div></div><div class="tradingview-widget-container" data-symbol="TVC:USOIL"><div class="tradingview-widget-container__widget"></div></div></div><div style="font:11px Arial;color:#89796b;margin-top:10px">数据由 TradingView 行情组件提供；市场休市时显示最近价格，数据可能延迟。</div>','wl-oil-inline');
   oil.replaceWith(holder);
   holder.querySelectorAll('[data-symbol]').forEach(function(block){
     const script=document.createElement('script');script.type='text/javascript';script.async=true;
     script.src='https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js';
     script.text=JSON.stringify({symbol:block.dataset.symbol,width:'100%',locale:'zh_CN',colorTheme:'light',isTransparent:true});
     block.appendChild(script);
   });
 }
 // 4. Clear editorial disclaimer and show current France article, Russia archived second.
 const editorial=panel.querySelector('.wl-editorial');if(editorial){editorial.classList.add('coco-upgraded');editorial.innerHTML=`<div class="coco-kicker">☕ 可可豆子的咖啡 · COCO'S COFFEE</div><div class="coco-new-grid"><article><a href="/coco-france-2026.html"><img class="coco-cover" src="/assets/coco_france_hero.webp" alt="AI创作的法国游行示意插画"><h2>2026法国更大规模的游行：一场“饮鸩止渴”的社会困局</h2></a><p>2026年10月24日 · 高税负、公共债务与街头示威</p><p><a href="/coco-france-2026.html"><b>阅读全文 →</b></a></p><small>封面为AI创作示意图，非现场摄影。文章引用来源详见全文。</small></article><aside><img class="coco-portrait" src="/assets/coco_portrait_2026.webp" alt="可可豆子水彩头像"><p style="font-weight:700">历史第二篇 · 2026年10月23日</p><a class="coco-history" href="/coco-ukraine-2026.html">俄乌战争：一场关于历史、领土与国家命运的战争 →</a><p><a href="/coco-opinions.html">查看全部历史文章 →</a></p></aside></div>`;}
 // Remove any second Coco panel generated by the old script to avoid overlap.
 document.querySelectorAll('#coco-editorial-2026').forEach(x=>x.remove());
 // 5. MA real estate photo + clearly labeled chart based on verified Sept figures already in this section.
 const property=document.getElementById('wl-ma-realestate');if(property&&!property.querySelector('.wl-property-visual')){
  const chart=el('div',`<img src="/assets/cozy_home.jpg" alt="马萨诸塞州住宅风格示意照片"><div><div style="font:700 18px Georgia,serif;color:#315f47">MA 房价对比 · 2026年9月</div><div style="font:12px Arial;color:#796e5c;margin:6px 0 12px">独栋与公寓成交价中位数，不是平均价</div><div class="wl-chart-row"><span>独栋</span><div class="wl-chart-track"><div class="wl-chart-fill" style="width:100%"></div></div><strong>$670K</strong></div><div class="wl-chart-row"><span>公寓</span><div class="wl-chart-track"><div class="wl-chart-fill" style="width:78.36%"></div></div><strong>$525K</strong></div><div style="font:11px Arial;color:#877b70">图表来源：Massachusetts Association of REALTORS（详见本栏目数据来源）</div></div>`,'wl-property-visual');const intro=property.querySelector('.mre-intro');if(intro)intro.insertAdjacentElement('afterend',chart);else property.prepend(chart);
 }
 const school=document.getElementById('wl-school');if(school&&!school.querySelector('.wl-school-cover')){
  const feature=el('a',`<img src="https://westontoday.news/img_2022/whs_schools-210723_09..jpg" alt="Weston High School 主入口，照片来源 Weston Today"><div>🎓 Weston High School 毕业生升学去向（2024–2026）· 点击阅读全文 →</div>`,'wl-school-cover');feature.href='/weston-graduates.html';const title=school.querySelector('h2');if(title)title.insertAdjacentElement('afterend',feature);else school.prepend(feature);
 }
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',draw);else draw();
})();
