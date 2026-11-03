/* Weston Life special news replacement, installed 2026-11-03.
   Hacker feature: Nov 3-4; Pope local top story: Nov 3-5; archived after. */
(function(){
 'use strict';
 var START=Date.parse('2026-11-03T00:00:00-05:00');
 var HACKER_END=Date.parse('2026-11-05T00:00:00-05:00');
 var POPE_END=Date.parse('2026-11-06T00:00:00-05:00');
 var ARCHIVE_START=Date.parse('2026-11-03T00:00:00-05:00');
 var hTitle='现实中的骇客：币安63亿美元盗案背后的朝鲜黑客网络';
 var pTitle='历史性一票：首位已知在任期间参与美国选举投票的教皇';
 var hPath='/news/news-2026-11-03-binance-cyber.html';
 var pPath='/news/news-2026-11-03-pope-vote.html';
 var hImg='/assets/news-2026-11-03-hacker.jpg';
 var pImg='/assets/news-2026-11-03-pope-vote.svg';
 var planePath='/news/news-2026-11-01-learjet-bahamas-crash.html';
 function node(id){return document.getElementById(id)}
 function esc(s){var e=document.createElement('span');e.textContent=s;return e.innerHTML;}
 function css(){
   if(node('wl-20261103-style'))return;
   var s=document.createElement('style');s.id='wl-20261103-style';
   s.textContent='#wl-special-hacker-20261103{max-width:1140px;background:#fff;color:#171717;margin:18px 0 30px;border-top:3px solid #0e2728;border-bottom:1px solid #ddd;padding:14px 0 23px;font-family:Arial,"PingFang SC",sans-serif}' +
   '#wl-special-hacker-20261103 a{text-decoration:none;color:inherit;display:block}' +
   '#wl-special-hacker-20261103 .wl-sp-kicker{font-weight:bold;letter-spacing:.1em;font-size:12px;margin:0 0 12px;color:#456}' +
   '#wl-special-hacker-20261103 img{width:100%;max-height:520px;object-fit:cover;display:block;background:#061718}' +
   '#wl-special-hacker-20261103 h2{font-family:"Songti SC",Georgia,serif;font-size:clamp(25px,3.7vw,42px);line-height:1.4;margin:13px 0 12px;color:#111}' +
   '#wl-special-hacker-20261103 .wl-sp-deck{font-size:16px;line-height:1.85;max-width:920px;color:#333;margin:0 0 14px}' +
   '#wl-special-hacker-20261103 .wl-sp-photo{font-size:12px;line-height:1.7;color:#666;margin:7px 0 0}' +
   '#wl-special-hacker-20261103 .wl-sp-read{font-size:14px;font-weight:bold;text-decoration:underline;text-underline-offset:4px}' +
   '#wl-pope-pin-20261103{border-left:4px solid #3e6e92;background:#f3f7fa!important;border-radius:6px;padding:6px!important}' +
   '#wl-pope-pin-20261103 .wl-photo img{object-fit:cover;max-height:180px}' +
   '#wl-special-history-20261103{border-top:1px solid #bbb;padding:20px 0;margin-top:25px;font-family:Arial,"PingFang SC",sans-serif;color:#161616}' +
   '#wl-special-history-20261103 h2{font-size:20px;margin:0 0 8px;color:#111}' +
   '#wl-special-history-20261103 a{display:block;color:#222;font-size:14px;line-height:1.8;padding:7px 0;text-decoration:underline;text-underline-offset:3px}' +
   '@media(max-width:700px){#wl-special-hacker-20261103{padding-left:4px;padding-right:4px}#wl-special-hacker-20261103 img{max-height:none}}';
   document.head.appendChild(s);
 }
 function mountHacker(panel,t){
   var el=node('wl-special-hacker-20261103');
   if(t<START||t>=HACKER_END){if(el)el.remove();return;}
   if(el)return;
   el=document.createElement('article');el.id='wl-special-hacker-20261103';
   el.innerHTML='<a href="'+hPath+'"><div class="wl-sp-kicker">深度报道 · 2026-11-03 · 首页置顶两天（11月3—4日）</div>'+
   '<img src="'+hImg+'" alt="绿色数字都市里的皮衣耳机青年，人物身份未经核实的视觉示意图" loading="eager">'+
   '<div class="wl-sp-photo">视觉示意图：网传人物身份未经核实，非FBI确认的嫌疑人照片</div>'+
   '<h2>'+esc(hTitle)+'</h2><p class="wl-sp-deck">币安约63亿美元代币资产被盗，FBI把事件归因于朝鲜黑客行动TraderTraitor。朴珍赫因旧案再受关注，但FBI这次没有直接点名他。</p><strong class="wl-sp-read">阅读完整报道 / Read full story</strong></a>';
   var before=panel.querySelector('.wl-columns,.wl-breaking,.wl-news-grid,.wl-news-list,.wl-stories');
   var mast=panel.querySelector('.wl-masthead');
   if(before)panel.insertBefore(el,before);
   else if(mast)mast.insertAdjacentElement('afterend',el);
   else panel.insertBefore(el,panel.firstChild);
 }
 function mountPope(panel,t){
   var col=panel.querySelector('.wl-columns > div:first-child');
   var p=node('wl-pope-pin-20261103');
   if(!col)return;
   if(t<START||t>=POPE_END){
     if(p)p.remove();
     Array.prototype.forEach.call(col.querySelectorAll(':scope > .wl-story'),function(story){story.style.display='';});
     return;
   }
   if(!p){
     var heading=col.querySelector('.wl-column-title');
     if(!heading)return;
     p=document.createElement('a');p.id='wl-pope-pin-20261103';p.className='wl-story';p.href=pPath;
     p.innerHTML='<span class="wl-index">01</span><div class="wl-photo"><img src="'+pImg+'" alt="教皇投票主题原创示意插画" loading="eager"></div>'+
       '<div class="wl-copy"><strong>'+esc(pTitle)+'</strong><span class="wl-en">Pope Leo XIV votes in U.S. midterms — Vatican confirms historic first</span>'+
       '<span class="wl-source">Weston Life · 2026-11-03 · 梵蒂冈10月30日确认</span></div>';
     heading.insertAdjacentElement('afterend',p);
   }
   var stories=Array.prototype.filter.call(col.children,function(e){return e.classList.contains('wl-story');});
   stories.forEach(function(story,i){story.style.display=i<5?'':'none';var n=story.querySelector('.wl-index');if(n)n.textContent=String(i+1).padStart(2,'0');});
 }
 function archive(panel,t){
   var el=node('wl-special-history-20261103');
   if(t<ARCHIVE_START){if(el)el.remove();return;}
   if(!el){el=document.createElement('section');el.id='wl-special-history-20261103';el.innerHTML='<h2>专题历史新闻 · SPECIAL REPORT ARCHIVE</h2>';
     var prior=node('news-archive');
     if(prior)prior.insertBefore(el,prior.firstChild);
     else panel.appendChild(el);
   }
   var entries=[];
   if(t>=HACKER_END)entries.push('<a href="'+hPath+'">2026-11-03 · '+esc(hTitle)+' — 阅读全文</a>');
   if(t>=POPE_END)entries.push('<a href="'+pPath+'">2026-11-03 · '+esc(pTitle)+' — 阅读全文</a>');
   // Existing airplane report remains available for the originally promised 7-day archive period.
   if(t<Date.parse('2026-11-11T00:00:00-05:00'))entries.push('<a href="'+planePath+'">2026-11-01 · Learjet 60 飞机事故 · 原深度报道（历史）</a>');
   var markup='<h2>专题历史新闻 · SPECIAL REPORT ARCHIVE</h2>'+entries.join('');
   if(el.innerHTML!==markup)el.innerHTML=markup;
 }
 function render(){
   var panel=node('wl-auto')||document.querySelector('main');if(!panel)return;
   var t=Date.now();css();
   // Defensive cleanup against existing pinned cards while retaining daily news & all article files.
   var old=node('wl-learjet-headline-2026');if(old)old.remove();
   old=node('wl-halloween-pin');if(old)old.remove();
   mountHacker(panel,t);mountPope(panel,t);archive(panel,t);
 }
 render();document.addEventListener('DOMContentLoaded',render);window.addEventListener('load',render);
 document.addEventListener('visibilitychange',render);setInterval(render,60000);
 // The site is statically generated; normal page loads and periodic checks are sufficient.
})();
