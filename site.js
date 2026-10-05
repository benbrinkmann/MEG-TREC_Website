/* ─── MEG-TREC — SHARED PAGE SCRIPT ─────────────────────────────────────────────
   Loaded at the end of every page. Each block checks that the elements it
   needs exist, so pages without (for example) a sidebar are unaffected.
   ─────────────────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // ── Mobile navigation toggle ──────────────────────────────────────────────
  const toggle = document.getElementById('navToggle');
  const links  = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const isOpen = links.classList.toggle('open');
      toggle.classList.toggle('open', isOpen);
      toggle.setAttribute('aria-expanded', String(isOpen));
    });
  }

  // ── Darken the navigation bar once the page has scrolled ──────────────────
  const nav = document.getElementById('nav');
  if (nav) {
    const updateNav = () => nav.classList.toggle('scrolled', window.scrollY > 60);
    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();
  }

  // ── Fade sections in as they enter the viewport ───────────────────────────
  // Older browsers without IntersectionObserver simply show everything.
  const fadeEls = document.querySelectorAll('.fade-in');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.08 });
    fadeEls.forEach(el => io.observe(el));
  } else {
    fadeEls.forEach(el => el.classList.add('visible'));
  }

  // ── Highlight the sidebar link for the section currently in view ──────────
  // Used on pages with a .sidebar-nav table of contents (e.g., meg.html).
  const groups    = document.querySelectorAll('.content-group[id]');
  const sideLinks = document.querySelectorAll('.sidebar-nav a');
  if (groups.length > 0 && sideLinks.length > 0 && 'IntersectionObserver' in window) {
    const sectionIO = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          sideLinks.forEach(a => {
            a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id);
          });
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    groups.forEach(g => sectionIO.observe(g));
  }
})();
