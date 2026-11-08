/* Weston Life: rotate the three TOP STORIES every 8 seconds.
   Does not touch visitor counters, storage, or article content. */
(function () {
  function init() {
    var container = document.querySelector('#wl-auto .wl-breaking .wl-features');
    if (!container || container.dataset.wlEightSecondCarousel === 'yes') return;
    var slides = Array.prototype.slice.call(container.querySelectorAll(':scope > .wl-feature'));
    if (slides.length < 2) return;
    container.dataset.wlEightSecondCarousel = 'yes';
    var style = document.createElement('style');
    style.textContent = '#wl-auto .wl-breaking .wl-features[data-wl-eight-second-carousel="yes"]{display:block!important;max-width:1000px;margin:auto}' +
      '#wl-auto .wl-breaking .wl-features[data-wl-eight-second-carousel="yes"]>.wl-feature{display:none!important}' +
      '#wl-auto .wl-breaking .wl-features[data-wl-eight-second-carousel="yes"]>.wl-feature.wl-current-slide{display:block!important}' +
      '#wl-auto .wl-breaking .wl-features[data-wl-eight-second-carousel="yes"]>.wl-feature img{height:clamp(240px,45vw,520px);object-fit:cover}' +
      '#wl-auto .wl-breaking .wl-features[data-wl-eight-second-carousel="yes"]>.wl-feature strong{font-size:clamp(22px,3vw,34px)}';
    document.head.appendChild(style);
    var current = 0;
    function show(i) {
      current = i;
      slides.forEach(function(slide, j) {
        var active = j === i;
        slide.classList.toggle('wl-current-slide', active);
        slide.setAttribute('aria-hidden', String(!active));
        slide.tabIndex = active ? 0 : -1;
      });
    }
    show(0);
    window.setInterval(function () { show((current + 1) % slides.length); }, 8000);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
