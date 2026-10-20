const form = document.querySelector('#search-form');
const results = document.querySelector('#results');

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[char]);
}

function showError(message) {
  results.innerHTML = `<div class="notice">${escapeHtml(message)}</div>`;
}

function render(data) {
  if (!data.data.length) {
    results.innerHTML = '<div class="empty"><h2>Nenhum registro encontrado</h2><p>Tente ajustar os termos ou combinar outros filtros.</p></div>';
    return;
  }
  const cards = data.data.map(record => `
    <article class="card">
      <h3>${escapeHtml(record.nome)}</h3>
      <div class="meta">
        ${record.cargo ? `<span class="pill">${escapeHtml(record.cargo)}</span>` : ''}
        ${record.orgao ? `<span class="pill">${escapeHtml(record.orgao)}</span>` : ''}
      </div>
    </article>`).join('');
  const page = data.pagination;
  const pager = page.pages > 1 ? `<div class="pager">
    <button ${page.page <= 1 ? 'disabled' : ''} data-page="${page.page - 1}">← Anterior</button>
    <button ${page.page >= page.pages ? 'disabled' : ''} data-page="${page.page + 1}">Próxima →</button>
  </div>` : '';
  results.innerHTML = `<div class="result-head"><span>${page.total.toLocaleString('pt-BR')} registro(s)</span><span>Página ${page.page} de ${Math.max(page.pages, 1)}</span></div>${cards}${pager}`;
  results.querySelectorAll('[data-page]').forEach(button => {
    button.addEventListener('click', () => search(Number(button.dataset.page)));
  });
}

async function search(page = 1) {
  const query = new URLSearchParams();
  for (const [key, raw] of new FormData(form)) {
    const value = String(raw).trim();
    if (value) query.set(key, value);
  }
  if (!['nome', 'cargo', 'orgao', 'similar'].some(key => query.has(key))) {
    showError('Informe ao menos um critério de busca.');
    return;
  }
  query.set('page', String(page));
  results.innerHTML = '<div class="empty"><h2>Buscando registros…</h2><p>Consultando a fonte pública disponível.</p></div>';
  try {
    const response = await fetch(`/api/servidores?${query}`);
    const body = await response.json();
    if (!response.ok) {
      showError(body.error?.message || 'Não foi possível concluir a busca.');
      return;
    }
    render(body);
  } catch {
    showError('Não foi possível conectar à API. Verifique se os serviços estão ativos.');
  }
}

form.addEventListener('submit', event => {
  event.preventDefault();
  search(1);
});
form.addEventListener('reset', () => setTimeout(() => {
  results.innerHTML = '<div class="empty"><span class="empty-icon">⌕</span><h2>Sua busca começa aqui</h2><p>Informe um nome, cargo ou órgão para consultar a base disponível.</p></div>';
}, 0));
