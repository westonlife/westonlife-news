/* Homepage Coco card replacement; does not access visitor counters. */
(function(){
 'use strict';
 function run(){
  var panel=document.querySelector('#wl-auto .wl-editorial');
  var grid=panel&&panel.querySelector('.coco-new-grid');
  var article=grid&&grid.querySelector('article');
  if(!article||article.dataset.cocoSix==='1')return;
  var link=article.querySelector('a');
  if(!link)return;
  link.href='/coco-six-points-2026-publish.html';
  var img=link.querySelector('img');
  if(img){img.src='/coco-six-cover-2026.jpg';img.alt='自由女神像，还能照亮多少美国梦？';}
  var h=link.querySelector('h2');
  if(h)h.textContent='自由女神像，还能照亮多少美国梦？';
  var p=article.querySelectorAll(':scope > p');
  if(p[0])p[0].textContent='特朗普的六大政策之殇：战争、移民、关税、股市、盟友与家族利益。';
  if(p[1])p[1].textContent='2026年11月4日 · 可可豆子的时事评论';
  if(p[2]){p[2].innerHTML='<a href="/coco-six-points-2026-publish.html"><b>阅读全文 →</b></a>';}
  var aside=grid.querySelector('aside');
  if(aside&&!aside.querySelector('[data-coco-history-six]')){
   var a=document.createElement('a');a.href='/coco-iran-2026.html';
   a.className='coco-history';a.dataset.cocoHistorySix='1';
   a.textContent='2026年11月1日 ·《五个不能》→';
   var label=aside.querySelector('p');if(label)label.insertAdjacentElement('afterend',a);else aside.appendChild(a);
  }
  article.dataset.cocoSix='1';
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
 window.addEventListener('load',run);
})();
