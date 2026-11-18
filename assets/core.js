/* Shared navigation and motion. All essential content is available without JS. */
(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('js');
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const animations = new Set();
  const ease = 'cubic-bezier(.22,.7,.25,1)';

  function animate(element, frames, options = {}) {
    if (!element || preference.matches || !element.animate) return;
    const animation = element.animate(frames, { duration: 360, easing: ease, ...options });
    animations.add(animation);
    animation.finished.then(() => animations.delete(animation), () => animations.delete(animation));
    return animation;
  }
  window.siteMotion = { animate, reduced: () => preference.matches };
  preference.addEventListener('change', () => {
    if (preference.matches) animations.forEach(animation => animation.cancel());
  });
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

  const menu = document.querySelector('dialog.menu');
  const trigger = document.querySelector('[data-menu-toggle]');
  if (menu && trigger && typeof menu.showModal === 'function') {
    function closeMenu() { menu.close(); }
    trigger.addEventListener('click', () => {
      menu.showModal();
      trigger.setAttribute('aria-expanded', 'true');
      document.body.classList.add('menu-open');
      animate(menu, [{ transform: 'translateX(16px)', opacity: .8 }, { transform: 'none', opacity: 1 }], { duration: 240 });
    });
    menu.querySelector('[data-menu-close]').addEventListener('click', closeMenu);
    menu.addEventListener('keydown', event => {
      if (event.key !== 'Tab') return;
      const controls = [...menu.querySelectorAll('a[href], button:not(:disabled)')].filter(el => el.getClientRects().length);
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (event.shiftKey && (document.activeElement === first || document.activeElement === menu)) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
    menu.addEventListener('click', event => {
      // A backdrop click targets the dialog but falls outside its actual panel.
      if (event.target !== menu) return;
      const bounds = menu.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right) closeMenu();
    });
    menu.addEventListener('close', () => {
      trigger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('menu-open');
      trigger.focus({ preventScroll: true });
    });
    const desktop = window.matchMedia('(min-width: 1201px)');
    desktop.addEventListener('change', () => { if (desktop.matches && menu.open) closeMenu(); });
  } else {
    // An older browser still gets all navigation links.
    root.classList.remove('js');
  }

  const hero = document.querySelector('[data-hero]');
  if (hero) {
    // Text settles into place; the LCP photograph is painted from the first frame and only eases its scale.
    const copy = hero.querySelector('.hero-copy, .page-hero-copy, .project-hero-head');
    const parts = copy ? [...copy.children] : [];
    parts.slice(0, 5).forEach((part, index) => animate(part, [{ transform: 'translateY(14px)' }, { transform: 'none' }], { duration: 420, delay: index * 60, fill: 'backwards' }));
    const photo = hero.querySelector('.hero-photo > img, .page-hero-photo > img, .project-cover > img');
    animate(photo, [{ transform: 'scale(1.035)' }, { transform: 'none' }], { duration: 900 });
    animate(hero.querySelector('.hero-photo figcaption'), [{ transform: 'translateY(8px)', opacity: .6 }, { transform: 'none', opacity: 1 }], { duration: 420, delay: 260, fill: 'backwards' });
  }

  // Groups of cards enter once. The hidden state is set here, never in CSS, and only below the fold.
  const groups = [...document.querySelectorAll('[data-reveal]')];
  if (groups.length && 'IntersectionObserver' in window && !preference.matches && document.documentElement.animate) {
    const pending = new Set();
    const show = item => {
      if (!pending.delete(item)) return;
      item.style.opacity = '';
      item.style.transform = '';
    };
    const observer = new IntersectionObserver(entries => {
      let order = 0;
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        const item = entry.target;
        if (!pending.has(item)) return;
        const delay = Math.min(order++, 3) * 80;
        show(item);
        animate(item, [{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'none' }], { duration: 520, delay, fill: 'backwards' });
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    groups.forEach(group => [...group.children].forEach(item => {
      if (item.getBoundingClientRect().top < innerHeight * 0.94 || item.hidden) return;
      pending.add(item);
      item.style.opacity = '0';
      item.style.transform = 'translateY(16px)';
      observer.observe(item);
    }));
    const revealAll = () => [...pending].forEach(show);
    window.addEventListener('beforeprint', revealAll);
    preference.addEventListener('change', () => { if (preference.matches) revealAll(); });
    window.siteMotion.revealAll = revealAll;
  }

  // Keep the primary action useful when already on the contact page.
  const form = document.querySelector('[data-form-demo]');
  if (form) {
    form.id = 'richiesta';
    document.querySelectorAll('a[href="contatti.html"]').forEach(link => link.setAttribute('href', '#richiesta'));
  }
})();
