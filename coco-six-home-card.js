/* Weston Life Coco editorial card — additive only; never reads/writes visitor counters. */
(function(){
  function add(){
    if(document.getElementById('coco-six-points-2026-card'))return;
    var old=document.querySelector('a[href*="coco-iran-five-cannots-2026"]');
    if(!old){return;}
    var card=old.cloneNode(true);
    card.id='coco-six-points-2026-card';
    card.href='/coco-six-points-2026-publish.html';
    card.querySelectorAll('[href]').forEach(function(a){a.href='/coco-six-points-2026-publish.html'});
    var pic=card.querySelector('img');
    if(pic){pic.src='/coco-six-cover-2026.jpg';pic.alt='自由女神像，还能照亮多少美国梦？';pic.style.width='100%';pic.style.objectFit='cover';}
    var headings=card.querySelectorAll('h1,h2,h3,h4');
    if(headings.length)headings[0].textContent='自由女神像，还能照亮多少美国梦？';
    var desc=card.querySelector('p');if(desc)desc.textContent='六大政策之殇：战争、移民、关税、股市、盟友与家族利益';
    // Clone the existing article card to retain precisely the same image size and layout.
    old.parentNode.insertBefore(card,old);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',add);else add();
  window.addEventListener('load',add);
})();
