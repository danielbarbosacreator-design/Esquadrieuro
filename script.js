/* ==========================================================================
   ESQUADRIEURO - ESQUADRIAS DE ALUMÍNIO E VIDRO TEMPERADO
   JavaScript Logic (Dynamic Calculations, WhatsApp Integration, Nav)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Header Sticky & Background Transition on Scroll
  const header = document.getElementById('header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // 2. Mobile Menu Toggle
  const mobileToggle = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  const navLinks = document.querySelectorAll('.nav-link');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
    });

    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
      });
    });
  }

  // 3. Active Link Highlight on Scroll
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');
      const activeLink = document.querySelector(`.nav-menu a[href*=${sectionId}]`);

      if (activeLink) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          activeLink.classList.add('active');
        } else {
          activeLink.classList.remove('active');
        }
      }
    });
  });

  // 4. Interactive Budget Estimator Calculator
  const calcForm = document.getElementById('calc-form');
  const calcMetragem = document.getElementById('calc-metragem');
  const calcProduto = document.getElementById('calc-produto');
  const calcResultText = document.getElementById('calc-result-text');

  // Base price table per m² in BRL
  const priceMap = {
    'Janelas de Alumínio': { min: 550, max: 780 },
    'Portas Minimalistas / Pivotantes': { min: 720, max: 1100 },
    'Fachada Pele de Vidro': { min: 850, max: 1350 },
    'Envidraçamento de Sacadas': { min: 480, max: 690 },
    'Projeto Completo (Janelas, Portas e Fachadas)': { min: 680, max: 980 }
  };

  function updateEstimate() {
    if (!calcMetragem || !calcProduto || !calcResultText) return;

    const area = parseFloat(calcMetragem.value) || 0;
    const prodKey = calcProduto.value;
    const rates = priceMap[prodKey] || { min: 600, max: 900 };

    if (area <= 0) {
      calcResultText.textContent = 'Informe a metragem aproximada';
      return;
    }

    const minTotal = Math.round(area * rates.min);
    const maxTotal = Math.round(area * rates.max);

    const minFormatted = minTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
    const maxFormatted = maxTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });

    calcResultText.textContent = `${minFormatted} — ${maxFormatted}`;
  }

  if (calcMetragem && calcProduto) {
    calcMetragem.addEventListener('input', updateEstimate);
    calcProduto.addEventListener('change', updateEstimate);
    updateEstimate(); // Initial call
  }

  // 5. Send Budget Form to WhatsApp
  if (calcForm) {
    calcForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const nome = document.getElementById('calc-nome').value.trim() || 'Cliente';
      const tipo = document.getElementById('calc-tipo').value;
      const produto = document.getElementById('calc-produto').value;
      const metragem = document.getElementById('calc-metragem').value;
      const estimativa = calcResultText.textContent;
      const obs = document.getElementById('calc-obs').value.trim();

      let msg = `*SOLICITAÇÃO DE ORÇAMENTO - SITE ESQUADRIEURO*\n\n`;
      msg += `👤 *Nome:* ${nome}\n`;
      msg += `🏗️ *Tipo de Projeto:* ${tipo}\n`;
      msg += `📦 *Solução Desejada:* ${produto}\n`;
      msg += `📐 *Área Estimada:* ${metragem} m²\n`;
      msg += `💰 *Estimativa do Simulador:* ${estimativa}\n`;
      if (obs) {
        msg += `📝 *Observações:* ${obs}\n`;
      }
      msg += `\n_Enviado através do site oficial Esquadrieuro (Fábrica Euroframes)_`;

      const encodedMsg = encodeURIComponent(msg);
      const whatsappUrl = `https://wa.me/5547984474374?text=${encodedMsg}`;

      window.open(whatsappUrl, '_blank');
    });
  }

  // 6. Direct Contact Form Handler
  const contactForm = document.getElementById('contact-direct-form');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('contact-name').value.trim();
      const email = document.getElementById('contact-email').value.trim();
      const message = document.getElementById('contact-msg').value.trim();

      let msg = `*CONTATO DIRETO - SITE ESQUADRIEURO*\n\n`;
      msg += `👤 *Nome:* ${name}\n`;
      msg += `📧 *E-mail:* ${email}\n`;
      msg += `💬 *Mensagem:* ${message}\n`;

      const encodedMsg = encodeURIComponent(msg);
      const whatsappUrl = `https://wa.me/5547984474374?text=${encodedMsg}`;

      window.open(whatsappUrl, '_blank');
    });
  }
});
