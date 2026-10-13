'use strict';
const $ = id => document.getElementById(id);
let records = [];
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
  const query = $('query').value.trim().toLowerCase();
  const selected = records.filter(r => (!query || JSON.stringify([r.id, r.title, r.manuscripts, r.proofs]).toLowerCase().includes(query)) && (!$('source').value || r.source === $('source').value) && (!$('status').value || ($('status').value === 'scope' ? r.scope_url : r.status === $('status').value)));
  $('count').textContent = `${selected.length} of ${records.length} result families`;
  $('empty').hidden = selected.length !== 0;
  const fragment = document.createDocumentFragment();
  for (const r of selected) {
    const article = element('article', undefined, 'record'); article.id = r.id;
    article.append(element('div', r.id.replace('openai-math:', 'OAI / '), 'record-id'));
    const body = element('div'); body.append(element('h3', r.title));
    const tags = element('div', undefined, 'tags');
    tags.append(element('span', r.source), element('span', r.proofs.length ? 'External proof linked' : 'Discovered', `badge ${r.proofs.length ? 'linked' : ''}`), element('span', `${r.manuscripts.length} manuscript${r.manuscripts.length === 1 ? '' : 's'}`));
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
    $('total').textContent = records.length;
    $('linked').textContent = records.filter(r => r.proofs.length).length;
    render();
    $('filters').addEventListener('input', render);
    $('filters').addEventListener('submit', event => event.preventDefault());
    $('filters').addEventListener('reset', () => setTimeout(render, 0));
  } catch (error) { $('count').textContent = 'The catalogue could not be loaded. Please refresh or download the data.'; console.error(error); }
}
init();
