/* Weston Life | 诗词里的中国 · 第五首《敕勒歌》
   2026-11-19 | Additive enhancement for index.html AND poetry.html.
   Does not read, modify, hide or reset counter.js or visitor counts.
   Original first four poems and their media remain in poetry.html.
*/
(function () {
  'use strict';
  var PAGE = '/poetry.html#fifth';
  var COVER = '/assets/chilege-05.jpg';
  var POEM = '敕勒川，阴山下。天似穹庐，笼盖四野。天苍苍，野茫茫。风吹草低见牛羊。';
  var EXPLANATION = [
    '第五首，敕勒歌。南北朝乐府民歌。',
    '我们先来理解诗歌。敕勒川，阴山下，描绘的是阴山山脉脚下一望无际的草原。敕勒是古代生活在中国北方的民族名称。',
    '天似穹庐，笼盖四野。穹庐，是古代游牧民族居住的圆顶毡帐。诗人把天空比作巨大的帐篷，仿佛从四面八方笼罩着整个大草原。',
    '天苍苍，野茫茫。天空辽远，草原广阔，诗句通过重复的节奏，让我们仿佛置身天地之间。',
    '风吹草低见牛羊。风吹动高高的草，草伏下去，牛羊显露出来。这里的见，通常读作现，表示显现。诗歌从宏大的天地转向草原上的生命，使画面一下子活了起来。',
    '这首歌没有确切可考的个人作者，通常归为北朝民歌。有传统记载，把它与北齐名将斛律金吟唱草原歌曲的故事联系起来，但这不等于能够确定斛律金就是原作者。',
    '创作背景与中国古代北方的游牧生活有关。阴山及其附近的草原，是古代北方各族往来、放牧和生活的重要地区。民歌借天空、毡帐、草原和牛羊，留下了生动的文化记忆。',
    '这首诗的艺术特点，是语言短小，意境开阔。前两句交代地点，接着用穹庐比喻天空，再以苍苍、茫茫写天地之大，最后用风吹草低见牛羊，写出生机和惊喜。',
    '读完敕勒歌，我们看到的是辽阔的自然，更能感受到古代北方人们与草原共同生活的方式。这就是诗词里的中国，第五首。'
  ].join('');
  var speaking = false;
  var queue = [];
  var speechId = 0;

  function home() {
    var card = document.getElementById('china-poems');
    if (!card) return;
    var cover = card.querySelector('img');
    if (cover) {
      cover.src = COVER;
      cover.alt = '敕勒歌：阴山、蓝天、草原与牛羊的水彩画（取自读者提供的诗歌页面）';
      cover.style.objectFit = 'contain';
      cover.style.background = '#f7f3ea';
    }
    var notice = document.getElementById('wl-poetry-four-notice');
    if (!notice) {
      notice = document.createElement('p');
      notice.id = 'wl-poetry-four-notice'; // Reuse existing slot; do not create duplicate notices.
      notice.style.cssText = 'font-size:19px;line-height:1.7;font-weight:bold;color:#8b2929;background:#fff0df;border:1px solid #e4d0ba;border-radius:9px;padding:12px 18px;margin:19px auto;max-width:540px';
      var en = card.querySelector('h3');
      if (en) en.insertAdjacentElement('afterend', notice);
      else card.appendChild(notice);
    }
    notice.textContent = '今日更新 · 第五首《敕勒歌》｜南北朝乐府民歌';
    card.querySelectorAll('a').forEach(function (a) {
      var href = a.getAttribute('href') || '';
      if (/poetry\.html|qibushi\.html/.test(href)) {
        a.href = PAGE;
        a.textContent = href.indexOf('qibushi') !== -1 ? '今日第五首：《敕勒歌》 →' : '进入《诗词里的中国》· 学习第五首 →';
      }
    });
    if (cover && cover.closest('a')) cover.closest('a').href = PAGE;
  }

  function sayText(text, button, label) {
    if (!('speechSynthesis' in window)) {
      alert('此浏览器暂不支持中文语音朗读，请使用 iPhone Safari 或更新浏览器。');
      return;
    }
    // Same button toggles stop; a different button starts the requested recording.
    if (speaking && button.dataset.speaking === 'true') { stopSpeaking(); return; }
    stopSpeaking();
    var id = ++speechId;
    speaking = true;
    button.dataset.speaking = 'true';
    button.textContent = '■ 停止' + label;
    var synth = window.speechSynthesis;
    var voices = synth.getVoices();
    var chinese = voices.filter(function(v){return /^zh(-|_)/i.test(v.lang) || /^zh$/i.test(v.lang);});
    var voice = chinese.find(function(v){return /Tingting|Meijia|Xiaoxiao|Mandarin|Chinese|普通话/i.test(v.name);}) || chinese[0] || null;
    queue = text.match(/[^。！？；]+[。！？；]?/g) || [text];
    function next() {
      if (id !== speechId) return;
      var part = queue.shift();
      if (!part) { stopSpeaking(); return; }
      var utterance = new SpeechSynthesisUtterance(part);
      utterance.lang = 'zh-CN';
      if (voice) utterance.voice = voice;
      utterance.rate = label === '诗歌朗诵' ? 0.76 : 0.88;
      utterance.pitch = 1;
      utterance.onend = next;
      utterance.onerror = function(e) {
        if (id !== speechId) return;
        if (e.error === 'interrupted' || e.error === 'canceled') return;
        stopSpeaking();
      };
      synth.speak(utterance);
    }
    next();
  }
  function stopSpeaking() {
    speechId++;
    queue = [];
    speaking = false;
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    document.querySelectorAll('.wl-five-audio-btn').forEach(function(b) {
      b.dataset.speaking = 'false';
      b.textContent = '▶ 播放' + b.dataset.label;
    });
  }
  function audioPanel(title, id, text, hint) {
    return '<section class="audio-panel"><h3>' + title + '</h3>' +
      '<button type="button" class="wl-five-audio-btn" id="' + id + '"' +
      ' style="display:block;max-width:360px;width:100%;background:#365b47;color:#fff;border:0;border-radius:8px;padding:13px 16px;font:600 17px Arial,sans-serif;cursor:pointer"' +
      ' data-label="' + text + '">▶ 播放' + text + '</button>' +
      '<p>' + hint + '</p></section>';
  }
  function poetryPage() {
    var fourth = document.getElementById('fourth');
    if (!fourth || document.getElementById('fifth')) return;
    document.title = '诗词里的中国｜第五首《敕勒歌》｜Weston Life';
    var description = document.querySelector('meta[name="description"]');
    if (description) description.content = '诗词里的中国：第五首《敕勒歌》，原文、拼音、朗诵、译文、作者、创作背景及赏析；第一至第四首保留在历史目录。';
    var update = document.querySelector('.update');
    if (update) update.textContent = '2026年11月19日 · 今日更新第五首';
    // The previous featured poem remains intact and accessible as a historical entry.
    fourth.classList.remove('feature');
    fourth.classList.add('archive');
    var originalTag = fourth.querySelector('.tag');
    if (originalTag) originalTag.textContent = '历史第四首 · POEM 04 · 东晋末至南朝宋初';
    var fifth = document.createElement('article');
    fifth.id = 'fifth';
    fifth.className = 'feature';
    fifth.innerHTML =
      '<p class="tag">第五首 · POEM 05 · 南北朝乐府民歌</p>' +
      '<h2 class="poem-title">敕勒歌</h2><p class="by">北朝民歌 · 作者不详</p>' +
      '<figure class="poem-art"><img src="' + COVER + '" alt="阴山脚下的敕勒草原：青山、蓝天、绿草和牛羊，取自提供的书页插画" style="object-fit:contain;aspect-ratio:auto;background:#fff" decoding="async"><figcaption>天苍苍，野茫茫。风吹草低见牛羊。</figcaption></figure>' +
      audioPanel('一、诗词朗诵 · 听原诗','wl-five-recitation','诗歌朗诵','使用手机内置中文语音朗读，不是预录 MP3；无需上传音频文件。') +
      '<div class="lines">' +
      '<p><span class="pinyin">chì lè chuān，yīn shān xià。</span>敕勒川，阴山下。</p>' +
      '<p><span class="pinyin">tiān sì qióng lú，lǒng gài sì yě。</span>天似穹庐，笼盖四野。</p>' +
      '<p><span class="pinyin">tiān cāng cāng，yě máng máng。</span>天苍苍，野茫茫。</p>' +
      '<p><span class="pinyin">fēng chuī cǎo dī xiàn niú yáng。</span>风吹草低见牛羊。</p>' +
      '</div>' +
      '<h3>二、译文</h3><p>敕勒族生活的辽阔平原位于阴山脚下。天空像一顶巨大的圆形毡帐，笼罩着四面八方。天空苍茫，草原广阔无边。微风吹过，高草低伏，露出了成群的牛羊。</p>' +
      '<h3>三、作者与来源</h3><p>《敕勒歌》是流传下来的北朝民歌，作者不详。它与古代敕勒族的草原生活传统联系密切。史书中有斛律金吟唱这首歌的记载，但不能据此认定他是原作者。</p>' +
      '<h3>四、创作背景</h3><p>南北朝时期，中国北方的草原与农耕地区有密切往来。阴山脚下的辽阔草原，是许多北方民族放牧与生活的地方。这首民歌以天空、穹庐、草地和牛羊，展现北方游牧生活的自然风貌。后世也有关于北齐军中传唱此歌的故事，具体成歌年代与作者仍无定论。</p>' +
      '<h3>五、字词与意境赏析</h3><p><strong>敕勒川</strong>：古代北方敕勒族生活的平原。<strong>阴山</strong>：中国北方的山脉。<strong>穹庐</strong>：圆顶毡帐。<strong>四野</strong>：四面八方。<strong>见</strong>：在这里表示显现，常读 xiàn。</p>' +
      '<p>诗歌先写地点，再以“穹庐”比喻天空，以“苍苍”“茫茫”写天地的广大；最后“风吹草低见牛羊”让静态景色有了生命与动感。寥寥数句，便写出了古代中国北方草原的雄浑与丰饶。</p>' +
      audioPanel('六、全篇讲解 · 听译文、作者、背景与赏析','wl-five-explanation','全篇讲解','包含译文、作者与来源、历史背景、关键词及意境赏析；使用手机内置中文语音。') +
      '<h3>七、原图来源</h3><p class="muted">插图截取自你提供的《敕勒歌》书页照片。已按画面裁剪，不改动前四首原图和原有音频。</p>' +
      '<p class="back"><a href="#catalog">查看目录与历史诗歌 ↓</a></p>';
    fourth.parentNode.insertBefore(fifth, fourth);

    var toc = document.querySelector('#catalog .toc');
    if (toc && !toc.querySelector('a[href="#fifth"]')) {
      var link = document.createElement('a');
      link.href = '#fifth';
      link.innerHTML = '<strong>第五首 · 敕勒歌</strong><span>北朝乐府民歌 · 今日更新</span>';
      toc.insertBefore(link, toc.firstChild);
      var previous = toc.querySelector('a[href="#fourth"]');
      if (previous) previous.innerHTML = '<strong>第四首 · 饮酒（其五）</strong><span>陶渊明 · 历史第四首</span>';
    }
    var oldBack = fourth.querySelector('.back a');
    if (oldBack) oldBack.textContent = '查看目录与历史诗歌 ↓';
    var poemButton = document.getElementById('wl-five-recitation');
    var explanationButton = document.getElementById('wl-five-explanation');
    if (poemButton) poemButton.addEventListener('click', function(){ sayText(POEM,poemButton,'诗歌朗诵'); });
    if (explanationButton) explanationButton.addEventListener('click', function(){ sayText(EXPLANATION,explanationButton,'全篇讲解'); });
    window.addEventListener('pagehide', stopSpeaking);
  }

  function init() { home(); poetryPage(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
