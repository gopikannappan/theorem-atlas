'use strict';
import { filterRecords, paginate, recordHash, recordIdFromHash } from './catalogue-state.mjs';
import { attachObservations, observationStages, hasStage, outcomeLabel } from './evidence-state.mjs';
let evidenceSnapshot = null;
const $ = id => document.getElementById(id);
let records = [];
const KIND_LABELS = { result_family: 'Result family', formalization_project: 'Formalization project', external_proof_artifact: 'Lean artifact', external_artifact: 'Other artifact', statement_collection: 'Statement collection' };
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
function observationPanel(observation) {
  const panel = element('section', undefined, 'observation-panel');
  panel.append(element('h4', 'Atlas machine evidence'));
  if (!observation) {
    panel.append(element('p', 'No matching machine observations indexed for this exact proof version.'));
    return panel;
  }
  const stages = observationStages(observation);
  panel.append(element('p', stages.compiled ? 'Compilation reproduced at least once. Outcomes below retain earlier successes and later limits.' : 'Compilation has not been reproduced within the recorded budgets.'));
  panel.append(element('p', 'Module replay assumes imported environments. Fresh replay attempts the whole group of imports. Neither establishes mathematical fidelity.'));
  if (stages.trust_flag) panel.append(element('p', 'Trust flag: Lean.ofReduceBool appears in the reported axiom output. Native computation requires independent trust review.', 'trust-flag'));
  const table = element('table');
  const caption = element('caption', 'Recorded attempts · ' + evidenceSnapshot.observed_on);
  const head = element('tr');
  for (const title of ['Attempt', 'Build', 'Type / axioms', 'Module replay', 'Fresh replay']) head.append(element('th', title));
  const thead = element('thead'); thead.append(head); table.append(caption, thead);
  const tbody = element('tbody');
  observation.attempts.forEach((attempt, index) => {
    const row = element('tr'); const source = element('td');
    source.append(link('Run ' + (index + 1) + ' ↗', attempt.run_url));
    row.append(source);
    for (const key of ['build', 'probe', 'module_replay', 'fresh_replay']) row.append(element('td', outcomeLabel(attempt[key])));
    tbody.append(row);
  });
  table.append(tbody);
  const scroll = element('div', undefined, 'evidence-table'); scroll.append(table); panel.append(scroll);
  panel.append(element('p', 'Independent mathematical fidelity review: pending · Reviewer unassigned', 'review'));
  panel.append(element('p', 'Independent trust review: pending · Reviewer unassigned', 'review'));
  const report = element('p'); report.append(link('Audit report, diagnostics and artifacts ↗', evidenceSnapshot.report_url)); panel.append(report);
  return panel;
}
function recordUrl(id) {
  return location.pathname + location.search + recordHash(id);
}
function closeOverlay() {
  if (!$('record-dialog').open) return;
  if (history.state?.atlasOverlay) {
    $('record-dialog').close();
    document.body.classList.remove('overlay-open');
    history.back();
  }
  else {
    history.replaceState(null, '', location.pathname + location.search);
    syncOverlay();
  }
}
function syncOverlay() {
  const id = recordIdFromHash(location.hash);
  const dialog = $('record-dialog');
  if (!id) {
    if (dialog.open) dialog.close();
    document.body.classList.remove('overlay-open');
    return;
  }
  const r = records.find(record => record.id === id);
  $('detail-title').textContent = r ? r.title : 'Record not found';
  $('detail-meta').textContent = r ? `${r.source} · ${KIND_LABELS[r.kind]} · ${r.id}` : 'This record URL does not match the current catalogue.';
  $('detail-link').href = recordUrl(id);
  $('detail-status').textContent = '';
  const content = $('detail-content');
  if (r) {
    const evidence = element('div', undefined, 'evidence');
    const manuscripts = element('ul');
    for (const m of r.manuscripts) { const li = element('li'); li.append(link(m.title, m.url)); manuscripts.append(li); }
    if (r.manuscripts.length) evidence.append(manuscripts);
    for (const reference of r.references || []) {
      const p = element('p'); p.append(link(reference.title + ' ↗', reference.url)); evidence.append(p);
    }
    if (r.artifact_url) { const p = element('p'); p.append(link(r.archive_member ? 'Pinned proof archive ↗' : r.kind === 'external_artifact' ? 'Pinned text artifact ↗' : 'Pinned upstream Lean artifact ↗', r.artifact_url)); evidence.append(p); }
    if (r.archive_member) evidence.append(element('p', 'Archive member: ' + r.archive_member));
    if (r.archive_sha256) evidence.append(element('p', 'Archive SHA-256: ' + r.archive_sha256));
    for (const relation of r.source_relationships || []) { const p = element('p', relation.description + ' '); p.append(link('Pinned reuse evidence ↗', relation.evidence_url)); evidence.append(p); }
    if (r.origin_note) evidence.append(element('p', r.origin_note));
    if (r.metadata_note) evidence.append(element('p', r.metadata_note));
    if (r.license) {
      const p = element('p', 'Upstream license: '); p.append(link(r.license.code + ' · ' + r.license.materials, r.license.url)); evidence.append(p);
      evidence.append(element('p', r.attribution));
      evidence.append(element('p', r.license.third_party_note));
    }
    const provenance = element('p', 'Upstream commit: '); provenance.append(link(r.upstream_commit, r.source_url)); evidence.append(provenance);
    if (r.scope_url) { const p = element('p'); p.append(link('Upstream formalization scope note ↗', r.scope_url)); evidence.append(p); }
    for (const [index, proof] of r.proofs.entries()) {
      const p = element('p'); p.append(link(proof.declaration + ' ↗', proof.url)); evidence.append(p);
      evidence.append(element('p', `Lean: ${proof.toolchain} · External proof · Independent review pending`));
      evidence.append(element('p', `Dependencies: ${proof.dependencies.join(', ')}`));
      evidence.append(observationPanel(r.observations?.[index]));
    }
    evidence.append(element('p', 'Statement, definitions, assumptions and trust dependencies have not been independently reviewed. Machine observations are evidence, not a completed audit or manuscript-fidelity approval.', 'review'));

    content.replaceChildren(evidence);
  } else content.replaceChildren(element('p', 'Close this panel to browse or search the catalogue.'));
  if (!dialog.open) dialog.showModal();
  document.body.classList.add('overlay-open');
}

function render() {
  const selected = filterRecords(records, { query: $('query').value, source: $('source').value, status: $('status').value, kind: $('kind').value });
  const pagination = paginate(selected, currentPage, $('page-size').value);
  currentPage = pagination.page;
  $('count').textContent = `${pagination.first}–${pagination.last} of ${selected.length} matching records (${records.length} total)`;
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
    const article = element('a', undefined, 'record'); article.id = r.id;
    article.href = recordUrl(r.id);
    article.setAttribute('aria-haspopup', 'dialog');
    article.setAttribute('aria-label', r.title + ' — view record');
    article.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      history.pushState({ atlasOverlay: true }, '', recordUrl(r.id));
      syncOverlay();
    });
    article.append(element('div', r.id.startsWith('openai-math:') ? r.id.replace('openai-math:', 'OAI / ') : r.category || KIND_LABELS[r.kind], 'record-id'));
    const body = element('div'); body.append(element('h3', r.title));
    const tags = element('div', undefined, 'tags');
    tags.append(element('span', r.source), element('span', r.proofs.length ? 'External proof linked' : r.kind === 'statement_collection' ? 'Statements; not proof coverage' : r.kind === 'external_artifact' ? 'Text artifact; no Lean link' : r.artifact_url ? 'Unreviewed Lean artifact' : r.scope_url ? 'Upstream Lean scope note' : 'No Lean scope note indexed', `badge ${r.proofs.length ? 'linked' : ''}`), element('span', r.kind === 'result_family' ? `${r.manuscripts.length} manuscript${r.manuscripts.length === 1 ? '' : 's'}` : KIND_LABELS[r.kind]));
    if (hasStage(r, 'module_replayed')) tags.append(element('span', 'Module replay passed', 'badge observed'));
    else if (hasStage(r, 'compiled')) tags.append(element('span', 'Compilation reproduced', 'badge observed'));
    if (r.proofs.length) tags.append(element('span', 'Independent review pending', 'badge'));
    if (hasStage(r, 'trust_flag')) tags.append(element('span', 'Native computation · trust review pending', 'badge trust-flag'));
    if (r.proofs.length > 1) tags.append(element('span', `${r.proofs.length} alternative proof links`, 'badge'));
    if (r.source_relationships?.length) tags.append(element('span', 'Shared source material', 'badge'));
    body.append(tags);
    body.append(element('span', 'View record ↗', 'record-action'));
    article.append(body); fragment.append(article);
  }
  $('results').replaceChildren(fragment);
  const params = new URLSearchParams();
  for (const id of ['query', 'source', 'status', 'kind']) if ($(id).value) params.set(id, $(id).value);
  if (currentView === 'list') params.set('view', 'list');
  if (currentPage > 1) params.set('page', String(currentPage));
  if ($('page-size').value !== '12') params.set('size', $('page-size').value);
  history.replaceState(null, '', location.pathname + (params.size ? '?' + params : '') + location.hash);
}
async function init() {
  try {
    const response = await fetch('results.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const catalogue = await response.json();
    records = catalogue.results;
    try {
      const evidenceResponse = await fetch('evidence.json');
      if (!evidenceResponse.ok) throw new Error('Evidence unavailable');
      evidenceSnapshot = await evidenceResponse.json();
      records = attachObservations(records, evidenceSnapshot);
      $('machine-summary').textContent = `Machine observations · ${evidenceSnapshot.observed_on}: ${records.filter(r => hasStage(r, 'compiled')).length} records compiled at least once; ${records.filter(r => hasStage(r, 'module_replayed')).length} records passed module replay with imports assumed. Independent reviews are pending; 0 completed audits.`;
      const report = element('p'); report.append(link('Read the audit checkpoint ↗', evidenceSnapshot.report_url)); $('machine-evidence').append(report);
      const pilot = evidenceSnapshot.observations.find(o => o.target_id === 'atlas:integer-complexity' && o.record_id === null);
      if (pilot && observationStages(pilot).fresh_replayed) {
        const p = element('p', 'Separate pilot: integer complexity passed fresh dependency replay. It is outside the 12 linked catalogue records and remains independently unreviewed. ');
        p.append(link('Pilot declaration ↗', pilot.proof.url)); $('machine-evidence').append(p);
      }
    } catch (error) {
      $('machine-summary').textContent = 'Machine evidence is temporarily unavailable. Proof links remain browsable; no audit status is inferred.';
      console.warn(error);
    }
    const overlap = catalogue.overlap_report;
    if (overlap) $('overlap-summary').textContent = `${overlap.exact_artifact_groups.length} exact artifact overlap groups; ${overlap.repeated_manuscript_groups.length} repeated manuscript-link groups; ${overlap.alternative_proof_records.length} record with alternative proofs; ${overlap.source_reuse.length} documented source-reuse relationships. These are metadata checks, not a theorem-equivalence audit.`;
    for (const source of [...new Set(records.map(r => r.source))].sort()) { const option = element('option', source); option.value = source; $('source').append(option); }
    const params = new URLSearchParams(location.search);
    for (const id of ['query', 'source', 'status', 'kind']) if (params.has(id)) $(id).value = params.get(id);
    currentView = params.get('view') === 'list' ? 'list' : 'tiles';
    currentPage = Number(params.get('page') || 1);
    $('page-size').value = String(paginate([], 1, params.get('size')).size);
    $('total').textContent = records.length;
    $('linked').textContent = records.filter(r => r.proofs.length).length;
    $('coverage-summary').textContent = `${records.filter(r => r.kind === 'result_family').length} result families · ${records.filter(r => r.kind === 'formalization_project').length} formalization projects · ${records.filter(r => r.kind === 'external_proof_artifact').length} Lean artifacts · ${records.filter(r => r.kind === 'external_artifact').length} other artifact · ${records.filter(r => r.kind === 'statement_collection').length} statement collection. ${records.filter(r => r.proofs.length).length} records have curated declaration links; 0 independently audited. Projects and artifacts are not additional manuscript or theorem counts.`;
    render();
    syncOverlay();
    $('detail-close').addEventListener('click', closeOverlay);
    $('record-dialog').addEventListener('cancel', event => { event.preventDefault(); closeOverlay(); });
    let pointerStartedOutside = false;
    function outsideDialog(event) {
      const box = $('record-dialog').getBoundingClientRect();
      return event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom;
    }
    $('record-dialog').addEventListener('pointerdown', event => { pointerStartedOutside = outsideDialog(event); });
    $('record-dialog').addEventListener('click', event => {
      if (pointerStartedOutside && outsideDialog(event)) closeOverlay();
      pointerStartedOutside = false;
    });
    window.addEventListener('popstate', syncOverlay);
    window.addEventListener('hashchange', syncOverlay);
    $('detail-copy').addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(new URL($('detail-link').href).href);
        $('detail-status').textContent = 'Record link copied';
      } catch { $('detail-status').textContent = 'Use the Record link beside this button to copy the address.'; }
    });
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
