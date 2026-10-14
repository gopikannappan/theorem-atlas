import test from 'node:test';
import assert from 'node:assert/strict';
import { filterRecords, paginate, recordHash, recordIdFromHash } from '../site/catalogue-state.mjs';
const records = Array.from({ length: 25 }, (_, i) => ({ id: String(i), title: `Result ${i}`, source: 'OpenAI', manuscripts: [], proofs: [], status: 'discovered', scope_url: i % 2 ? 'https://example.com' : null }));
test('default tiles page size is 12 with complete page boundaries', () => {
  assert.equal(paginate(records).items.length, 12);
  assert.deepEqual([1, 2, 3].flatMap(page => paginate(records, page).items), records);
  assert.equal(paginate(records, 3).first, 25);
  assert.equal(paginate(records, 3).last, 25);
});
test('invalid and out-of-range URL pagination is normalized', () => {
  for (const page of [-4, NaN, Infinity, 1.5]) assert.equal(paginate(records, page).page, 1);
  assert.equal(paginate(records, 999).page, 3);
  assert.equal(paginate(records, 1, '24').items.length, 24);
  assert.equal(paginate(records, 1, 13).size, 12);
});
test('empty filtered results have no phantom result range', () => {
  const result = paginate([], 9);
  assert.equal(result.first, 0); assert.equal(result.last, 0); assert.equal(result.page, 1);
});
test('coverage filters distinguish scope notes from curated proofs', () => {
  assert.equal(filterRecords(records, { status: 'scope' }).length, 12);
  assert.equal(filterRecords(records, { status: 'no_scope' }).length, 13);
  assert.equal(filterRecords(records, { status: 'external_linked' }).length, 0);
  assert.equal(filterRecords(records, { query: ' result 24 ' })[0].id, '24');
  assert.equal(filterRecords(records, { source: 'Other' }).length, 0);
});
test('record type filter distinguishes proof artifacts from statement collections', () => {
  const mixed = [{ ...records[0], kind: 'external_proof_artifact' }, { ...records[1], kind: 'statement_collection' }];
  assert.equal(filterRecords(mixed, { kind: 'external_proof_artifact' }).length, 1);
  assert.equal(filterRecords(mixed, { kind: 'statement_collection' })[0].id, '1');
});

test('record deep links round-trip IDs including archive member paths', () => {
  for (const id of ['openai-math:005', 'deepseek-minif2f:test/aime_1983_p1.lean', 'name with & punctuation'])
    assert.equal(recordIdFromHash(recordHash(id)), id);
});
test('non-record and malformed fragments do not open an overlay', () => {
  for (const hash of ['', '#catalogue', '#record=', '#record=%ZZ']) assert.equal(recordIdFromHash(hash), null);
});

import { readFileSync } from 'node:fs';
import { attachObservations, observationStages, hasStage, outcomeLabel } from '../site/evidence-state.mjs';
const snapshot = JSON.parse(readFileSync(new URL('../site/evidence.json', import.meta.url)));
const catalogue = JSON.parse(readFileSync(new URL('../catalog/results.json', import.meta.url))).results;
test('frozen machine evidence matches exact external proofs without promoting audit status', () => {
  const enriched = attachObservations(catalogue, snapshot);
  assert.equal(enriched.filter(r => hasStage(r, 'compiled')).length, 10);
  assert.equal(enriched.filter(r => hasStage(r, 'module_replayed')).length, 7);
  assert.equal(enriched.flatMap(r => r.observations || []).filter(o => observationStages(o).compiled).length, 11);
  assert.equal(enriched.flatMap(r => r.observations || []).filter(o => observationStages(o).fresh_replayed).length, 0);
  assert.equal(enriched.filter(r => hasStage(r, 'trust_flag')).length, 2);
  assert.equal(enriched.filter(r => hasStage(r, 'review_pending')).length, 12);
  enriched.forEach((r, i) => {
    assert.equal(r.status, catalogue[i].status);
    assert.equal(r.fidelity_review, 'unreviewed');
    r.proofs.forEach(p => assert.equal(p.audit_state, 'not_locally_audited'));
  });
});
test('observations cannot migrate across commits, declarations, toolchains or records', () => {
  const observation = snapshot.observations.find(o => o.record_id !== null);
  const original = catalogue.find(r => r.id === observation.record_id);
  for (const field of ['url', 'commit', 'declaration', 'toolchain', 'mathlib_commit']) {
    const changed = { ...original, proofs: original.proofs.map(p => ({ ...p, [field]: 'different' })) };
    assert(attachObservations([changed], snapshot)[0].observations.every(o => o === null));
  }
  assert(attachObservations([{ ...original, id: 'different' }], snapshot)[0].observations.every(o => o === null));
});
test('attempt history retains earlier compilation success and later timeout', () => {
  const p1 = snapshot.observations.find(o => o.target_id === 'harmonic:imo2025:p1');
  assert.equal(observationStages(p1).compiled, true);
  assert.equal(outcomeLabel(p1.attempts.at(-1).build), 'Timed out');
  assert.equal(observationStages(p1).module_replayed, false);
  const p4 = snapshot.observations.filter(o => o.record_id === 'harmonic:imo2025:p4');
  assert.equal(p4.length, 2);
  p4.forEach(o => {
    assert.equal(observationStages(o).trust_flag, true);
    assert.equal(observationStages(o).module_replayed, false);
  });
});
test('machine-evidence filters coexist with pagination and exclude the separate pilot', () => {
  const enriched = attachObservations(catalogue, snapshot);
  assert.equal(filterRecords(enriched, { status: 'compiled' }).length, 10);
  assert.equal(filterRecords(enriched, { status: 'module_replayed' }).length, 7);
  assert.equal(filterRecords(enriched, { status: 'trust_flag' }).length, 2);
  assert.equal(filterRecords(enriched, { status: 'review_pending' }).length, 12);
  assert.equal(paginate(filterRecords(enriched, { status: 'compiled' })).last, 10);
  const pilot = snapshot.observations.find(o => o.record_id === null);
  assert.equal(observationStages(pilot).fresh_replayed, true);
  assert(!enriched.some(r => r.observations?.includes(pilot)));
});
test('missing evidence stays unknown and does not imply a failed proof', () => {
  assert.deepEqual(observationStages(null), { compiled: false, module_replayed: false, fresh_replayed: false, trust_flag: false });
  assert.equal(outcomeLabel(null), 'Not run');
  assert.equal(outcomeLabel({ outcome: 'incomplete_group_build', exit_code: null }), 'Skipped: incomplete group build');
});
