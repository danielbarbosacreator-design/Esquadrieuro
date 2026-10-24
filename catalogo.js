/* ==========================================================================
   ESQUADRIEURO — CATÁLOGO COMPLETO & FILTROS (catalogo.js)
   Fábrica Euroframes — São Francisco do Sul, SC
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initScrollEffects();

  // Dados de produtos
  function getProducts() {
    return typeof INITIAL_CATALOG !== 'undefined' ? [...INITIAL_CATALOG] : [];
  }

  const allProducts = getProducts();

  // Elementos do DOM
  const gridContainer = document.getElementById('catalog-page-grid');
  const searchInput = document.getElementById('catalog-page-search');
  const clearSearchBtn = document.getElementById('catalog-page-clear-search');
  const sortSelect = document.getElementById('catalog-sort-select');
  const categoryTabs = document.querySelectorAll('#catalog-page-category-tabs .cat-tab-btn');
  const resultsCountEl = document.getElementById('catalog-results-count');
  const activeFilterLabelEl = document.getElementById('catalog-active-filter-label');
  const resetFiltersBtn = document.getElementById('btn-reset-filters');
  const loadMoreWrap = document.getElementById('catalog-load-more-wrap');
  const loadMoreBtn = document.getElementById('btn-load-more-products');
  const loadMoreProgress = document.getElementById('load-more-progress');

  // Modal de Detalhes
  const productModal = document.getElementById('product-detail-modal');
  const closeProductModalBtn = document.getElementById('close-product-modal');

  // Estado da Página
  const PAGE_BATCH_SIZE = 24;
  let currentCategory = 'all';
  let searchQuery = '';
  let currentSort = 'default';
  let visibleLimit = PAGE_BATCH_SIZE;

  // Lê parâmetros da URL caso o usuário venha com link direto
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('cat')) {
    currentCategory = urlParams.get('cat');
  }
  if (urlParams.has('q')) {
    searchQuery = urlParams.get('q');
    if (searchInput) searchInput.value = searchQuery;
  }

  // Preenche os contadores das abas
  function updateCategoryTabCounts() {
    const counts = { all: allProducts.length };
    allProducts.forEach(item => {
      const c = item.category || 'outros';
      counts[c] = (counts[c] || 0) + 1;
    });

    Object.keys(counts).forEach(cat => {
      const el = document.getElementById(`tab-count-${cat}`);
      if (el) el.textContent = counts[cat];
    });

    // Total stats
    const totalEl = document.getElementById('stat-total-prods');
    if (totalEl) totalEl.textContent = allProducts.length;
  }
  updateCategoryTabCounts();

  // Sincroniza abas ativas
  function syncCategoryTabUI() {
    categoryTabs.forEach(tab => {
      if (tab.getAttribute('data-category') === currentCategory) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });
  }
  syncCategoryTabUI();

  // Filtra e Ordena os Produtos
  function getFilteredAndSortedProducts() {
    let list = allProducts.filter(item => {
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

    // Ordenação
    if (currentSort === 'name-asc') {
      list.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    } else if (currentSort === 'name-desc') {
      list.sort((a, b) => (b.title || '').localeCompare(a.title || ''));
    } else if (currentSort === 'code-asc') {
      list.sort((a, b) => (a.code || '').localeCompare(b.code || ''));
    }

    return list;
  }

  // Renderiza Grid
  function render() {
    if (!gridContainer) return;
    const filtered = getFilteredAndSortedProducts();

    // Atualiza botão de limpar busca
    if (clearSearchBtn) {
      clearSearchBtn.style.display = searchQuery ? 'block' : 'none';
    }

    // Atualiza labels de resultados
    if (resultsCountEl) {
      resultsCountEl.textContent = `${filtered.length} produto${filtered.length === 1 ? '' : 's'}`;
    }

    if (activeFilterLabelEl) {
      const activeTab = document.querySelector('#catalog-page-category-tabs .cat-tab-btn.active');
      const catName = activeTab ? activeTab.childNodes[0].textContent.trim() : 'Todos';
      activeFilterLabelEl.textContent = searchQuery 
        ? `para "${searchQuery}" em ${catName}` 
        : `em ${catName}`;
    }

    if (resetFiltersBtn) {
      const hasFilter = currentCategory !== 'all' || searchQuery !== '' || currentSort !== 'default';
      resetFiltersBtn.hidden = !hasFilter;
    }

    // Empty state
    if (filtered.length === 0) {
      gridContainer.innerHTML = `
        <div class="catalog-empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <h3>Nenhum produto encontrado</h3>
          <p>Tente buscar por outro código de peça ou remova os filtros aplicados.</p>
        </div>
      `;
      if (loadMoreWrap) loadMoreWrap.hidden = true;
      return;
    }

    // Fatiamento por limite visível
    const displayList = filtered.slice(0, visibleLimit);

    gridContainer.innerHTML = displayList.map(item => {
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

    // Botão de Carregar Mais
    if (loadMoreWrap) {
      if (visibleLimit < filtered.length) {
        loadMoreWrap.hidden = false;
        const remaining = filtered.length - visibleLimit;
        if (loadMoreBtn) {
          loadMoreBtn.textContent = `Carregar mais ${Math.min(PAGE_BATCH_SIZE, remaining)}`;
        }
        if (loadMoreProgress) {
          loadMoreProgress.textContent = `Mostrando ${visibleLimit} de ${filtered.length} produtos`;
        }
      } else {
        loadMoreWrap.hidden = true;
      }
    }

    // Eventos do modal de detalhes
    gridContainer.querySelectorAll('[data-action="detail"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const prodId = e.currentTarget.getAttribute('data-id');
        openProductModal(prodId);
      });
    });
  }

  // Evento Carregar Mais
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', () => {
      visibleLimit += PAGE_BATCH_SIZE;
      render();
    });
  }

  // Eventos de Filtro por Categoria
  categoryTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      currentCategory = tab.getAttribute('data-category');
      visibleLimit = PAGE_BATCH_SIZE;
      syncCategoryTabUI();
      render();
    });
  });

  // Links de categorias no rodapé
  document.querySelectorAll('.footer-cat-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const cat = link.getAttribute('data-cat');
      if (cat) {
        currentCategory = cat;
        visibleLimit = PAGE_BATCH_SIZE;
        syncCategoryTabUI();
        render();
        document.getElementById('catalog-toolbar').scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Busca com debounce
  let searchTimeout;
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        searchQuery = e.target.value;
        visibleLimit = PAGE_BATCH_SIZE;
        render();
      }, 150);
    });
  }

  // Limpar Busca
  if (clearSearchBtn && searchInput) {
    clearSearchBtn.addEventListener('click', () => {
      searchInput.value = '';
      searchQuery = '';
      visibleLimit = PAGE_BATCH_SIZE;
      render();
      searchInput.focus();
    });
  }

  // Ordenação
  if (sortSelect) {
    sortSelect.addEventListener('change', (e) => {
      currentSort = e.target.value;
      render();
    });
  }

  // Reset Geral de Filtros
  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener('click', () => {
      currentCategory = 'all';
      searchQuery = '';
      currentSort = 'default';
      visibleLimit = PAGE_BATCH_SIZE;
      if (searchInput) searchInput.value = '';
      if (sortSelect) sortSelect.value = 'default';
      syncCategoryTabUI();
      render();
    });
  }

  // Modal de Detalhes
  function openProductModal(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product || !productModal) return;

    const imgEl = document.getElementById('modal-product-image');
    const codeEl = document.getElementById('modal-product-code');
    const nameEl = document.getElementById('modal-product-name');
    const descEl = document.getElementById('modal-product-desc');
    const colorsWrap = document.getElementById('modal-product-colors');
    const colorsBox = document.getElementById('modal-colors-wrap');
    const wppBtn = document.getElementById('modal-whatsapp-btn');

    if (imgEl) imgEl.src = product.image ? (product.image + '?v=4') : 'assets/images/janelas.png';
    if (codeEl) codeEl.textContent = product.code ? `Código ${product.code}` : 'Sob medida';
    if (nameEl) nameEl.textContent = product.title;
    if (descEl) descEl.textContent = product.description || '';

    if (product.colors && product.colors.length > 0) {
      if (colorsWrap) {
        colorsWrap.innerHTML = product.colors.map(c => `<span class="color-chip">${c}</span>`).join('');
      }
      if (colorsBox) colorsBox.style.display = 'block';
    } else {
      if (colorsBox) colorsBox.style.display = 'none';
    }

    if (wppBtn) {
      const msg = encodeURIComponent(`Olá! Gostaria de cotar o produto "${product.title}" (Código: ${product.code || 'S/N'}) do catálogo oficial da Esquadrieuro.`);
      wppBtn.href = `https://wa.me/5547984474374?text=${msg}`;
    }

    productModal.showModal();
  }

  if (closeProductModalBtn && productModal) {
    closeProductModalBtn.addEventListener('click', () => {
      productModal.close();
    });

    productModal.addEventListener('click', (e) => {
      const rect = productModal.getBoundingClientRect();
      const isInDialog = (rect.top <= e.clientY && e.clientY <= rect.top + rect.height &&
        rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
      if (!isInDialog) {
        productModal.close();
      }
    });
  }

  // Baixar Catálogo PDF
  const downloadPdfBtn = document.getElementById('btn-download-catalog-page');
  if (downloadPdfBtn) {
    downloadPdfBtn.addEventListener('click', () => {
      const link = document.createElement('a');
      link.href = 'assets/catalogo-esquadrieuro-2025.pdf';
      link.download = 'Catalogo-Oficial-Esquadrieuro-Store-2025.pdf';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  }

  // Header e menu mobile
  const header = document.getElementById('header');
  const navMenu = document.getElementById('nav-menu');
  const mobileToggle = document.getElementById('mobile-toggle');
  window.addEventListener('scroll', () => {
    if (header) header.classList.toggle('scrolled', window.scrollY > 40);
  });
  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => navMenu.classList.toggle('open'));
  }

  // Render inicial
  render();
});
