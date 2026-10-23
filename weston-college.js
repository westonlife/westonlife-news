/* Weston Life / WHS College Destinations 2026 & 2025.
 * Source 2026: Wildcat Tracks (June 8, 2026), permission-based self-reported list.
 * Source 2025: Weston Town 2026 School Committee annual report, p.29.
 * Derived aggregates only; no student names, and no inflated admissions counts.
 * Place <script src="weston-college.js" defer></script> before </body> in existing index.html.
 */
(function () {
'use strict';
const DATA={"2026":[["Boston College",8],["Northeastern University",8],["Harvard University",6],["Boston University",4],["Brown University",3],["Cornell University",3],["University of Colorado Boulder",3],["University of Southern California",3],["Bucknell University",2],["Duke University",2],["Massachusetts Institute of Technology",2],["New York University",2],["Providence College",2],["Texas Christian University",2],["Trinity College",2],["University of Chicago",2],["University of Massachusetts Amherst",2],["University of Miami",2],["University of Michigan",2],["University of Virginia",2],["Villanova University",2],["Wake Forest University",2],["Babson College",1],["Bates College",1],["Clemson University",1],["Colby College",1],["Colgate University",1],["College of William & Mary",1],["College of the Holy Cross",1],["Connecticut College",1],["Dartmouth College",1],["Emory University",1],["Georgia Institute of Technology",1],["Indiana University",1],["Lehigh University",1],["Liberty University",1],["Manhattanville University",1],["McGill University",1],["Merrimack College",1],["Pomona College",1],["Princeton University",1],["Quinnipiac University",1],["Rice University",1],["San Diego State University",1],["Santa Clara University",1],["Simmons University",1],["Southern Methodist University",1],["St. Bonaventure University",1],["Stanford University",1],["Suffolk University",1],["Syracuse University",1],["Tufts University",1],["Tulane University",1],["U.S. Air Force Academy",1],["U.S. Naval Academy",1],["University of California Los Angeles",1],["University of Maryland College Park",1],["University of New Hampshire",1],["University of New Haven",1],["University of Oregon",1],["University of Rhode Island",1],["University of Richmond",1],["University of Rochester",1],["University of South Carolina",1],["University of Tampa",1],["University of Texas at Austin",1],["University of Utah",1],["University of Vermont",1],["University of Wisconsin Madison",1],["Virginia Tech",1],["Washington University in St. Louis",1],["Wentworth Institute of Technology",1],["Wesleyan University",1]],"2025":[["Northeastern University",6],["University of Massachusetts Amherst",6],["Boston College",5],["Colgate University",5],["Cornell University",5],["Boston University",4],["University of Connecticut",4],["University of Virginia",4],["Carnegie Mellon University",3],["Dartmouth College",3],["Harvard University",3],["Indiana University",3],["Mass Bay Community College",3],["Middlebury College",3],["Purdue University",3],["University of Miami",3],["Centre College",2],["Dean College",2],["Elon University",2],["Lasell University",2],["Massachusetts Institute of Technology",2],["McGill University",2],["New York University",2],["Rutgers University",2],["Stonehill College",2],["Tufts University",2],["Tulane University",2],["University of Chicago",2],["University of Colorado Boulder",2],["University of Denver",2],["University of New Hampshire",2],["University of Richmond",2],["University of St Andrews",2],["University of Vermont",2],["University of Wisconsin Madison",2],["Villanova University",2],["Wheaton College MA",2],["Aalto University",1],["Amherst College",1],["Arizona State University",1],["Bates College",1],["Brandeis University",1],["Brigham Young University",1],["Bucknell University",1],["Bunker Hill Community College",1],["Case Western Reserve University",1],["Colby College",1],["Columbia University",1],["Coppin State University",1],["Delaware Valley University",1],["Fairfield University",1],["Florida Institute of Technology",1],["Georgetown University",1],["Georgia State University",1],["Hamilton College",1],["Hobart and William Smith Colleges",1],["Johns Hopkins University",1],["Johnson & Wales University",1],["Kenyon College",1],["Morgan State University",1],["New Jersey Institute of Technology",1],["North Carolina Central University",1],["Penn State University",1],["Pomona College",1],["Princeton University",1],["Providence College",1],["Rose-Hulman Institute of Technology",1],["San Diego State University",1],["Sarah Lawrence College",1],["Southern Methodist University",1],["St. John's University",1],["Suffolk University",1],["Syracuse University",1],["Texas A&M University",1],["The Ohio State University",1],["United States Military Academy",1],["University at Albany",1],["University of Arizona",1],["University of California San Diego",1],["University of Florida",1],["University of Georgia",1],["University of Maryland College Park",1],["University of Massachusetts Boston",1],["University of Massachusetts Lowell",1],["University of Michigan",1],["University of North Carolina Chapel Hill",1],["University of Notre Dame",1],["University of Pennsylvania",1],["University of Rhode Island",1],["University of Tampa",1],["Virginia Tech",1],["Washington University in St. Louis",1],["Wesleyan University",1],["Williams College",1],["Worcester Polytechnic Institute",1],["Yale University",1]]};
const YEAR_SOURCE={'2026':'https://wildcattracks.weston.org/4912/features/seniors-next-steps-4/','2025':'https://www.westonma.gov/DocumentCenter/View/42263/Report-of-the-School-Committee-PDF#page=8'};
const STYLE=`
#wl-school.wc-enhanced{max-width:1100px!important;margin:26px auto!important;padding:0!important;background:#f9f8f3!important;border:1px solid #dadfd1!important;border-radius:18px!important;box-shadow:0 9px 30px rgba(35,55,37,.055);overflow:hidden;font-family:Georgia,'Times New Roman',serif;color:#233d31!important}
#wl-school .wc-hero{padding:28px 32px 24px;background:linear-gradient(125deg,#f1f3e9 0%,#faf7ed 74%);border-bottom:1px solid #e2e4d9}
#wl-school .wc-eyebrow{font:700 11px/1.5 Arial,sans-serif;letter-spacing:.18em;color:#8a7151;margin:0 0 10px}
#wl-school .wc-title{margin:0 0 11px!important;font:600 clamp(27px,3.9vw,39px)/1.2 Georgia,serif!important;color:#31543f!important}
#wl-school .wc-subtitle{margin:0;max-width:800px;font:15px/1.7 Arial,sans-serif;color:#56675b}
#wl-school .wc-controls{display:flex;align-items:center;gap:12px;justify-content:space-between;flex-wrap:wrap;margin:20px 0 0}
#wl-school .wc-search{background:white;border:1px solid #cbd6c9;border-radius:10px;min-width:230px;max-width:420px;width:min(100%,420px);padding:12px 14px;font:14px Arial,sans-serif;color:#26382f;box-sizing:border-box}
#wl-school .wc-hint{font:12px Arial,sans-serif;color:#768377}
#wl-school .wc-year{padding:24px 32px 28px;border-bottom:1px solid #e5e7de}
#wl-school .wc-year:last-child{border-bottom:0}
#wl-school .wc-yearhead{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:15px}
#wl-school .wc-yearhead h3{font:600 25px Georgia,serif;color:#355842;margin:0!important}
#wl-school .wc-source-pill{font:700 11px Arial,sans-serif;background:#e7eee4;color:#406147;border:1px solid #cddbc9;border-radius:999px;padding:6px 11px}
#wl-school .wc-figures{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:14px 0 16px}
#wl-school .wc-figure{padding:15px 14px;border-radius:12px;background:#fff;border:1px solid #e1e5dc;min-width:0}
#wl-school .wc-figure strong{display:block;color:#305a41;font:700 29px/1.2 Arial,sans-serif;margin:0 0 4px}
#wl-school .wc-figure small{font:12px/1.55 Arial,sans-serif;color:#607366;display:block}
#wl-school .wc-summary{font:14px/1.75 Arial,sans-serif;color:#58685c;margin:0 0 16px}
#wl-school .wc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 22px}
#wl-school .wc-row{display:flex;gap:10px;justify-content:space-between;align-items:center;border-bottom:1px solid #e8ece5;padding:10px 0;font:13.5px/1.5 Arial,sans-serif;min-width:0}
#wl-school .wc-row span{min-width:0;overflow-wrap:anywhere}
#wl-school .wc-row b{flex:none;min-width:32px;text-align:center;background:#edf4ea;border-radius:8px;padding:4px 8px;color:#30543d;font:700 14px Arial,sans-serif}
#wl-school .wc-expand{margin:16px 0 0;cursor:pointer;background:#375e47;border:0;color:white;padding:11px 19px;font:600 13px Arial,sans-serif;border-radius:10px}
#wl-school .wc-expand:hover{background:#244733}
#wl-school .wc-sources{margin-top:17px;border-top:1px dashed #d1d9cd;padding-top:14px;font:12px/1.75 Arial,sans-serif;color:#667469}
#wl-school .wc-sources a{color:#315f46;text-decoration:underline;font-weight:600}
#wl-school .wc-empty{font:14px Arial,sans-serif;color:#64776a;padding:18px 0}
html[data-wl-lang="zh"] #wl-school .wc-en{display:none!important}
html[data-wl-lang="en"] #wl-school .wc-zh{display:none!important}
@media(max-width:650px){#wl-school .wc-hero{padding:23px 18px}#wl-school .wc-year{padding:22px 18px}#wl-school .wc-grid{grid-template-columns:1fr}#wl-school .wc-figures{gap:7px}#wl-school .wc-figure{padding:11px 8px}#wl-school .wc-figure strong{font-size:25px}#wl-school .wc-figure small{font-size:11px}#wl-school .wc-search{max-width:none}}
`;
function start(){
  let host=document.getElementById('wl-school');
  if(!host) return;
  if(host.dataset.collegeLoaded==='true')return;
  host.dataset.collegeLoaded='true';
  host.classList.add('wc-enhanced');
  host.setAttribute('aria-label','Weston High School college destinations 2026 and 2025');
  if(!document.querySelector('#wc-styles')){
    const style=document.createElement('style');style.id='wc-styles';style.textContent=STYLE;document.head.appendChild(style);
  }
  host.innerHTML=`
<div class="wc-hero">
  <p class="wc-eyebrow">WESTON LIFE / EDUCATION &amp; COMMUNITY</p>
  <h2 class="wc-title"><span class="wc-zh">🎓 Weston 升学 · 毕业生去向</span><span class="wc-en">🎓 Weston College Destinations</span></h2>
  <p class="wc-subtitle wc-zh">马萨诸塞州 Weston High School，2026届优先展示，随后是2025届。按大学汇总实际就读或毕业生公开填报的去向，并注明原始出处。</p>
  <p class="wc-subtitle wc-en">Weston High School in Massachusetts. The Class of 2026 appears first, followed by 2025. Counts are from published college destinations, with clear source notes.</p>
  <div class="wc-controls">
    <input id="wc-filter" class="wc-search" type="search" aria-label="Search university" placeholder="搜索大学 / Search colleges..." autocomplete="off">
    <span class="wc-hint"><span class="wc-zh">资料核对：2026年10月23日</span><span class="wc-en">Sources checked: Oct 23, 2026</span></span>
  </div>
</div>
<div id="wc-year-2026" class="wc-year"></div>
<div id="wc-year-2025" class="wc-year"></div>`;
  const expanded={'2026':false,'2025':false};
  const esc=t=>String(t).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const t=(zh,en)=>`<span class="wc-zh">${zh}</span><span class="wc-en">${en}</span>`;
  const lang=()=>document.documentElement.getAttribute('data-wl-lang')==='en'?'en':'zh';
  function render(year){
    const panel=document.getElementById('wc-year-'+year);
    const q=document.getElementById('wc-filter').value.trim().toLowerCase();
    const matches=DATA[year].filter(x=>x[0].toLowerCase().includes(q));
    const list=q||expanded[year]?matches:matches.slice(0,14);
    const n=DATA[year].length;
    const people=DATA[year].reduce((acc,x)=>acc+x[1],0);
    const is26=year==='2026';
    const source=is26?'Wildcat Tracks · Jun 8, 2026':'Weston Town · 2026 Report, p.29';
    panel.innerHTML=`
      <div class="wc-yearhead"><h3>${year} ${t('届毕业去向','Class of '+year)}</h3><span class="wc-source-pill">${t(is26?'学生自愿公开名单':'镇政府官方统计',is26?'Student opt-in submissions':'Official town report')}</span></div>
      <div class="wc-figures">
        <div class="wc-figure"><strong>${is26?people:'169'}</strong><small>${t(is26?'自愿公开去向的人数':'毕业生总数',is26?'Opt-in submissions':'Total graduates')}</small></div>
        <div class="wc-figure"><strong>${n}</strong><small>${t('不同大学/机构','Institutions listed')}</small></div>
        <div class="wc-figure"><strong>${is26?'—':'97%'}</strong><small>${t(is26?'非全届完整统计':'继续接受教育',is26?'Not a class-wide rate':'Continuing education')}</small></div>
      </div>
      <p class="wc-summary">${t(
       is26?'校报邀请全届毕业生自愿提供毕业去向，并仅刊登同意公开者。本栏目将同一大学的填报合并统计（例如“Harvard College”归入“Harvard University”），不能把117份公开反馈解释为全部毕业生人数或升学率。':'Weston镇2026年学校委员会报告：2025届169名毕业生，约97%继续接受教育，分布于96所院校。院校旁的数字为实际入读人数，未标人数的学校按1人计；合计164人。',
       is26?'The student newspaper invited graduates to voluntarily share their plans and published only those consenting. Duplicate institution labels are normalized. The '+people+' published responses are not the total class size or a college-going rate.':'The Town of Weston reports 169 graduates in the Class of 2025, with approximately 97% continuing education across 96 institutions. Each number represents matriculants (not admissions offers); the list sums to 164 students.'
      )}</p>
      <div class="wc-grid">${list.length?list.map(([name,count])=>`<div class="wc-row"><span>${esc(name)}</span><b aria-label="students">${count}</b></div>`).join(''):`<p class="wc-empty">${t('没有匹配的大学','No matching colleges')}</p>`}</div>
      ${!q && n>14?`<button class="wc-expand" type="button" data-wc-year="${year}" aria-expanded="${expanded[year]}">${expanded[year]?t('收起大学名单 ↑','Show fewer ↑'):t('查看完整 '+n+' 所大学 →','Show all '+n+' institutions →')}</button>`:''}
      <div class="wc-sources">${t('来源 / 出处：','Source: ')} <a href="${YEAR_SOURCE[year]}" target="_blank" rel="noopener noreferrer">${esc(source)} ↗</a><span class="wc-zh">${is26?' · 原始报道载有同意公开的学生名单；本站只公布各大学的汇总人数。':' · 官方文件第29页；这是入读去向，不是获录取的大学数。'}</span><span class="wc-en">${is26?' · We publish aggregated school counts, not names.':' · Report page 29; these are actual college destinations, not offers.'}</span></div>`;
  }
  function renderAll(){render('2026');render('2025');}
  host.addEventListener('click',function(event){
    const b=event.target.closest('[data-wc-year]');if(!b)return;
    expanded[b.dataset.wcYear]=!expanded[b.dataset.wcYear];render(b.dataset.wcYear);
  });
  document.getElementById('wc-filter').addEventListener('input',renderAll);
  const obs=new MutationObserver(()=>renderAll());
  obs.observe(document.documentElement,{attributes:true,attributeFilter:['data-wl-lang']});
  renderAll();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
