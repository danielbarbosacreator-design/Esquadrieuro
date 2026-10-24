/* ==========================================================================
   ESQUADRIEURO — EFEITOS DE ROLAGEM (home e catálogo)
   Blocos surgem com animação suave e um desfoque fica na base da tela.
   ========================================================================== */

// Blocos que entram animados. Irmãos do mesmo grupo entram em sequência.
const REVEAL_SELECTORS = [
  '.hero-content',
  '.facts .fact',
  '.sec-head',
  '.showcase-card',
  '.obras-card',
  '.quote-intro',
  '.quote-form',
  '.split-media',
  '.split-text',
  '.map-container',
  '.diff-grid li',
  '.faq-intro',
  '.faq-item',
  '.catalog-header-bar',
  '.catalog-filter-tabs',
  '.cta-final-inner',
  '.footer-grid > div'
];

const REVEAL_STAGGER = 0.08; // segundos entre irmãos
const REVEAL_MAX_STEPS = 4;

function initScrollEffects() {
  const blocks = document.querySelectorAll(REVEAL_SELECTORS.join(','));
  blocks.forEach(el => {
    el.classList.add('reveal-up');
    const siblings = [...el.parentElement.children].filter(c => c.matches(REVEAL_SELECTORS.join(',')));
    const step = Math.min(siblings.indexOf(el), REVEAL_MAX_STEPS - 1);
    if (step > 0) el.style.setProperty('--reveal-delay', `${step * REVEAL_STAGGER}s`);
  });

  const revealEls = document.querySelectorAll('.reveal-up');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('revealed'));
  }

  // Desfoque na base: aparece depois de começar a rolar e some no fim da página
  const fade = document.createElement('div');
  fade.className = 'scroll-fade';
  fade.setAttribute('aria-hidden', 'true');
  document.body.appendChild(fade);

  const updateFade = () => {
    const scrolled = window.scrollY > 40;
    const atEnd = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 120;
    fade.classList.toggle('is-visible', scrolled && !atEnd);
  };
  window.addEventListener('scroll', updateFade, { passive: true });
  window.addEventListener('resize', updateFade);
  updateFade();
}
