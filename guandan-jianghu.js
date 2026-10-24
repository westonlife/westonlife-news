/* Weston Life · 米国掼蛋江湖（独立新增模块）
   保留 Coco's Perspective / 可可豆子的观点、学校升学、每日新闻等原栏目不变。
   Add <script src="/guandan-jianghu.js" defer></script> below existing coco-opinion.js in index.html.
*/
(function () {
  'use strict';
  function mountGuandan() {
    if (document.getElementById('wl-guandan-serial')) return;
    var stylesheet = document.createElement('style');
    stylesheet.id = 'wl-guandan-serial-style';
    stylesheet.textContent = `
      #wl-guandan-serial{max-width:1100px;margin:30px auto;padding:26px 25px 30px;background:#fffaf3;border:1px solid #e2d7c8;border-top:5px solid #9e613b;border-radius:14px;box-shadow:0 8px 25px rgba(51,44,28,.06);color:#2a3d30;text-align:center;font-family:Georgia,'Songti SC','Noto Serif CJK SC',serif}
      #wl-guandan-serial *{box-sizing:border-box}
      #wl-guandan-serial .gd-kicker{font:700 12px/1.6 Arial,sans-serif;letter-spacing:.18em;color:#9a603e;margin:0 0 10px}
      #wl-guandan-serial h2{font:500 clamp(29px,4.2vw,49px)/1.3 Georgia,'Songti SC',serif;color:#304f3a;margin:12px 0!important}
      #wl-guandan-serial .gd-meta{color:#896c56;font:14px/1.7 Arial,sans-serif;margin:8px 0 18px}
      #wl-guandan-serial .gd-cover{max-width:1000px;display:block;margin:0 auto 22px;text-decoration:none;overflow:hidden;border-radius:11px;border:1px solid #eadcca}
      #wl-guandan-serial .gd-cover img{display:block;width:100%;height:auto;object-fit:contain;transition:transform .3s}
      #wl-guandan-serial .gd-cover:hover img{transform:scale(1.015)}
      #wl-guandan-serial .gd-intro{font:17px/1.8 Georgia,'Songti SC',serif;max-width:780px;margin:15px auto 16px;color:#4d5245}
      #wl-guandan-serial .gd-btn{display:inline-block;padding:13px 27px;color:#fff!important;background:#406148;border-radius:9px;font:700 14px/1.4 Arial,sans-serif;text-decoration:none!important}
      #wl-guandan-serial .gd-btn:hover{background:#2d4b35}
      html[data-wl-lang="zh"] #wl-guandan-serial .gd-en{display:none!important}
      html[data-wl-lang="en"] #wl-guandan-serial .gd-zh{display:none!important}
      @media (max-width:650px){#wl-guandan-serial{padding:16px 13px 20px;margin:20px 12px}#wl-guandan-serial .gd-kicker{font-size:10px;letter-spacing:.08em}#wl-guandan-serial .gd-intro{font-size:15px}}
    `;
    document.head.appendChild(stylesheet);
    var section = document.createElement('section');
    section.id = 'wl-guandan-serial';
    section.setAttribute('aria-label', '米国掼蛋江湖 · 系列连载小说');
    section.innerHTML = `
      <p class="gd-kicker">WESTON LIFE · COMMUNITY SERIAL NOVEL</p>
      <h2><span class="gd-zh">米国掼蛋江湖之系列——Weston对战Newton</span><span class="gd-en">Guandan Chronicles in America · Weston vs. Newton</span></h2>
      <p class="gd-meta"><span class="gd-zh">第一回 · 作者：巧克力豆子</span><span class="gd-en">Chapter One · By Coco Bean</span></p>
      <a class="gd-cover" href="/guandan-jianghu-01.html" title="阅读《米国掼蛋江湖》第一回 / Read Chapter One">
        <img src="/guandan-waltham-pencil.webp" alt="米国掼蛋江湖之系列 Weston对战Newton 彩色铅笔画，六位牌友围桌掼蛋" loading="eager" decoding="async">
      </a>
      <p class="gd-intro gd-zh">昨夜Waltham，Weston与Newton狭路相逢。一局掼蛋打了六个小时，竟仍未分胜负！江湖未完，且听巧克力豆子说书。</p>
      <p class="gd-intro gd-en">A Guandan showdown in Waltham: Weston versus Newton. Six hours of cards, and still no decisive winner. The neighborhood legend begins here.</p>
      <a class="gd-btn" href="/guandan-jianghu-01.html"><span class="gd-zh">阅读第一回 →</span><span class="gd-en">Read Chapter One →</span></a>
    `;
    var coco = document.getElementById('coco-editorial-2026');
    var school = document.getElementById('wl-school');
    if (coco && coco.parentNode) {
      // Must appear directly after Coco's Perspective and before the school statistics.
      coco.insertAdjacentElement('afterend', section);
    } else if (school && school.parentNode) {
      school.parentNode.insertBefore(section, school);
    } else {
      var news = document.getElementById('wl-auto');
      if (news) news.insertAdjacentElement('afterend', section);
      else document.body.appendChild(section);
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountGuandan, {once:true});
  } else { mountGuandan(); }
})();
