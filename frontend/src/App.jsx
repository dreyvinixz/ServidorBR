import { useEffect, useRef, useState } from 'react';

const SOURCE_URL = 'https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal--aposentados';

function Icon({ name, className = 'size-5' }) {
  const common = { className, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.7, strokeLinecap: 'round', strokeLinejoin: 'round', 'aria-hidden': true };
  const paths = {
    search: <><circle cx="10.8" cy="10.8" r="6.8" /><path d="m16 16 4.5 4.5" /></>,
    arrow: <><path d="M5 12h14" /><path d="m13 6 6 6-6 6" /></>,
    building: <><path d="M4 21h16M6 21V5l6-2 6 2v16M9 9h.01M15 9h.01M9 13h.01M15 13h.01M10 21v-4h4v4" /></>,
    person: <><circle cx="12" cy="8" r="3.5" /><path d="M5 21a7 7 0 0 1 14 0" /></>,
    briefcase: <><rect x="3" y="7" width="18" height="13" rx="2" /><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18M10 12v2h4v-2" /></>,
    chevron: <path d="m7 10 5 5 5-5" />,
    close: <><path d="m18 6-12 12M6 6l12 12" /></>,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
    shield: <><path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11Z" /><path d="m9 12 2 2 4-4" /></>,
    sliders: <><path d="M4 21v-7m0-4V3m8 18v-9m0-4V3m8 18v-5m0-4V3" /><path d="M2 14h4m4-6h4m4 6h4" /></>,
    list: <><path d="M8 6h13M8 12h13M8 18h13" /><path d="M3 6h.01M3 12h.01M3 18h.01" /></>,
  };
  return <svg {...common}>{paths[name]}</svg>;
}

function SearchField({ label, hint, name, icon, placeholder, maxLength, value, onChange }) {
  return (
    <label className="group block min-w-0">
      <span className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-700">
        <Icon name={icon} className="size-4 text-slate-400" />{label}
      </span>
      <input
        name={name}
        value={value}
        onChange={onChange}
        maxLength={maxLength}
        placeholder={placeholder}
        autoComplete="off"
        className="field-input"
      />
      {hint && <span className="mt-2 block text-xs leading-5 text-slate-500">{hint}</span>}
    </label>
  );
}

function SearchableSelect({ label, hint, name, icon, options, value, onSelect, placeholder, loading, disabled }) {
  const [open, setOpen] = useState(false);
  const [term, setTerm] = useState('');
  const rootRef = useRef(null);
  const inputRef = useRef(null);
  const listId = `options-${name}`;
  const normalizedTerm = term.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR').trim();
  const visibleOptions = options
    .filter((option) => option.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR').includes(normalizedTerm))
    .slice(0, 60);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  useEffect(() => {
    if (!open) return undefined;
    function closeOutside(event) {
      if (!rootRef.current?.contains(event.target)) setOpen(false);
    }
    document.addEventListener('pointerdown', closeOutside);
    return () => document.removeEventListener('pointerdown', closeOutside);
  }, [open]);

  function choose(option) {
    onSelect(name, option);
    setTerm('');
    setOpen(false);
  }

  return (
    <div ref={rootRef} className="relative min-w-0">
      <span className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-700">
        <Icon name={icon} className="size-4 text-slate-400" />{label}
      </span>
      <button
        type="button"
        className="field-input field-combobox cursor-pointer disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-400"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={listId}
        aria-label={`${label}: ${value || placeholder}`}
        disabled={disabled}
        onClick={() => setOpen((current) => !current)}
      >
        <span className={value ? 'truncate text-slate-800' : 'truncate text-slate-400'}>{value || (loading ? 'Carregando opções…' : placeholder)}</span>
        <Icon name="chevron" className={`size-4 shrink-0 text-slate-500 transition ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="absolute z-30 mt-2 w-full rounded-2xl border border-slate-200 bg-white p-3 shadow-xl shadow-slate-900/10">
          <input
            ref={inputRef}
            value={term}
            onChange={(event) => setTerm(event.target.value)}
            onKeyDown={(event) => { if (event.key === 'Escape') setOpen(false); }}
            className="field-input"
            placeholder={`Buscar ${label.toLocaleLowerCase('pt-BR')}…`}
            aria-label={`Filtrar opções de ${label.toLocaleLowerCase('pt-BR')}`}
            autoComplete="off"
          />
          <ul id={listId} role="listbox" aria-label={label} className="mt-2 max-h-64 overflow-y-auto">
            {visibleOptions.length ? visibleOptions.map((option) => (
              <li key={option} role="presentation">
                <button
                  type="button"
                  role="option"
                  aria-selected={option === value}
                  onClick={() => choose(option)}
                  className="w-full rounded-lg px-3 py-2 text-left text-sm leading-5 text-slate-700 hover:bg-emerald-50 hover:text-emerald-900 focus-visible:bg-emerald-50 focus-visible:outline-none"
                >{option}</button>
              </li>
            )) : <li className="px-3 py-3 text-sm leading-5 text-slate-500">Nenhuma opção encontrada. Confira a digitação.</li>}
          </ul>
          {visibleOptions.length === 60 && <p className="px-3 pt-2 text-xs text-slate-500">Refine a busca para ver outras opções.</p>}
          {value && <button type="button" onClick={() => { onSelect(name, ''); setTerm(''); setOpen(false); }} className="mt-2 w-full border-t border-slate-100 px-3 pt-3 text-left text-xs font-semibold text-emerald-800">Remover seleção</button>}
        </div>
      )}
      {hint && <span className="mt-2 block text-xs leading-5 text-slate-500">{hint}</span>}
    </div>
  );
}

function ResultCard({ record, index }) {
  return (
    <article className="result-card animate-rise" style={{ animationDelay: `${Math.min(index * 45, 270)}ms` }}>
      <div className="flex items-start gap-4">
        <div className="flex size-11 shrink-0 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-800 ring-1 ring-emerald-100">
          <Icon name="person" className="size-5" />
        </div>
        <div className="min-w-0 flex-1">
          <h3 className="break-words text-base font-bold tracking-tight text-slate-900">{record.nome}</h3>
          <div className="mt-3 flex flex-wrap gap-2">
            <span className="result-tag"><Icon name="briefcase" className="size-3.5" />{record.cargo || 'Cargo não informado pela fonte'}</span>
            <span className="result-tag"><Icon name="building" className="size-3.5" />{record.orgao || 'Órgão não informado pela fonte'}</span>
          </div>
        </div>
        <span className="hidden rounded-full bg-slate-50 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400 sm:inline-flex">Registro público</span>
      </div>
    </article>
  );
}

function EmptyState({ searching }) {
  return (
    <div className="empty-state">
      <div className={`mb-5 flex size-14 items-center justify-center rounded-2xl ${searching ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-500'}`}>
        {searching ? <span className="size-5 animate-spin rounded-full border-2 border-emerald-800/25 border-t-emerald-800" /> : <Icon name="search" className="size-6" />}
      </div>
      <h2 className="text-lg font-bold tracking-tight text-slate-900">{searching ? 'Consultando os registros' : 'Sua busca começa aqui'}</h2>
      <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">
        {searching ? 'Estamos procurando correspondências na base pública disponível.' : 'Preencha ao menos um campo para encontrar registros de servidores aposentados.'}
      </p>
    </div>
  );
}

export default function App() {
  const [filters, setFilters] = useState({ nome: '', cargo: '', orgao: '', similar: '', per_page: '25' });
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [options, setOptions] = useState({ cargos: [], orgaos: [] });
  const [optionsLoading, setOptionsLoading] = useState(true);
  const [optionsError, setOptionsError] = useState('');
  const activeRequest = useRef(null);
  const resultsRef = useRef(null);

  useEffect(() => () => activeRequest.current?.abort(), []);

  useEffect(() => {
    const controller = new AbortController();
    fetch('/api/opcoes', { signal: controller.signal })
      .then(async (response) => {
        const body = await response.json();
        if (!response.ok) throw new Error(body.error?.message || 'Falha ao carregar opções.');
        setOptions({ cargos: body.cargos || [], orgaos: body.orgaos || [] });
      })
      .catch((requestError) => {
        if (requestError.name !== 'AbortError') {
          setOptionsError(requestError.message === 'Failed to fetch'
            ? 'Não foi possível conectar à API. Inicie o backend e tente novamente.'
            : requestError.message || 'Não foi possível carregar a lista de opções.');
        }
      })
      .finally(() => { if (!controller.signal.aborted) setOptionsLoading(false); });
    return () => controller.abort();
  }, []);

  function updateField(event) {
    const { name, value } = event.target;
    setFilters((current) => ({ ...current, [name]: value }));
  }

  function selectOption(name, value) {
    setFilters((current) => ({ ...current, [name]: value }));
  }

  async function search(page = 1) {
    const params = new URLSearchParams();
    for (const key of ['nome', 'cargo', 'orgao', 'similar']) {
      const value = filters[key].trim();
      if (value) params.set(key, value);
    }
    if (![...params.keys()].length) {
      setResult(null);
      setError('Informe ao menos um critério para iniciar a busca.');
      return;
    }
    params.set('per_page', filters.per_page);
    params.set('page', String(page));
    if (params.has('similar')) params.set('limit', '100');

    activeRequest.current?.abort();
    const controller = new AbortController();
    activeRequest.current = controller;
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`/api/servidores?${params.toString()}`, { signal: controller.signal });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error?.message || 'Não foi possível concluir a busca.');
      setResult(body);
      requestAnimationFrame(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }));
    } catch (requestError) {
      if (requestError.name !== 'AbortError') setError(requestError.message || 'Não foi possível conectar à API. Verifique se os serviços estão ativos.');
    } finally {
      if (!controller.signal.aborted) setLoading(false);
    }
  }

  function clearSearch() {
    activeRequest.current?.abort();
    setFilters({ nome: '', cargo: '', orgao: '', similar: '', per_page: '25' });
    setResult(null);
    setError('');
    setLoading(false);
  }

  const page = result?.pagination;
  const count = page?.total?.toLocaleString('pt-BR') ?? '0';

  return (
    <div className="min-h-screen bg-[#f5f7f4] text-slate-900">
      <header className="site-header">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8 lg:px-12">
          <a href="/" className="flex items-center gap-3 rounded-xl focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-emerald-700" aria-label="ServidorBR, início">
            <span className="flex size-10 items-center justify-center rounded-xl bg-emerald-900 text-xs font-black tracking-tight text-white shadow-lg shadow-emerald-950/10">SB</span>
            <span className="text-[17px] font-extrabold tracking-[-0.05em] text-slate-900">Servidor<span className="text-emerald-800">BR</span><span className="mt-0.5 block text-[9px] font-bold tracking-[0.2em] text-slate-500">CONSULTA PÚBLICA</span></span>
          </a>
          <div className="hidden items-center gap-2 rounded-full border border-slate-200/80 bg-white/75 px-3.5 py-2 text-[10px] font-bold tracking-[0.14em] text-slate-600 sm:flex">
            <span className="size-1.5 rounded-full bg-emerald-600" /> DADOS ABERTOS · BRASIL
          </div>
          <a href={SOURCE_URL} target="_blank" rel="noreferrer" className="text-xs font-semibold text-slate-600 transition hover:text-emerald-800">Sobre o projeto <span aria-hidden="true">↗</span></a>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-5 pb-16 pt-9 sm:px-8 sm:pt-14 lg:px-12 lg:pt-16">
        <section className="hero-grid relative isolate overflow-hidden rounded-[2rem] bg-emerald-950 px-6 py-9 text-white shadow-xl shadow-emerald-950/10 sm:px-10 sm:py-12 lg:px-14 lg:py-14">
          <div className="hero-glow pointer-events-none absolute -right-20 -top-36 -z-10 size-[30rem] rounded-full" />
          <div className="absolute right-8 top-8 hidden size-28 items-center justify-center rounded-full border border-white/10 bg-white/[0.04] text-emerald-100/70 lg:flex">
            <Icon name="shield" className="size-12" />
          </div>
          <div className="max-w-3xl">
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-emerald-200/20 bg-white/[0.07] px-3 py-1.5 text-[10px] font-bold tracking-[0.17em] text-emerald-100">
              <span className="size-1.5 rounded-full bg-lime-300" /> TRANSPARÊNCIA EM DADOS PÚBLICOS
            </div>
            <h1 className="max-w-2xl text-[2.7rem] font-semibold leading-[1.04] tracking-[-0.06em] sm:text-6xl lg:text-[4.25rem]">Informação pública,<br /><span className="font-serif font-normal italic text-lime-200">busca mais simples.</span></h1>
            <p className="mt-5 max-w-xl text-sm leading-6 text-emerald-100/75 sm:text-base sm:leading-7">Consulte registros de servidores aposentados do Executivo Federal por nome, cargo ou órgão.</p>
          </div>
          <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-3 border-t border-white/10 pt-5 text-xs text-emerald-100/70">
            <span className="inline-flex items-center gap-2"><Icon name="shield" className="size-4 text-lime-200" /> Fonte pública</span>
            <span className="inline-flex items-center gap-2"><Icon name="clock" className="size-4 text-lime-200" /> Consulta direta</span>
            <span className="inline-flex items-center gap-2"><Icon name="building" className="size-4 text-lime-200" /> Executivo Federal</span>
          </div>
        </section>

        <section className="search-panel relative z-10 mx-auto -mt-5 max-w-6xl rounded-3xl border border-white bg-white p-5 shadow-xl shadow-slate-900/[0.07] sm:p-7 lg:p-8" aria-labelledby="search-title">
          <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
            <div>
              <span className="section-kicker">CONSULTA DE REGISTROS</span>
              <h2 id="search-title" className="mt-1.5 text-xl font-bold tracking-tight text-slate-900">Como podemos ajudar?</h2>
            </div>
            <span className="text-xs text-slate-500"><span className="text-emerald-700">*</span> Use pelo menos um campo</span>
          </div>
          <form onSubmit={(event) => { event.preventDefault(); search(1); }}>
            <div className="grid gap-x-5 gap-y-5 md:grid-cols-2 lg:grid-cols-4">
              <div className="lg:col-span-2">
                <SearchField label="Nome do servidor" name="nome" icon="person" placeholder="Digite o nome completo" hint="Busca exata pelo nome informado." maxLength={120} value={filters.nome} onChange={updateField} />
              </div>
              <SearchableSelect label="Cargo ou profissão" name="cargo" icon="briefcase" options={options.cargos} value={filters.cargo} onSelect={selectOption} placeholder="Selecione um cargo" loading={optionsLoading} disabled={optionsLoading || Boolean(optionsError) || !options.cargos.length} hint="Escolha entre os cargos existentes na base; digite para filtrar a lista." />
              <SearchableSelect label="Órgão ou instituição" name="orgao" icon="building" options={options.orgaos} value={filters.orgao} onSelect={selectOption} placeholder="Selecione um órgão" loading={optionsLoading} disabled={optionsLoading || Boolean(optionsError) || !options.orgaos.length} hint="A lista mostra somente órgãos presentes nos registros." />
            </div>
            {optionsError && <p role="status" className="mt-3 text-xs leading-5 text-amber-800">{optionsError}</p>}
            <details className="advanced-search mt-6">
              <summary className="advanced-summary">
                <span className="advanced-icon"><Icon name="sliders" className="size-5" /></span>
                <span className="advanced-copy">
                  <span className="advanced-title">Opções avançadas</span>
                  <span className="advanced-description">Busca aproximada e preferências de resultados</span>
                </span>
                <span className="advanced-optional">Opcional</span>
                <span className="advanced-chevron"><Icon name="chevron" className="size-4" /></span>
              </summary>
              <div className="advanced-content">
                <div className="advanced-content-heading">
                  <div>
                    <h3>Personalize sua consulta</h3>
                    <p>Esses ajustes não são necessários para uma busca comum.</p>
                  </div>
                </div>
                <div className="grid gap-5 md:grid-cols-2">
                  <SearchField label="Nome aproximado" name="similar" icon="search" placeholder="Ex.: Maria Silva" hint="Use quando não souber a grafia exata do nome." maxLength={120} value={filters.similar} onChange={updateField} />
                  <label className="block">
                    <span className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-700"><Icon name="list" className="size-4 text-slate-400" />Resultados por página</span>
                    <select name="per_page" value={filters.per_page} onChange={updateField} className="field-input max-w-xs">
                      {[10, 25, 50, 100].map((size) => <option key={size} value={size}>{size} resultados</option>)}
                    </select>
                    <span className="mt-2 block text-xs leading-5 text-slate-500">Escolha quantos registros mostrar em cada página.</span>
                  </label>
                </div>
                <div className="advanced-note"><Icon name="shield" className="size-4 shrink-0" /><p>A busca aproximada compara nomes semelhantes e tem limite de 100 resultados no total.</p></div>
              </div>
            </details>
            <div className="mt-6 flex flex-col-reverse gap-3 border-t border-slate-100 pt-5 sm:flex-row sm:items-center">
              <button type="button" onClick={clearSearch} className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl px-5 text-sm font-semibold text-slate-600 transition hover:bg-slate-100 hover:text-slate-900 focus-visible:outline-2 focus-visible:outline-emerald-700">Limpar filtros <Icon name="close" className="size-4" /></button>
              <span className="flex-1 text-center text-xs leading-5 text-slate-500 sm:text-left">Os filtros informados são combinados. A fonte não disponibiliza UF.</span>
              <button type="submit" disabled={loading} className="primary-button inline-flex min-h-12 items-center justify-center gap-2.5 rounded-xl px-6 text-sm font-bold text-white transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-700 disabled:cursor-wait disabled:opacity-70">
                {loading ? <span className="size-4 animate-spin rounded-full border-2 border-white/35 border-t-white" /> : <Icon name="search" className="size-4" />}
                {loading ? 'Buscando…' : 'Buscar registros'} {!loading && <Icon name="arrow" className="size-4" />}
              </button>
            </div>
          </form>
        </section>

        <section ref={resultsRef} className="scroll-mt-8 pt-12" aria-live="polite" aria-busy={loading}>
          <div className="mb-5 flex flex-wrap items-end justify-between gap-4">
            <div>
              <span className="section-kicker">RESULTADOS</span>
              <h2 className="mt-1.5 text-2xl font-bold tracking-tight text-slate-900">Registros encontrados</h2>
            </div>
            {result && <span className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600">{count} {page.total === 1 ? 'registro' : 'registros'}</span>}
          </div>

          {error ? (
            <div role="alert" className="rounded-2xl border border-rose-200 bg-rose-50 px-5 py-4 text-sm font-medium text-rose-800">{error}</div>
          ) : loading && !result ? <EmptyState searching /> : !result ? <EmptyState searching={false} /> : result.data.length === 0 ? (
            <div className="empty-state rounded-2xl border border-slate-200 bg-white">
              <div className="mb-5 flex size-14 items-center justify-center rounded-2xl bg-amber-50 text-amber-700"><Icon name="search" className="size-6" /></div>
              <h2 className="text-lg font-bold tracking-tight text-slate-900">Não encontramos dados com esses filtros</h2>
              <p className="mt-2 max-w-xl text-sm leading-6 text-slate-600">Confira a grafia ou os campos escolhidos. Cargo e órgão são combinados entre si; o nome comum é exato. Para variações no nome, use <strong>Nome aproximado</strong> nas opções avançadas.</p>
              <button type="button" onClick={clearSearch} className="mt-5 inline-flex min-h-10 items-center justify-center rounded-xl border border-emerald-200 bg-emerald-50 px-4 text-sm font-semibold text-emerald-900 transition hover:bg-emerald-100">Limpar filtros e tentar novamente</button>
            </div>
          ) : (
            <>
              <div className="grid gap-3 lg:grid-cols-2">{result.data.map((record, index) => <ResultCard key={record.id ?? `${record.nome}-${index}`} record={record} index={index} />)}</div>
              <div className="mt-5 flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs text-slate-500">Página <strong className="text-slate-800">{page.page}</strong> de <strong className="text-slate-800">{Math.max(page.pages, 1)}</strong>{result.query_time_ms != null && <span className="ml-2">· {result.query_time_ms.toLocaleString('pt-BR')} ms</span>}</p>
                <div className="flex gap-2">
                  <button type="button" onClick={() => search(page.page - 1)} disabled={loading || page.page <= 1} className="pager-button">← Anterior</button>
                  <button type="button" onClick={() => search(page.page + 1)} disabled={loading || page.page >= page.pages} className="pager-button">Próxima →</button>
                </div>
              </div>
            </>
          )}
        </section>

        <footer className="mt-14 flex flex-col gap-3 border-t border-slate-200 pt-6 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
          <p>Dados públicos · Gestão de Pessoas — Aposentados do Executivo Federal</p>
          <a className="inline-flex items-center gap-1 font-semibold text-emerald-800 transition hover:text-emerald-950" href={SOURCE_URL} target="_blank" rel="noreferrer">Conheça a fonte dos dados <span aria-hidden="true">↗</span></a>
        </footer>
      </main>
    </div>
  );
}
