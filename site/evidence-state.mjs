// Display recorded observations; this module confers no audit or fidelity status.
const fields = ['url', 'commit', 'declaration', 'toolchain', 'mathlib_commit'];
export function attachObservations(records, snapshot) {
  if (snapshot?.schema_version !== 1 || !Array.isArray(snapshot.observations)) throw new Error('Unsupported evidence snapshot');
  return records.map(record => ({ ...record, observations: record.proofs.map(proof =>
    snapshot.observations.find(o => o.record_id === record.id
      && fields.every(field => typeof proof[field] === 'string' && proof[field] === o.proof?.[field])) || null) }));
}
export function observationStages(observation) {
  const attempts = observation?.attempts || [];
  return {
    compiled: attempts.some(a => a.build?.exit_code === 0 && a.probe?.exit_code === 0),
    module_replayed: attempts.some(a => a.module_replay?.exit_code === 0),
    fresh_replayed: attempts.some(a => a.fresh_replay?.exit_code === 0),
    trust_flag: attempts.some(a => a.axioms?.some(line => line.includes('Lean.ofReduceBool'))),
  };
}
export function hasStage(record, stage) {
  return stage === 'review_pending' ? record.proofs.length > 0
    : (record.observations || []).some(o => observationStages(o)[stage] === true);
}
export function outcomeLabel(result) {
  if (result?.exit_code === 0) return 'Passed';
  return ({ timeout: 'Timed out', failed: 'Failed', incomplete_group_build: 'Skipped: incomplete group build',
    no_built_modules: 'Not run: build incomplete', group_budget_exhausted: 'Budget exhausted',
    union_probe_failed: 'Not run: import probe failed', not_run: 'Not run' })[result?.outcome] || 'Not run';
}
