/* ==========================================================================
   ESQUADRIEURO - ESQUADRIAS, LOJA & CATÁLOGO DINÂMICO
   Script de Interatividade, Catálogo em Tempo Real e Painel Administrativo
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  // ==========================================================================
  // 0. SCROLL REVEAL (IntersectionObserver)
  // ==========================================================================
  renderObras();
  initQuoteForm();
  initScrollEffects();

  // ==========================================================================
  // 1. ESTADO & STORAGE LOCAL (PRODUTOS, SÓCIOS E CATÁLOGO)
  // ==========================================================================
  const CATALOG_VERSION = '2025_v4_pdf_official';
  const STORAGE_KEYS = {
    VERSION: 'esquadrieuro_catalog_version',
    PRODUCTS: 'esquadrieuro_products_official_2025',
    FOUNDERS: 'esquadrieuro_founders_v3',
    PDF_LINK: 'esquadrieuro_pdf_link_v2',
    AUTH: 'esquadrieuro_admin_auth'
  };

  const INITIAL_FOUNDERS = {
    image: 'assets/images/proprietarios.jpg?v=2026_v1',
    quote: 'Não entregamos apenas esquadrias; entregamos segurança, estanqueidade e o conforto visual que transforma uma obra em um verdadeiro lar.',
    bio: 'Na Esquadrieuro, você conta com o acompanhamento direto dos próprios fundadores. Desde o alinhamento da planta arquitetônica com engenheiros e arquitetos até a conferência milimétrica das folgas e a instalação final, nossa diretoria garante que nenhum detalhe seja deixado ao acaso.'
  };

  // Limpa caches antigos para garantir fidelidade de 100% ao Catálogo Oficial e fotos atualizadas
  try {
    ['esquadrieuro_products', 'esquadrieuro_products_v2', 'esquadrieuro_products_v2025', 'esquadrieuro_products_official_2025', 'esquadrieuro_founders_v2'].forEach(k => localStorage.removeItem(k));
  } catch(e) {}

  // Carrega produtos ou inicia com catálogo padrão
  function getProducts() {
    return typeof INITIAL_CATALOG !== 'undefined' ? [...INITIAL_CATALOG] : [];
  }

  function saveProducts(products) {
    localStorage.setItem(STORAGE_KEYS.PRODUCTS, JSON.stringify(products));
    renderCatalog();
    renderAdminProductsList();
  }

  // Carrega dados dos fundadores
  function getFounders() {
    try {
      const stored = localStorage.getItem(STORAGE_KEYS.FOUNDERS);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (e) {
      console.error('Erro ao ler fundadores', e);
    }
    return typeof INITIAL_FOUNDERS !== 'undefined' ? { ...INITIAL_FOUNDERS } : null;
  }

  function saveFounders(founders) {
    localStorage.setItem(STORAGE_KEYS.FOUNDERS, JSON.stringify(founders));
    renderFoundersSection();
  }

  // Toast Helper
  function showToast(message) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.style.display = 'block';
    setTimeout(() => {
      toast.style.display = 'none';
    }, 3200);
  }

  // ==========================================================================
  // 2. NAVEGAÇÃO, HEADER SCROLL & MOBILE MENU
  // ==========================================================================
  const header = document.getElementById('header');
  const mobileToggle = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  const navLinks = document.querySelectorAll('.nav-link');

  // Efeito glassmorphism e compactação do header ao rolar
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }

    // Link ativo de navegação
    // Apenas um link ativo: a última seção cujo topo já passou do header
    const scrollY = window.pageYOffset + 140;
    let currentId = null;
    document.querySelectorAll('section[id]').forEach(section => {
      if (section.offsetTop <= scrollY) currentId = section.id;
    });
    navLinks.forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === `#${currentId}`);
    });
  });

  // Toggle do menu mobile
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

  // ==========================================================================
  // 3. FAQ ACCORDION
  // ==========================================================================
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    if (questionBtn) {
      questionBtn.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');
        faqItems.forEach(i => i.classList.remove('open'));
        if (!isOpen) {
          item.classList.add('open');
        }
      });
    }
  });

  // ==========================================================================
  // 4. RENDERIZAÇÃO DA SEÇÃO FUNDADORES
  // ==========================================================================
  function renderFoundersSection() {
    const founders = getFounders();
    if (!founders) return;

    const imgEl = document.getElementById('founders-display-img');
    const quoteEl = document.getElementById('founders-quote');
    const bioEl = document.getElementById('founders-bio');

    if (imgEl && founders.image) imgEl.src = founders.image;
    if (quoteEl && founders.quote) quoteEl.textContent = `“${founders.quote}”`;
    if (bioEl && founders.bio) bioEl.textContent = founders.bio;
  }
  renderFoundersSection();

  // ==========================================================================
  // 5. MOTOR DO CATÁLOGO DE PRODUTOS (FILTROS, BUSCA, 3 FILEIRAS & EXPANSÃO)
  // ==========================================================================
  const catalogContainer = document.getElementById('catalog-container');
  const catalogSearch = document.getElementById('catalog-search');
  const categoryTabs = document.querySelectorAll('.cat-tab-btn');
  const expandFooter = document.getElementById('catalog-expand-footer');
  const countBadge = document.getElementById('catalog-count-badge');
  const btnToggleExpand = document.getElementById('btn-toggle-expand-catalog');
  const btnExpandText = document.getElementById('btn-expand-text');

  const ROW_LIMIT = 12; // 3 fileiras (4 colunas x 3 = 12 produtos)
  let currentCategory = 'all';
  let searchQuery = '';
  let isCatalogExpanded = false;

  function renderCatalog() {
    if (!catalogContainer) return;
    const products = getProducts();

    // Filtragem por Categoria e Busca
    const filtered = products.filter(item => {
      const matchCat = (currentCategory === 'all') || (item.category === currentCategory);
      const q = searchQuery.toLowerCase().trim();
      const matchSearch = !q || (
        (item.title && item.title.toLowerCase().includes(q)) ||
        (item.code && item.code.toLowerCase().includes(q)) ||
        (item.line && item.line.toLowerCase().includes(q)) ||
        (item.description && item.description.toLowerCase().includes(q))
      );
      return matchCat && matchSearch;
    });

    if (filtered.length === 0) {
      catalogContainer.innerHTML = `
        <div class="catalog-empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <h3>Nenhum produto encontrado</h3>
          <p>Tente buscar por outro termo ou selecione "Todos os Produtos".</p>
        </div>
      `;
      if (expandFooter) expandFooter.style.display = 'none';
      return;
    }

    if (expandFooter) expandFooter.style.display = 'flex';

    // Determina quais produtos exibir com base no estado de expansão
    const displayProducts = isCatalogExpanded ? filtered : filtered.slice(0, ROW_LIMIT);

    // Atualiza badges e botões de expansão
    if (countBadge) {
      if (isCatalogExpanded) {
        countBadge.textContent = `Mostrando todos os ${filtered.length} produtos`;
      } else {
        const showing = Math.min(ROW_LIMIT, filtered.length);
        countBadge.textContent = `Mostrando ${showing} de ${filtered.length} produtos`;
      }
    }

    if (btnToggleExpand) {
      if (filtered.length <= ROW_LIMIT) {
        btnToggleExpand.style.display = 'none';
      } else {
        btnToggleExpand.style.display = 'inline-flex';
        if (isCatalogExpanded) {
          btnToggleExpand.classList.add('is-expanded');
          if (btnExpandText) btnExpandText.textContent = 'Mostrar menos';
        } else {
          btnToggleExpand.classList.remove('is-expanded');
          const remaining = filtered.length - ROW_LIMIT;
          if (btnExpandText) btnExpandText.textContent = `Ver mais ${remaining} produtos`;
        }
      }
    }

    catalogContainer.innerHTML = displayProducts.map(item => {
      const codeDisplay = item.code ? `Cód. ${item.code}` : '';
      const badgeDisplay = item.badge ? `<span class="product-badge-tag">${item.badge}</span>` : '';
      const lineDisplay = item.line ? `<div class="product-line-tag">${item.line}</div>` : '';
      const whatsappMsg = encodeURIComponent(`Olá! Gostaria de cotar o produto "${item.title}" (Código: ${item.code || 'S/N'}) do catálogo da Esquadrieuro.`);
      const whatsappUrl = `https://wa.me/5547984474374?text=${whatsappMsg}`;

      return `
        <div class="product-card-modern" data-id="${item.id}">
          <div class="product-thumb">
            <img src="${item.image ? (item.image + '?v=4') : 'assets/images/janelas.png'}" alt="${item.title}" loading="lazy">
            ${badgeDisplay}
          </div>
          <div class="product-body">
            <div class="product-header-meta">
              ${lineDisplay}
              ${codeDisplay ? `<span class="product-code-pill">${codeDisplay}</span>` : ''}
            </div>
            <h4 class="product-name">${item.title}</h4>
            <p class="product-excerpt">${item.description || ''}</p>
            <div class="product-footer-actions">
              <button class="btn-ver-detalhes" data-action="detail" data-id="${item.id}">Detalhes</button>
              <a href="${whatsappUrl}" target="_blank" class="btn-cotar-prod">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-1.043 3.804 3.786-.992z"/></svg>
                Cotar
              </a>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Eventos de clique para abrir modal de detalhes
    catalogContainer.querySelectorAll('[data-action="detail"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const prodId = e.currentTarget.getAttribute('data-id');
        openProductModal(prodId);
      });
    });
  }

  // Toggle de expansão
  if (btnToggleExpand) {
    btnToggleExpand.addEventListener('click', () => {
      isCatalogExpanded = !isCatalogExpanded;
      renderCatalog();
      if (!isCatalogExpanded) {
        const target = document.getElementById('produtos');
        if (target) {
          const top = target.getBoundingClientRect().top + window.pageYOffset - 90;
          window.scrollTo({ top, behavior: 'smooth' });
        }
      }
    });
  }

  // Eventos de filtro por aba
  categoryTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      categoryTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentCategory = tab.getAttribute('data-category');
      isCatalogExpanded = false; // reseta ao mudar categoria para sempre ver as 3 fileiras primeiro
      renderCatalog();
    });
  });

  // Evento de busca em tempo real
  if (catalogSearch) {
    catalogSearch.addEventListener('input', (e) => {
      searchQuery = e.target.value;
      isCatalogExpanded = false;
      renderCatalog();
    });
  }

  // Render inicial do catálogo
  renderCatalog();

  // ==========================================================================
  // 6. MODAL DE DETALHES DO PRODUTO
  // ==========================================================================
  const productModal = document.getElementById('product-detail-modal');
  const closeProductModalBtn = document.getElementById('close-product-modal');

  function openProductModal(productId) {
    const products = getProducts();
    const product = products.find(p => p.id === productId);
    if (!product || !productModal) return;

    document.getElementById('modal-product-image').src = product.image ? (product.image + '?v=4') : 'assets/images/janelas.png';
    document.getElementById('modal-product-code').textContent = product.code ? `Código ${product.code}` : 'Sob medida';
    document.getElementById('modal-product-name').textContent = product.title;
    document.getElementById('modal-product-desc').textContent = product.description || '';

    // Cores
    const colorsWrap = document.getElementById('modal-product-colors');
    if (product.colors && product.colors.length > 0) {
      colorsWrap.innerHTML = product.colors.map(c => `<span class="color-chip">${c}</span>`).join('');
      document.getElementById('modal-colors-wrap').style.display = 'block';
    } else {
      document.getElementById('modal-colors-wrap').style.display = 'none';
    }

    // Link WhatsApp
    const msg = encodeURIComponent(`Olá! Gostaria de mais detalhes e cotação para o produto "${product.title}" (Código: ${product.code || 'S/N'}) do catálogo da Esquadrieuro.`);
    document.getElementById('modal-whatsapp-btn').href = `https://wa.me/5547984474374?text=${msg}`;

    productModal.showModal();
  }

  if (closeProductModalBtn) {
    closeProductModalBtn.addEventListener('click', () => {
      productModal.close();
    });
  }

  if (productModal) {
    productModal.addEventListener('click', (e) => {
      const rect = productModal.getBoundingClientRect();
      const isInDialog = (rect.top <= e.clientY && e.clientY <= rect.top + rect.height &&
        rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
      if (!isInDialog) {
        productModal.close();
      }
    });
  }

  // Botão Download Catálogo PDF
  const downloadCatalogBtn = document.getElementById('btn-download-catalog');
  if (downloadCatalogBtn) {
    downloadCatalogBtn.addEventListener('click', () => {
      const savedLink = localStorage.getItem(STORAGE_KEYS.PDF_LINK);
      if (savedLink) {
        window.open(savedLink, '_blank');
      } else {
        window.open('assets/catalogo-esquadrieuro-2025.pdf', '_blank');
      }
    });
  }

  // ==========================================================================
  // 7. PAINEL ADMINISTRATIVO (LOGIN, GESTÃO DE PRODUTOS, SÓCIOS E PDF)
  // ==========================================================================
  const adminModal = document.getElementById('admin-modal');
  const openAdminBtn = document.getElementById('open-admin-btn');
  const footerAdminBtn = document.getElementById('footer-admin-btn');
  const closeAdminModal = document.getElementById('close-admin-modal');
  const adminLoginForm = document.getElementById('admin-login-form');
  const adminLoginScreen = document.getElementById('admin-login-screen');
  const adminDashboardScreen = document.getElementById('admin-dashboard-screen');
  const adminLogoutBtn = document.getElementById('admin-logout-btn');

  function openAdmin() {
    if (!adminModal) return;
    const isAuth = sessionStorage.getItem(STORAGE_KEYS.AUTH) === 'true';
    if (isAuth) {
      showDashboard();
    } else {
      showLogin();
    }
    adminModal.showModal();
  }

  function showLogin() {
    adminLoginScreen.style.display = 'block';
    adminDashboardScreen.style.display = 'none';
  }

  function showDashboard() {
    adminLoginScreen.style.display = 'none';
    adminDashboardScreen.style.display = 'block';
    renderAdminProductsList();
    populateAdminFoundersForm();
  }

  if (openAdminBtn) openAdminBtn.addEventListener('click', openAdmin);
  if (footerAdminBtn) footerAdminBtn.addEventListener('click', openAdmin);
  if (closeAdminModal) closeAdminModal.addEventListener('click', () => adminModal.close());

  // Login
  if (adminLoginForm) {
    adminLoginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('admin-email').value.trim();
      const pass = document.getElementById('admin-pass').value.trim();

      // Autenticação administrativa
      if ((email === 'admin@esquadrieuro.com.br' || email.includes('admin')) && (pass === 'admin123' || pass === '123456')) {
        sessionStorage.setItem(STORAGE_KEYS.AUTH, 'true');
        showToast('Login efetuado com sucesso!');
        showDashboard();
      } else {
        alert('Credenciais incorretas! Tente a senha padrão: admin123');
      }
    });
  }

  // Logout
  if (adminLogoutBtn) {
    adminLogoutBtn.addEventListener('click', () => {
      sessionStorage.removeItem(STORAGE_KEYS.AUTH);
      showLogin();
      showToast('Desconectado do painel');
    });
  }

  // Tabs do Painel Admin
  const adminTabs = document.querySelectorAll('.admin-tab-btn');
  const adminTabContents = document.querySelectorAll('.admin-tab-content');
  adminTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      adminTabs.forEach(t => t.classList.remove('active'));
      adminTabContents.forEach(c => c.style.display = 'none');
      tab.classList.add('active');
      const target = document.getElementById(tab.getAttribute('data-tab'));
      if (target) target.style.display = 'block';
    });
  });

  // Lista de produtos no painel
  function renderAdminProductsList() {
    const listEl = document.getElementById('admin-products-list');
    const countEl = document.getElementById('admin-prod-count');
    if (!listEl) return;

    const products = getProducts();
    if (countEl) countEl.textContent = products.length;

    listEl.innerHTML = products.map(prod => `
      <div class="admin-product-item" data-id="${prod.id}">
        <img class="admin-prod-thumb" src="${prod.image || 'assets/images/janelas.png'}" alt="${prod.title}">
        <div class="admin-prod-info">
          <h5>${prod.title}</h5>
          <div class="admin-prod-meta">
            <strong>Cód:</strong> ${prod.code || '-'} | <strong>Cat:</strong> ${prod.category} | <strong>Linha:</strong> ${prod.line || '-'}
          </div>
        </div>
        <div class="admin-actions">
          <button class="btn-icon-admin" data-action="edit" data-id="${prod.id}" title="Editar">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
          </button>
          <button class="btn-icon-admin delete" data-action="delete" data-id="${prod.id}" title="Excluir">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
          </button>
        </div>
      </div>
    `).join('');

    // Eventos dos botões de editar e excluir
    listEl.querySelectorAll('[data-action="edit"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        editProduct(id);
      });
    });

    listEl.querySelectorAll('[data-action="delete"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        deleteProduct(id);
      });
    });
  }

  // Formulário de Adicionar / Editar Produto
  const productForm = document.getElementById('admin-product-form');
  const btnShowAddProduct = document.getElementById('btn-show-add-product');
  const btnCancelProdForm = document.getElementById('btn-cancel-prod-form');

  if (btnShowAddProduct) {
    btnShowAddProduct.addEventListener('click', () => {
      productForm.reset();
      document.getElementById('prod-edit-id').value = '';
      document.getElementById('prod-current-image').value = '';
      document.getElementById('form-product-title').textContent = 'Cadastrar Novo Produto no Catálogo';
      productForm.style.display = 'block';
    });
  }

  if (btnCancelProdForm) {
    btnCancelProdForm.addEventListener('click', () => {
      productForm.style.display = 'none';
      productForm.reset();
    });
  }

  function editProduct(id) {
    const products = getProducts();
    const prod = products.find(p => p.id === id);
    if (!prod) return;

    document.getElementById('prod-edit-id').value = prod.id;
    document.getElementById('prod-code').value = prod.code || '';
    document.getElementById('prod-category').value = prod.category || 'esquadrias';
    document.getElementById('prod-title').value = prod.title || '';
    document.getElementById('prod-line').value = prod.line || '';
    document.getElementById('prod-badge').value = prod.badge || '';
    document.getElementById('prod-colors').value = (prod.colors || []).join(', ');
    document.getElementById('prod-desc').value = prod.description || '';
    document.getElementById('prod-current-image').value = prod.image || '';

    document.getElementById('form-product-title').textContent = `Editar Produto: ${prod.title}`;
    productForm.style.display = 'block';
    productForm.scrollIntoView({ behavior: 'smooth' });
  }

  function deleteProduct(id) {
    if (confirm('Tem certeza de que deseja excluir este produto do catálogo?')) {
      let products = getProducts();
      products = products.filter(p => p.id !== id);
      saveProducts(products);
      showToast('Produto excluído com sucesso!');
    }
  }

  if (productForm) {
    productForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const editId = document.getElementById('prod-edit-id').value;
      const code = document.getElementById('prod-code').value.trim();
      const category = document.getElementById('prod-category').value;
      const title = document.getElementById('prod-title').value.trim();
      const line = document.getElementById('prod-line').value.trim();
      const badge = document.getElementById('prod-badge').value.trim();
      const colorsStr = document.getElementById('prod-colors').value.trim();
      const description = document.getElementById('prod-desc').value.trim();
      const currentImg = document.getElementById('prod-current-image').value;
      const fileInput = document.getElementById('prod-image-file');

      const colors = colorsStr ? colorsStr.split(',').map(c => c.trim()).filter(Boolean) : [];

      function finalizeSave(imageUrl) {
        let products = getProducts();

        if (editId) {
          // Edição
          const index = products.findIndex(p => p.id === editId);
          if (index !== -1) {
            products[index] = {
              ...products[index],
              code,
              category,
              title,
              line,
              badge,
              colors,
              description,
              image: imageUrl || products[index].image
            };
          }
          showToast('Produto atualizado com sucesso!');
        } else {
          // Novo
          const newProduct = {
            id: 'prod_' + Date.now(),
            code,
            category,
            title,
            line,
            badge,
            colors,
            description,
            image: imageUrl || 'assets/images/janelas.png'
          };
          products.unshift(newProduct);
          showToast('Novo produto cadastrado no catálogo!');
        }

        saveProducts(products);
        productForm.reset();
        productForm.style.display = 'none';
      }

      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (event) {
          finalizeSave(event.target.result);
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        finalizeSave(currentImg);
      }
    });
  }

  // ABA SÓCIOS / FUNDADORES
  const foundersForm = document.getElementById('admin-founders-form');
  function populateAdminFoundersForm() {
    const f = getFounders();
    if (!f) return;
    const namesEl = document.getElementById('founders-names');
    const quoteEl = document.getElementById('founders-quote-input');
    const bioEl = document.getElementById('founders-bio-input');

    if (namesEl) namesEl.value = f.names || '';
    if (quoteEl) quoteEl.value = f.quote || '';
    if (bioEl) bioEl.value = f.bio || '';
  }

  if (foundersForm) {
    foundersForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const f = getFounders() || {};
      f.names = document.getElementById('founders-names').value.trim();
      f.quote = document.getElementById('founders-quote-input').value.trim();
      f.bio = document.getElementById('founders-bio-input').value.trim();

      const fileInput = document.getElementById('founders-image-file');
      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (event) {
          f.image = event.target.result;
          saveFounders(f);
          showToast('Dados e foto dos proprietários atualizados!');
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        saveFounders(f);
        showToast('Dados dos proprietários atualizados com sucesso!');
      }
    });
  }

  // ABA PDF DO CATÁLOGO
  const pdfForm = document.getElementById('admin-pdf-form');
  if (pdfForm) {
    const savedLink = localStorage.getItem(STORAGE_KEYS.PDF_LINK);
    if (savedLink) {
      document.getElementById('catalog-pdf-link').value = savedLink;
    }

    pdfForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const link = document.getElementById('catalog-pdf-link').value.trim();
      const pdfFileInput = document.getElementById('catalog-pdf-file');

      if (pdfFileInput.files && pdfFileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (event) {
          localStorage.setItem(STORAGE_KEYS.PDF_LINK, event.target.result);
          showToast('Arquivo PDF do catálogo carregado com sucesso!');
        };
        reader.readAsDataURL(pdfFileInput.files[0]);
      } else if (link) {
        localStorage.setItem(STORAGE_KEYS.PDF_LINK, link);
        showToast('Link do PDF atualizado com sucesso!');
      }
    });
  }

  // ABA BACKUP E RESTAURAÇÃO
  const btnExport = document.getElementById('btn-export-backup');
  const btnRestore = document.getElementById('btn-restore-default');

  if (btnExport) {
    btnExport.addEventListener('click', () => {
      const data = {
        products: getProducts(),
        founders: getFounders(),
        pdfLink: localStorage.getItem(STORAGE_KEYS.PDF_LINK),
        exportedAt: new Date().toISOString()
      };
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `backup-catalogo-esquadrieuro-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
      showToast('Backup exportado com sucesso!');
    });
  }

  if (btnRestore) {
    btnRestore.addEventListener('click', () => {
      if (confirm('Atenção: Isso redefinirá todos os produtos e informações para o padrão de fábrica oficial. Deseja continuar?')) {
        localStorage.removeItem(STORAGE_KEYS.PRODUCTS);
        localStorage.removeItem(STORAGE_KEYS.FOUNDERS);
        localStorage.removeItem(STORAGE_KEYS.PDF_LINK);
        renderCatalog();
        renderAdminProductsList();
        renderFoundersSection();
        showToast('Catálogo de fábrica restaurado com sucesso!');
      }
    });
  }

});

// ==========================================================================
// OBRAS ENTREGUES (dados em obras-data.js)
// ==========================================================================
function renderObras() {
  const grid = document.getElementById('obras-grid');
  if (!grid || typeof OBRAS === 'undefined') return;

  const section = document.getElementById('obras');
  if (!OBRAS.length) {
    if (section) section.hidden = true;
    return;
  }

  grid.innerHTML = OBRAS.map(obra => `
    <article class="obras-card">
      <div class="obras-img">
        <img src="${obra.foto}" alt="${obra.titulo}, ${obra.cidade}" loading="lazy">
        ${obra.exemplo ? '<span class="obras-sample">Foto ilustrativa</span>' : ''}
      </div>
      <p class="obras-meta">${obra.tipo} · ${obra.cidade}</p>
      <h3>${obra.titulo}</h3>
      ${obra.linha ? `<p class="obras-line">${obra.linha}</p>` : ''}
    </article>
  `).join('');
}

// ==========================================================================
// FORMULÁRIO DE ORÇAMENTO → abre o WhatsApp com a mensagem pronta
// ==========================================================================
const QUOTE_WHATSAPP = '5547984474374';

function initQuoteForm() {
  const form = document.getElementById('quote-form');
  if (!form) return;

  const nome = form.querySelector('#q-nome');
  const nomeError = form.querySelector('#q-nome-error');
  const itensError = form.querySelector('#q-itens-error');
  const getItens = () => [...form.querySelectorAll('input[name="itens"]:checked')].map(i => i.value);

  const showError = (field, errorEl, show) => {
    errorEl.classList.toggle('is-visible', show);
    if (field) field.setAttribute('aria-invalid', show ? 'true' : 'false');
  };

  nome.addEventListener('input', () => { if (nome.value.trim()) showError(nome, nomeError, false); });
  form.querySelectorAll('input[name="itens"]').forEach(box => {
    box.addEventListener('change', () => { if (getItens().length) showError(null, itensError, false); });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const itens = getItens();
    const nomeOk = nome.value.trim().length > 0;
    showError(nome, nomeError, !nomeOk);
    showError(null, itensError, itens.length === 0);
    if (!nomeOk) { nome.focus(); return; }
    if (!itens.length) return;

    const detalhes = form.querySelector('#q-detalhes').value.trim();
    const linhas = [
      `Olá! Sou ${nome.value.trim()} e gostaria de um orçamento.`,
      '',
      `Obra: ${form.querySelector('#q-tipo').value} em ${form.querySelector('#q-cidade').value}`,
      `Preciso de: ${itens.join(', ')}`
    ];
    if (detalhes) linhas.push(`Detalhes: ${detalhes}`);
    linhas.push('', 'Posso enviar fotos ou a planta por aqui.');

    const url = `https://wa.me/${QUOTE_WHATSAPP}?text=${encodeURIComponent(linhas.join('\n'))}`;
    window.open(url, '_blank', 'noopener');
  });
}
