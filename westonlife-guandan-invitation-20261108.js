/* Weston Life independent invitation module. Does not read or modify visitor counters. */
(function () {
  'use strict';
  function init() {
    if (document.getElementById('wl-guandan-invite-2026')) return;
    var poems = document.getElementById('china-poems');
    if (!poems) return;
    var style = document.createElement('style');
    style.textContent = '#wl-guandan-invite-2026{max-width:1040px;margin:30px auto;padding:24px;background:#fffaf1;border:1px solid #ddd0bc;border-top:5px solid #365b47;border-radius:16px;text-align:center;color:#283e31;font-family:Georgia,"Songti SC",serif;box-sizing:border-box}#wl-guandan-invite-2026 *{box-sizing:border-box}#wl-guandan-invite-2026 .gd-tag{font:700 12px Arial,sans-serif;letter-spacing:.15em;color:#98613e}#wl-guandan-invite-2026 h2{font-size:clamp(27px,4vw,44px);line-height:1.25;margin:14px 0}#wl-guandan-invite-2026 img{display:block;width:100%;height:auto;border-radius:9px}#wl-guandan-invite-2026 p{font-size:17px;line-height:1.8}#wl-guandan-invite-2026 .gd-details{max-width:800px;margin:20px auto;text-align:left;background:#f4eee2;border-radius:10px;padding:16px 24px}#wl-guandan-invite-2026 .gd-details p{margin:6px 0}#wl-guandan-invite-2026 .gd-en{display:none}html[data-wl-lang="en"] #wl-guandan-invite-2026 .gd-zh{display:none}html[data-wl-lang="en"] #wl-guandan-invite-2026 .gd-en{display:block}@media(max-width:650px){#wl-guandan-invite-2026{margin:18px 12px;padding:13px}#wl-guandan-invite-2026 .gd-details{padding:12px}}';
    document.head.appendChild(style);
    var section = document.createElement('section');
    section.id = 'wl-guandan-invite-2026';
    section.innerHTML = '<div class="gd-tag">WESTON LIFE · COMMUNITY INVITATION</div>'+
      '<h2 class="gd-zh">Weston × Newton 掼蛋邀请赛 · 江湖高手召集令</h2>'+
      '<h2 class="gd-en">Weston × Newton Guandan Invitational · Players Wanted</h2>'+
      '<img src="/weston-newton-guandan-invitation.webp" alt="Weston Newton 掼蛋邀请赛，原创彩色铅笔手绘风格海报" loading="lazy" decoding="async">'+
      '<div class="gd-details gd-zh"><p><strong>赛事阵容：</strong>Newton 3队、6人；Weston 3队、6人，共12位选手。</p><p><strong>诚邀高手：</strong>欢迎Newton实力派选手及Weston自认为顶级、冠军级的掼蛋高手报名。报名后将进行选手资格确认与考核。</p><p><strong>冠军奖品：</strong>掼蛋自动发牌机，具体品牌及型号待定。</p><p><strong>比赛时间：</strong>暂定2026年12月初，具体日期与场地另行通知。</p><p><strong>报名：</strong>请直接联系组织者，或在微信群中联系我报名。即日起接受报名。</p><p style="font-size:13px;color:#805a43">提示：海报中“10月底截止报名”为旧文案，请以本公告的最新报名安排为准。</p></div>'+
      '<div class="gd-details gd-en"><p><strong>Teams:</strong> Three pairs (six players) each from Newton and Weston.</p><p><strong>Invitation:</strong> Experienced Newton players and self-described top Weston players are welcome. Final qualification review applies.</p><p><strong>Prize:</strong> Automatic Guandan card dealer; brand and model to be confirmed.</p><p><strong>When:</strong> Tentatively early December 2026; exact date and venue to follow.</p><p><strong>Register:</strong> Contact the organizer directly or through the WeChat group. Registration is open.</p><p style="font-size:13px">The outdated October deadline printed on the artwork is superseded by this announcement.</p></div>';
    poems.parentNode.insertBefore(section, poems);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true});
  else init();
})();
