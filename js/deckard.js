/* deckard.js — small vanilla helpers for djdeckard.com (loaded with `defer`).
   Features: mobile nav drawer, gallery lightbox. */
(function () {
  'use strict';

  /* ---- Mobile nav drawer ---- */
  var toggle = document.querySelector('.nav-toggle');
  var drawer = document.getElementById('drawer');
  var closeBtn = drawer && drawer.querySelector('.drawer-close');

  function openDrawer() {
    if (!drawer) return;
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    document.body.classList.add('nav-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'true');
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('nav-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
  }
  if (toggle) toggle.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (drawer) drawer.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', closeDrawer);
  });

  /* ---- Gallery lightbox ---- */
  var lb = document.getElementById('lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    var tiles = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
    var srcs = tiles.map(function (t) {
      var img = t.querySelector('img');
      return t.getAttribute('data-full') || (img && img.getAttribute('src'));
    });
    var idx = 0;
    function show(i) { idx = (i + srcs.length) % srcs.length; lbImg.src = srcs[idx]; }
    function open(i) { show(i); lb.classList.add('open'); document.body.classList.add('nav-open'); }
    function close() { lb.classList.remove('open'); document.body.classList.remove('nav-open'); lbImg.src = ''; }

    tiles.forEach(function (t, i) {
      t.setAttribute('role', 'button');
      t.setAttribute('tabindex', '0');
      t.addEventListener('click', function () { open(i); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); }
      });
    });
    lb.querySelector('.lightbox__close').addEventListener('click', close);
    lb.querySelector('.lightbox__prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
    lb.querySelector('.lightbox__next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(idx - 1);
      else if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* Esc also closes the nav drawer */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeDrawer();
  });
})();
