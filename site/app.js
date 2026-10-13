'use strict';
import { filterRecords, paginate } from './catalogue-state.mjs';
const $ = id => document.getElementById(id);
let records = [];
let currentPage = 1;
let currentView = 'tiles';
function element(tag, text, cls) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (cls) node.className = cls;
  return node;
}
function link(text, url) {
  const node = element('a', text);
  const parsed = new URL(url);
  if (parsed.protocol !== 'https:') throw new Error('Invalid source URL');
  node.href = parsed.href; node.target = '_blank'; node.rel = 'noopener noreferrer';
  return node;
}
function render() {
  const selected = filterRecords(records, { query: $('query').value, source: $('source').value, status: $('status').value });
  const pagination = paginate(selected, currentPage, $('page-size').value);
  currentPage = pagination.page;
  $('count').textContent = `${pagination.first}–${pagination.last} of ${selected.length} matching families (${records.length} total)`;
  $('empty').hidden = selected.length !== 0;
  $('results').className = currentView;
  $('tiles-view').setAttribute('aria-pressed', String(currentView === 'tiles'));
  $('list-view').setAttribute('aria-pressed', String(currentView === 'list'));
  $('pagination').hidden = selected.length === 0;
  $('previous-page').disabled = currentPage === 1;
  $('next-page').disabled = currentPage === pagination.totalPages;
  const options = document.createDocumentFragment();
  for (let page = 1; page <= pagination.totalPages; page++) {
    const option = element('option', String(page)); option.value = String(page); options.append(option);
  }
  $('page-number').replaceChildren(options); $('page-number').value = String(currentPage);
  $('page-total').textContent = `of ${pagination.totalPages}`;
  const fragment = document.createDocumentFragment();
  for (const r of pagination.items) {
    const article = element('article', undefined, 'record'); article.id = r.id;
    article.append(element('div', r.id.replace('openai-math:', 'OAI / '), 'record-id'));
    const body = element('div'); body.append(element('h3', r.title));
    const tags = element('div', undefined, 'tags');
    tags.append(element('span', r.source), element('span', r.proofs.length ? 'External proof linked' : r.scope_url ? 'Upstream Lean scope note' : 'No Lean scope note indexed', `badge ${r.proofs.length ? 'linked' : ''}`), element('span', `${r.manuscripts.length} manuscript${r.manuscripts.length === 1 ? '' : 's'}`));
    body.append(tags);
    const details = element('details'); details.append(element('summary', 'Inspect sources & evidence'));
    const evidence = element('div', undefined, 'evidence');
    const manuscripts = element('ul');
    for (const m of r.manuscripts) { const li = element('li'); li.append(link(m.title, m.url)); manuscripts.append(li); }
    evidence.append(manuscripts);
    const provenance = element('p', 'Upstream commit: '); provenance.append(link(r.upstream_commit, r.source_url)); evidence.append(provenance);
    if (r.scope_url) { const p = element('p'); p.append(link('Upstream formalization scope note ↗', r.scope_url)); evidence.append(p); }
    for (const proof of r.proofs) {
      const p = element('p'); p.append(link(proof.declaration + ' ↗', proof.url)); evidence.append(p);
      evidence.append(element('p', `Lean: ${proof.toolchain} · External · Not locally audited`));
      evidence.append(element('p', `Dependencies: ${proof.dependencies.join(', ')}`));
    }
    evidence.append(element('p', 'Statement and assumptions have not been independently extracted or reviewed. No local proof audit or manuscript-fidelity review is claimed.', 'review'));
    details.append(evidence); body.append(details); article.append(body); fragment.append(article);
  }
  $('results').replaceChildren(fragment);
  const params = new URLSearchParams();
  for (const id of ['query', 'source', 'status']) if ($(id).value) params.set(id, $(id).value);
  if (currentView === 'list') params.set('view', 'list');
  if (currentPage > 1) params.set('page', String(currentPage));
  if ($('page-size').value !== '12') params.set('size', $('page-size').value);
  history.replaceState(null, '', location.pathname + (params.size ? '?' + params : '') + location.hash);
}
async function init() {
  try {
    const response = await fetch('results.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    records = (await response.json()).results;
    for (const source of [...new Set(records.map(r => r.source))].sort()) { const option = element('option', source); option.value = source; $('source').append(option); }
    const params = new URLSearchParams(location.search);
    for (const id of ['query', 'source', 'status']) if (params.has(id)) $(id).value = params.get(id);
    currentView = params.get('view') === 'list' ? 'list' : 'tiles';
    currentPage = Number(params.get('page') || 1);
    $('page-size').value = String(paginate([], 1, params.get('size')).size);
    $('total').textContent = records.length;
    $('linked').textContent = records.filter(r => r.proofs.length).length;
    $('coverage-summary').textContent = `${records.filter(r => r.scope_url).length} families have upstream Lean scope notes · ${records.filter(r => r.proofs.length).length} has a curated declaration link · 0 locally audited. Scope notes may describe partial or supporting results.`;
    render();
    $('filters').addEventListener('input', () => { currentPage = 1; render(); });
    $('filters').addEventListener('submit', event => event.preventDefault());
    $('filters').addEventListener('reset', () => { currentPage = 1; setTimeout(render, 0); });
    $('page-size').addEventListener('change', () => { currentPage = 1; render(); });
    for (const view of ['tiles', 'list']) $(view + '-view').addEventListener('click', () => { currentView = view; render(); });
    function goToPage(page) {
      currentPage = page; render();
      $('count').scrollIntoView({ block: 'start' });
    }
    $('previous-page').addEventListener('click', () => goToPage(currentPage - 1));
    $('next-page').addEventListener('click', () => goToPage(currentPage + 1));
    $('page-number').addEventListener('change', () => goToPage(Number($('page-number').value)));
  } catch (error) { $('count').textContent = 'The catalogue could not be loaded. Please refresh or download the data.'; console.error(error); }
}
init();
