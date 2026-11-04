/* Weston Life: homepage language synchronization, 2026-11-04.
   Only changes visible text inside specified sections. No counter access. */
(function(){'use strict';
var poemZH=[
'诗词里的中国','China in 100 Poems',
'你是否还在为孩子学不好汉语而焦虑？',
'你是否担心孩子缺乏深厚的中国历史文化底蕴？是否担心孩子对中国社会、人文和历史缺乏深入理解？',
'那么，请从《诗词里的中国》开始。',
'通过这一本书，以100首经典诗词为学习路径，让孩子用轻松而系统的方法学习汉语，理解中国历史、文化与社会，逐步建立深厚的中华文化底蕴。',
'这就是作者编写这本书的初衷。','作者：出水芙蓉','进入《诗词里的中国》 →'];
var poemEN=[
'China in 100 Poems','Learn Chinese Through 100 Classical Poems',
'Are you concerned that your child is struggling to learn Chinese?',
'Do you wish your child had a deeper understanding of Chinese history, society, literature and culture?',
'Start with China in 100 Poems.',
'Through 100 classical poems, this collection offers a gentle, systematic way to learn Chinese while exploring the history, culture and ideas behind the language.',
'That is why the author created this collection.','By: Lotus Rising from the Water','Explore the Poems →'];
var cocoZH=['☕ 可可豆子实时评论 · COCO\'S COFFEE','自由女神像，还能照亮多少美国梦？','特朗普的六大政策之殇：战争、移民、关税、股市、盟友与家族利益。','2026年11月4日 · 可可豆子的时事评论','阅读全文 →','封面为水彩风格AI创作插画，非现场摄影；事实与评论详见全文。','过去 · 历史文章','2026年11月1日 ·《五个不能》→','2026法国更大规模的游行：一场“饮鸩止渴”的社会困局 →','查看全部历史文章 →'];
var cocoEN=['☕ Coco’s Commentary · COCO\'S COFFEE','Can the Statue of Liberty Still Illuminate the American Dream?','Six Troubling Policies of the Trump Era: War, Immigration, Tariffs, Markets, Allies and Family Interests.','November 4, 2026 · Commentary by Coco','Read the full article →','Cover art is an AI-generated watercolor-style illustration, not a documentary photograph. See the article for analysis and sources.','Previous Articles','November 1, 2026 · Five Things We Must Not Do →','France’s Larger Wave of Protests: A Social Dilemma →','View all previous articles →'];
function remember(el,zh,en,lang){if(!el)return; if(!el.dataset.wlOriginalText)el.dataset.wlOriginalText=el.textContent;el.textContent=lang==='en'?en:zh;}
function apply(){
 var lang=document.documentElement.dataset.wlLang==='en'?'en':'zh';
 var poem=document.getElementById('china-poems');
 if(poem){var nodes=[poem.querySelector('h2'),poem.querySelector('h3')].concat(Array.from(poem.querySelectorAll('p')),[poem.querySelector('a[href="/poetry.html"]')]);nodes.forEach(function(el,i){if(el)remember(el,poemZH[i],poemEN[i],lang)});}
 var panel=document.querySelector('#wl-auto .wl-editorial');
 if(panel){var grid=panel.querySelector('.coco-new-grid'), article=grid&&grid.querySelector('article'),aside=grid&&grid.querySelector('aside');
 var items=[panel.querySelector('.coco-kicker'),article&&article.querySelector('h2'),article&&article.querySelector(':scope > p:nth-of-type(1)'),article&&article.querySelector(':scope > p:nth-of-type(2)'),article&&article.querySelector(':scope > p:nth-of-type(3) a'),article&&article.querySelector('small'),aside&&aside.querySelector('p'),aside&&aside.querySelector('[data-coco-history-six]'),aside&&aside.querySelector('a.coco-history:not([data-coco-history-six])'),aside&&aside.querySelector('a[href="/coco-opinions.html"]')];
 items.forEach(function(el,i){if(el)remember(el,cocoZH[i],cocoEN[i],lang)});
 }
 var hacker=document.getElementById('wl-special-hacker-20261103');
 if(hacker){var h=hacker.querySelector('h2'),deck=hacker.querySelector('.wl-sp-deck');
 if(h)remember(h,'现实中的骇客：币安63亿美元盗案背后的朝鲜黑客网络','Inside the Alleged Binance Theft: North Korea-Linked Hacker Networks',lang);
 if(deck)remember(deck,'美国调查机构与网络安全研究人员持续追踪朝鲜背景的网络犯罪活动。','Investigators and cybersecurity researchers continue to examine cybercrime networks linked to North Korea.',lang);
 }
}
function schedule(){setTimeout(apply,0);setTimeout(apply,250)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule);else schedule();
document.addEventListener('click',function(e){if(e.target.closest('[data-wl-choice]'))schedule()});
window.addEventListener('load',schedule);
})();
