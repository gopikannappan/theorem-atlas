import test from 'node:test';
import assert from 'node:assert/strict';
import { filterRecords, paginate } from '../site/catalogue-state.mjs';
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
