/* WestonLife 第三首《七步诗》；独立模块，不读取或修改计数器 */
(function(){
  'use strict';
  if(document.getElementById('wl-qibushi-3')) return;
  const section=document.createElement('section');
  section.id='wl-qibushi-3';
  section.setAttribute('aria-label','第三首 七步诗');
  section.innerHTML=`
    <style>
    #wl-qibushi-3{box-sizing:border-box;max-width:960px;margin:42px auto;padding:32px 22px;background:#fff;color:#28372e;font-family:serif;line-height:1.95;border-top:1px solid #e4e1d8}
    #wl-qibushi-3 *{box-sizing:border-box}
    #wl-qibushi-3 .wlq-title{text-align:center;font-size:30px;margin:4px 0 2px;color:#263b2c}
    #wl-qibushi-3 .wlq-author{text-align:center;color:#777;font-size:17px;margin-bottom:24px}
    #wl-qibushi-3 .wlq-poem{text-align:center;font-size:22px;line-height:2.15;margin:18px 0}
    #wl-qibushi-3 .wlq-poem p{margin:0}
    #wl-qibushi-3 .wlq-pic{display:block;max-width:min(100%,420px);height:auto;margin:22px auto;border:1px solid #eee}
    #wl-qibushi-3 h3{font-size:21px;color:#47794f;font-weight:500;margin:30px 0 8px}
    #wl-qibushi-3 .wlq-audio{background:#f5efe4;padding:16px;border-radius:10px;margin:14px 0}
    #wl-qibushi-3 .wlq-audio strong{display:block;font-size:18px;margin-bottom:8px}
    #wl-qibushi-3 audio{display:block;width:100%;max-width:100%}
    #wl-qibushi-3 .wlq-bio{display:flex;gap:20px;align-items:flex-start}
    #wl-qibushi-3 .wlq-bio img{width:170px;max-width:38%;height:auto;object-fit:contain}
    #wl-qibushi-3 .wlq-bio p{margin-top:0}
    #wl-qibushi-3 .wlq-note{font-size:14px;color:#777}
    @media(max-width:600px){#wl-qibushi-3{padding:24px 16px}#wl-qibushi-3 .wlq-poem{font-size:20px}#wl-qibushi-3 .wlq-bio{display:block}#wl-qibushi-3 .wlq-bio img{display:block;max-width:75%;width:210px;margin:0 auto 15px}}
    </style>
    <h2 class="wlq-title">3. 七步诗</h2>
    <div class="wlq-author">三国 · 魏 · 曹植</div>
    <div class="wlq-poem">
      <p>煮豆持作羹，</p><p>漉菽以为汁。</p>
      <p>萁在釜下燃，</p><p>豆在釜中泣。</p>
      <p>本是同根生，</p><p>相煎何太急？</p>
    </div>
    <img class="wlq-pic" src="/poetry-assets/qibushi-story.webp" alt="用户提供的《七步诗》历史故事插图" loading="lazy">
    <div class="wlq-audio"><strong>▶ 听《七步诗》原诗朗诵</strong><audio controls preload="metadata" src="/poetry-assets/qibushi-recitation.m4a">浏览器不支持音频播放。</audio></div>
    <div class="wlq-audio"><strong>▶ 听《七步诗》译文讲解</strong><audio controls preload="metadata" src="/poetry-assets/qibushi-explanation.m4a">浏览器不支持音频播放。</audio></div>
    <h3>作者</h3>
    <div class="wlq-bio"><p>曹植（192—232），字子建，曹操之子，三国时期魏国文学家，以诗文才华著称，与曹操、曹丕合称“三曹”。他的作品情感充沛、辞采华美，代表了建安文学的重要成就。</p><img src="/poetry-assets/caozhi-portrait.webp" alt="用户提供的曹植人物画像" loading="lazy"></div>
    <h3>创作背景</h3>
    <p>相传曹丕即位后对曹植有所猜忌，命他在七步之内作诗。曹植以豆与豆萁本出同根、却互相煎熬的形象，表达骨肉相争的悲哀。七步成诗的故事广为流传，但其具体情节的史实性仍有争议。</p>
    <h3>诗意解读</h3>
    <p>煮豆做羹，过滤豆子取得汁液；豆萁在锅下燃烧，豆子在锅中仿佛哭泣。豆和豆萁本来生于同一根，为什么要如此急切地互相煎熬呢？诗人借物抒情，劝诫骨肉之间不应相互伤害。</p>
    <p class="wlq-note">录音为作者提供的原始音频，网页未进行声音合成。此页文字为网页配套介绍，录音内容以原文件为准。</p>
  `;
  const target=document.querySelector('main') || document.body;
  target.appendChild(section);
})();
