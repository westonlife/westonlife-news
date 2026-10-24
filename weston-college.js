/* Weston Life · School portal: compact home, two destination detail pages, one dated notice archive.
   This file replaces the old long on-homepage college list. No dependencies. */
(function(){
'use strict';
const SCHOOL='Weston High School';
const SOURCES={
  '2025':'https://www.westonma.gov/DocumentCenter/View/42263/Report-of-the-School-Committee-PDF',
  '2026':'https://wildcattracks.weston.org/4912/features/seniors-next-steps-4/'
};
// School-published destination aggregates (same values as the existing weston-college.js).
// 2026 comes from opt-in student responses, NOT all Class of 2026 graduates.
const RAW={
 '2026':`Boston College|8;Northeastern University|8;Harvard University|6;Boston University|4;Brown University|3;Cornell University|3;University of Colorado Boulder|3;University of Southern California|3;Bucknell University|2;Duke University|2;Massachusetts Institute of Technology|2;New York University|2;Providence College|2;Texas Christian University|2;Trinity College|2;University of Chicago|2;University of Massachusetts Amherst|2;University of Miami|2;University of Michigan|2;University of Virginia|2;Villanova University|2;Wake Forest University|2;Babson College|1;Bates College|1;Clemson University|1;Colby College|1;Colgate University|1;College of William & Mary|1;College of the Holy Cross|1;Connecticut College|1;Dartmouth College|1;Emory University|1;Georgia Institute of Technology|1;Indiana University|1;Lehigh University|1;Liberty University|1;Manhattanville University|1;McGill University|1;Merrimack College|1;Pomona College|1;Princeton University|1;Quinnipiac University|1;Rice University|1;San Diego State University|1;Santa Clara University|1;Simmons University|1;Southern Methodist University|1;St. Bonaventure University|1;Stanford University|1;Suffolk University|1;Syracuse University|1;Tufts University|1;Tulane University|1;U.S. Air Force Academy|1;U.S. Naval Academy|1;University of California Los Angeles|1;University of Maryland College Park|1;University of New Hampshire|1;University of New Haven|1;University of Oregon|1;University of Rhode Island|1;University of Richmond|1;University of Rochester|1;University of South Carolina|1;University of Tampa|1;University of Texas at Austin|1;University of Utah|1;University of Vermont|1;University of Wisconsin Madison|1;Virginia Tech|1;Washington University in St. Louis|1;Wentworth Institute of Technology|1;Wesleyan University|1`,
 '2025':`Northeastern University|6;University of Massachusetts Amherst|6;Boston College|5;Colgate University|5;Cornell University|5;Boston University|4;University of Connecticut|4;University of Virginia|4;Carnegie Mellon University|3;Dartmouth College|3;Harvard University|3;Indiana University|3;Mass Bay Community College|3;Middlebury College|3;Purdue University|3;University of Miami|3;Centre College|2;Dean College|2;Elon University|2;Lasell University|2;Massachusetts Institute of Technology|2;McGill University|2;New York University|2;Rutgers University|2;Stonehill College|2;Tufts University|2;Tulane University|2;University of Chicago|2;University of Colorado Boulder|2;University of Denver|2;University of New Hampshire|2;University of Richmond|2;University of St Andrews|2;University of Vermont|2;University of Wisconsin Madison|2;Villanova University|2;Wheaton College MA|2;Aalto University|1;Amherst College|1;Arizona State University|1;Bates College|1;Brandeis University|1;Brigham Young University|1;Bucknell University|1;Bunker Hill Community College|1;Case Western Reserve University|1;Colby College|1;Columbia University|1;Coppin State University|1;Delaware Valley University|1;Fairfield University|1;Florida Institute of Technology|1;Georgetown University|1;Georgia State University|1;Hamilton College|1;Hobart and William Smith Colleges|1;Johns Hopkins University|1;Johnson & Wales University|1;Kenyon College|1;Morgan State University|1;New Jersey Institute of Technology|1;North Carolina Central University|1;Penn State University|1;Pomona College|1;Princeton University|1;Providence College|1;Rose-Hulman Institute of Technology|1;San Diego State University|1;Sarah Lawrence College|1;Southern Methodist University|1;St. John's University|1;Suffolk University|1;Syracuse University|1;Texas A&M University|1;The Ohio State University|1;United States Military Academy|1;University at Albany|1;University of Arizona|1;University of California San Diego|1;University of Florida|1;University of Georgia|1;University of Maryland College Park|1;University of Massachusetts Boston|1;University of Massachusetts Lowell|1;University of Michigan|1;University of North Carolina Chapel Hill|1;University of Notre Dame|1;University of Pennsylvania|1;University of Rhode Island|1;University of Tampa|1;Virginia Tech|1;Washington University in St. Louis|1;Wesleyan University|1;Williams College|1;Worcester Polytechnic Institute|1;Yale University|1`
};
const DATA=Object.fromEntries(Object.entries(RAW).map(([year,rows])=>[year,rows.split(';').map(x=>{const i=x.lastIndexOf('|');return [x.slice(0,i),Number(x.slice(i+1))]})]));
const HOME_NOTICES=[
 {title:'Picture Retake Day 10/27/2026',zh:'10月27日：高中补拍学生照片',published:'2026-10-22',event_date:'2026-10-27',source:SCHOOL,url:'https://www.westonschools.org/high/blog/2026/10/22/picture-retake-day-10-27-2026/'},
 {title:'Class of 2027 Chipotle Fundraiser 10/24',zh:'10月24日：2027届学生筹款活动',published:'2026-10-20',event_date:'2026-10-24',source:SCHOOL,url:'https://www.westonschools.org/high/blog/2026/10/20/class-of-2027-chipotle-fundraiser-10-24/'},
 {title:'Senior Class Lynch Creek Fundraiser',zh:'高四毕业班 Lynch Creek 筹款通知',published:'2026-10-20',source:SCHOOL,url:'https://www.westonschools.org/high/blog/2026/10/20/senior-class-lynch-creek-fundraiser/'}
];
const GRAD_IMG='/assets/weston-graduation-illustration.webp';
const NOTICE_IMG='/assets/weston-school-notice-illustration.webp';
const safe=x=>String(x==null?'':x).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const dateLabel=d=>/^\d{4}-\d{2}-\d{2}$/.test(d||'')?d:'未标日期';
function addStyle(){if(document.getElementById('wl-school-clean-css'))return;
 const el=document.createElement('style');el.id='wl-school-clean-css';el.textContent=`
 #wl-school.wl-school-compact,#wl-school-notices,.wl-school-detail{font-family:Georgia,'Songti SC',serif;max-width:1100px;margin:27px auto;background:#fffdfa;color:#253f35;border:1px solid #e1ddd1;border-radius:15px;padding:23px;box-sizing:border-box;box-shadow:0 4px 22px #273d2710}
 #wl-school.wl-school-compact * ,#wl-school-notices *,.wl-school-detail *{box-sizing:border-box}
 #wl-school.wl-school-compact{display:block!important}
 #wl-school.wl-school-compact h2,#wl-school-notices h2{font:600 clamp(25px,4.6vw,37px)/1.3 Georgia,'Songti SC',serif!important;color:#263e37!important;margin:5px 0!important}
 .wl-school-caption{font:15px/1.7 Arial,sans-serif;color:#6b7780;margin:5px 0 17px}
 .wl-school-image{display:block;width:100%;height:auto;max-height:355px;aspect-ratio:16/9;object-fit:cover;border-radius:10px}
 .wl-school-img-credit{display:block;margin:7px 0 16px;color:#858079;font:11px/1.6 Arial,sans-serif}
 .wl-school-choices{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}
 .wl-school-choice{display:block;text-decoration:none!important;background:#ebeff5;border:1px solid #e0e6ee;border-radius:12px;padding:18px;color:#1a355d!important;font:700 clamp(16px,3vw,21px)/1.4 Arial,sans-serif!important}
 .wl-school-choice span{display:block;font-weight:400;font-size:12px;color:#63768a;margin-top:5px}
 .wl-school-choice:hover{background:#dfe8f4}
 #wl-school-notices{clear:both}
 .wl-school-note-list{margin:8px 0 0}
 .wl-school-note{display:flex;gap:14px;padding:15px 1px;border-bottom:1px solid #e5e6e5;color:#263d35!important;text-decoration:none!important;align-items:start}
 .wl-school-note b{font:600 16px/1.5 Arial,'PingFang SC',sans-serif}
 .wl-school-note small{display:block;font:12px/1.8 Arial,sans-serif;color:#69758a;margin-top:4px}
 .wl-school-note .wl-note-icon{font-size:24px;flex:0 0 29px}
 .wl-school-all{display:inline-block;color:#315b4b!important;font:bold 15px Arial,sans-serif!important;margin-top:20px;text-decoration:underline!important}
 .wl-school-archive-layout{max-width:1000px;margin:0 auto;padding:20px 18px 55px}
 .wl-school-archive-layout .wl-school-note{padding:17px 8px;background:#fff;margin:7px 0;border:1px solid #e6e5dc;border-radius:9px}
 .wl-school-back{display:inline-block;margin-bottom:15px;color:#335d43;font:600 14px Arial,sans-serif}
 .wl-school-detail{padding:24px 28px}
 .wl-school-detail h1{font:500 clamp(27px,5vw,47px)/1.35 Georgia,'Songti SC',serif;color:#244f39}
 .wl-school-filter{width:100%;max-width:420px;border:1px solid #c8d5ca;padding:13px;border-radius:9px;font:15px Arial,sans-serif;margin:18px 0}
 .wl-dest-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 22px}
 .wl-dest-row{display:flex;justify-content:space-between;gap:15px;padding:12px 5px;border-bottom:1px solid #e4e9e2;font:14px/1.4 Arial,sans-serif}
 .wl-dest-row b{color:#27583b;flex:none;font-size:15px}
 .wl-dest-stats{display:flex;flex-wrap:wrap;gap:10px;margin:15px 0}
 .wl-dest-stats span{padding:14px;background:#edf1e9;border-radius:9px;font:13px Arial,sans-serif;color:#35523e}
 .wl-dest-stats strong{display:block;font-size:26px}
 @media(max-width:650px){#wl-school.wl-school-compact,#wl-school-notices,.wl-school-detail{margin:17px 10px;padding:16px} .wl-school-choices{gap:8px}.wl-school-choice{padding:13px 10px}.wl-school-image{max-height:230px}.wl-dest-grid{grid-template-columns:1fr}}
 `;document.head.appendChild(el);
}
function normalize(article){if(!article || typeof article.url!=='string'||!/^https:\/\/www\.westonschools\.org\//.test(article.url))return null;
 const d=/^\d{4}-\d{2}-\d{2}/.exec(article.published||'');if(!d)return null;
 return {title:String(article.title||'').trim(),zh:String(article.zh||'').trim(),published:d[0],source:String(article.source||SCHOOL),url:article.url,event_date:article.event_date||''};
}
function cleanNotices(rows){const seen=new Set(),clean=[];for(const a of rows){let n=normalize(a);if(!n||!n.title||seen.has(n.url))continue;seen.add(n.url);clean.push(n)}
 return clean.sort((a,b)=>b.published.localeCompare(a.published)||a.title.localeCompare(b.title)).slice(0,90);
}
function fromOldNoticeDom(){const items=[];document.querySelectorAll('[id="wl-school-today"] a.wl-school-post').forEach(a=>{
 const strong=a.querySelector('strong'),small=a.querySelector('small');const title=strong?.textContent?.trim();const meta=small?.textContent||'';const date=meta.match(/20\d\d-\d\d-\d\d/);
 if(title&&date)items.push({title,published:date[0],url:a.href,source:SCHOOL});
 });return items;
}
async function notices(old=[]){let remote=[];try{const resp=await fetch('/school-notices.json?v='+new Date().toISOString().slice(0,10),{cache:'no-store'});if(resp.ok){const data=await resp.json();remote=Array.isArray(data)?data:(data.notices||[]);}}catch(_){/* keep official static notices */}
 return cleanNotices([...remote,...old,...HOME_NOTICES]);
}
function oneNotice(a){return `<a class="wl-school-note" href="${safe(a.url)}" target="_blank" rel="noopener noreferrer"><span class="wl-note-icon" aria-hidden="true">📅</span><span><b>${safe(a.zh||a.title)}</b><small>${a.zh?`<span lang="en">${safe(a.title)} · </span>`:''}发布 ${safe(dateLabel(a.published))}${a.event_date?` · 活动日期 ${safe(a.event_date)}`:''} · ${safe(a.source)} · 官方原文 ↗</small></span></a>`;}
function showCompactHome(){const host=document.getElementById('wl-school');if(!host)return;
 // Record old, dated, official notices BEFORE eliminating duplicated HTML blocks.
 const old=fromOldNoticeDom();
 document.querySelectorAll('[id="wl-school-today"], [id="wl-school-daily"]').forEach(n=>n.remove());
 host.classList.add('wl-school-compact');host.setAttribute('aria-label','Weston High School 毕业生去向');
 host.innerHTML=`<h2>🎓 Weston High School 毕业生去向</h2><p class="wl-school-caption">College Destinations · 两届毕业去向分开查看</p>
 <img class="wl-school-image" src="${GRAD_IMG}" alt="毕业生戴学士帽合影的示意图片，非 Weston High School 实际毕业照" loading="lazy">
 <small class="wl-school-img-credit">毕业主题示意图片 · 非 Weston High School 实际毕业合影</small>
 <span class="wl-school-cover" style="display:none!important" aria-hidden="true"></span><div class="wl-school-choices"><a class="wl-school-choice" href="/weston-graduates-2025.html">🎓 2025届毕业去向 <span>查看大学及人数 →</span></a><a class="wl-school-choice" href="/weston-graduates-2026.html">🎓 2026届毕业去向 <span>查看大学及人数 →</span></a></div>`;
 const old2=document.getElementById('wl-school-notices');if(old2)old2.remove();
 const n=document.createElement('section');n.id='wl-school-notices';n.innerHTML=`<h2>📰 Weston School 最新动向</h2><p class="wl-school-caption">学校通知 · 活动安排 · 家长重要提醒</p><img class="wl-school-image" src="${NOTICE_IMG}" alt="学校通知板示意图片" loading="lazy"><small class="wl-school-img-credit">学校公告示意图片</small><div class="wl-school-note-list" id="wl-school-latest-list"></div><a class="wl-school-all" href="/weston-school-notices.html">查看全部学校通知 →</a>`;
 host.insertAdjacentElement('afterend',n);
 const list=n.querySelector('#wl-school-latest-list');list.innerHTML=cleanNotices([...old,...HOME_NOTICES]).slice(0,4).map(oneNotice).join('');
 notices(old).then(all=>{list.innerHTML=all.slice(0,4).map(oneNotice).join('')});
}
function showYearPage(){const root=document.getElementById('weston-graduate-detail');if(!root)return;let year=root.dataset.year; if(!DATA[year])return;
 const rows=DATA[year],n=rows.reduce((s,x)=>s+x[1],0);let is26=year==='2026';
 root.classList.add('wl-school-detail');root.innerHTML=`<a class="wl-school-back" href="/">← 返回 Weston Life 首页</a><h1>🎓 Weston High School ${year}届毕业生去向</h1><p class="wl-school-caption">Class of ${year} · College Destinations</p><img class="wl-school-image" src="${GRAD_IMG}" alt="毕业主题示意图，非 Weston High School 实际毕业照"><small class="wl-school-img-credit">毕业主题示意图片，非该校实际毕业照</small>
 <p>${is26?'根据 Wildcat Tracks 2026年6月公开、自愿填报的毕业去向整理。并非全届毕业生统计，也不是大学录取通知书数量。':'根据 Weston 镇政府学校委员会公开报告整理。下列为报告中列出的大学去向人数；不同统计口径下名单人数总和可能与毕业生总人数不同。'}</p>
 <div class="wl-dest-stats"><span><strong>${rows.length}</strong>所学校 / 机构</span><span><strong>${n}</strong>${is26?'份自愿公开填报':'条已列院校人数合计'}</span>${is26?'':'<span><strong>169</strong>镇报告毕业生总数</span><span><strong>约97%</strong>继续升学</span>'}</div>
 <label for="wl-school-find">搜索大学名称 / Search Colleges</label><input id="wl-school-find" class="wl-school-filter" type="search" placeholder="例如 MIT / Cornell / Northeastern"><div class="wl-dest-grid" id="wl-school-results"></div>
 <p style="font:13px/1.8 Arial,sans-serif;margin-top:30px">资料来源：<a href="${SOURCES[year]}" target="_blank" rel="noopener noreferrer">${is26?'Wildcat Tracks 学生自愿公开名单':'Weston 镇 School Committee 官方报告'} ↗</a>。资料发布时间、统计范围和实际入读口径请以原文为准。</p>`;
 const result=root.querySelector('#wl-school-results'),input=root.querySelector('#wl-school-find');
 function draw(){const q=input.value.toLowerCase().trim();result.innerHTML=rows.filter(([name])=>name.toLowerCase().includes(q)).map(([name,num])=>`<div class="wl-dest-row"><span>${safe(name)}</span><b>${num}</b></div>`).join('')||'<p>没有匹配的学校</p>';}
 input.addEventListener('input',draw);draw();
}
function showNoticeArchive(){const root=document.getElementById('weston-school-notices-page');if(!root)return;root.classList.add('wl-school-archive-layout');
 root.innerHTML=`<a class="wl-school-back" href="/">← 返回 Weston Life 首页</a><h1 style="color:#315c41">📰 Weston School 最新动向</h1><p class="wl-school-caption">Weston High School及Weston Public Schools官方公开通知。按照<strong>发布日期从新到旧</strong>排列，点击每条阅读学校原文。</p><img class="wl-school-image" src="${NOTICE_IMG}" alt="Weston School 学校通知板示意图"><small class="wl-school-img-credit">通知板示意图片，非真实公示栏照片</small><div id="wl-school-notice-full"></div><p style="font:13px/1.8 Arial,sans-serif;margin-top:24px">重要：本页是公开网页通知整理，不替代学校通过 PowerSchool、电子邮件或私人家长系统发送的通知。<a href="https://www.westonschools.org/high/" target="_blank">Weston High School 官网 ↗</a> · <a href="https://www.westonschools.org/news/" target="_blank">学区新闻 ↗</a> · <a href="https://www.westonschools.org/calendar/" target="_blank">学区日历 ↗</a></p>`;
 const box=root.querySelector('#wl-school-notice-full');box.innerHTML=HOME_NOTICES.map(oneNotice).join('');
 notices().then(all=>{box.innerHTML=all.map(oneNotice).join('')||'<p>当前没有可核实的公开学校通知。</p>'});
}
function init(){addStyle();showCompactHome();showYearPage();showNoticeArchive();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
