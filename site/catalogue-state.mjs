export function filterRecords(records, { query = '', source = '', status = '', kind = '' } = {}) {
  const needle = query.trim().toLowerCase();
  return records.filter(r => (!needle || JSON.stringify([r.id, r.title, r.manuscripts, r.proofs]).toLowerCase().includes(needle))
    && (!source || r.source === source)
    && (!kind || r.kind === kind)
    && (!status || (status === 'scope' ? Boolean(r.scope_url) : status === 'no_scope' ? !r.scope_url : r.status === status)));
}
export function paginate(records, requestedPage = 1, requestedSize = 12) {
  const size = [12, 24, 48].includes(Number(requestedSize)) ? Number(requestedSize) : 12;
  const totalPages = Math.max(1, Math.ceil(records.length / size));
  const number = Number(requestedPage);
  const page = Math.min(totalPages, Math.max(1, Number.isSafeInteger(number) ? number : 1));
  const start = (page - 1) * size;
  return { items: records.slice(start, start + size), page, size, totalPages,
    first: records.length ? start + 1 : 0, last: Math.min(start + size, records.length) };
}
