"""Bounded supporting-lemma experiment. Records compiler output, grants no audit state."""
import hashlib
import json
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLCHAIN = (ROOT / 'lean-toolchain').read_text().strip()


def main():
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = ROOT / 'attempts' / run_id
    output.mkdir(parents=True)
    record = {'run_id': run_id, 'result_id': 'openai-math:005',
              'target_kind': 'supporting_lemma_experiment',
              'declaration': 'TheoremAtlas.Pilot.odd_denominator_ne_zero',
              'assumptions': 'n is a natural number',
              'statement': '∀ n : ℕ, 2 * n + 1 ≠ 0',
              'scope': 'Natural-number denominator nonvanishing only; not Catalan irrationality.',
              'source_url': 'https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Catalans-constant-is-irrational-September-24-2026/paper.pdf',
              'upstream_commit': '1581d4cbdd69a0faf34b2089614fe2a814316a6a',
              'local_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'local_worktree_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True)),
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'toolchain': TOOLCHAIN, 'dependencies': ['Lean core: Nat.succ_ne_zero'],
              'generator': 'Codex session; exact model/version unavailable',
              'budget': {'max_attempts': 2, 'timeout_seconds_per_attempt': 30},
              'estimated_compute_cost': None, 'fidelity_review': 'unreviewed',
              'audit_state': 'not_audited', 'attempts': []}
    def checkpoint():
        (output / 'record.json').write_text(json.dumps(record, indent=2) + '\n')
    checkpoint()
    # These experiments are generated separately from the compiler invocation.
    strategies = [('reflexivity baseline', 'rfl'),
                  ('use core successor nonvanishing', 'exact Nat.succ_ne_zero (2 * n)')]
    for index, (strategy, proof) in enumerate(strategies, 1):
        source = ('namespace TheoremAtlas.Pilot\n'
                  'theorem odd_denominator_ne_zero (n : Nat) : 2 * n + 1 ≠ 0 := by\n'
                  f'  {proof}\nend TheoremAtlas.Pilot\n'
                  '#print axioms TheoremAtlas.Pilot.odd_denominator_ne_zero\n')
        (output / f'attempt-{index}.lean').write_text(source)
        started = time.monotonic()
        command = ['lean', f'+{TOOLCHAIN}', 'Pilot.lean']
        with tempfile.TemporaryDirectory(prefix='theorem-atlas-') as clean:
            workspace = Path(clean)
            (workspace / 'lean-toolchain').write_text(TOOLCHAIN + '\n')
            (workspace / 'Pilot.lean').write_text(source)
            try:
                run = subprocess.run(command, cwd=clean, capture_output=True, text=True, timeout=30)
                diagnostic, code = run.stdout + run.stderr, run.returncode
            except subprocess.TimeoutExpired as exc:
                diagnostic = 'TIMEOUT\n' + str(exc.stdout or '') + str(exc.stderr or '')
                code = None
            except OSError as exc:
                diagnostic, code = str(exc), None
        (output / f'attempt-{index}.log').write_text(diagnostic)
        record['attempts'].append({'index': index, 'strategy': strategy, 'command': command,
                                   'exit_code': code, 'elapsed_seconds': time.monotonic() - started,
                                   'source_sha256': hashlib.sha256(source.encode()).hexdigest()})
        checkpoint()
        if code == 0:
            break
    record['outcome'] = 'compiler_accepted_unreviewed' if record['attempts'][-1]['exit_code'] == 0 else 'incomplete'
    checkpoint()
    (output / 'REPORT.md').write_text(
        '# Supporting lemma experiment\n\n'
        f'Outcome: `{record["outcome"]}`. See record.json and all attempt logs.\n\n'
        'This experiment establishes no catalogue audit or fidelity status. The target only '
        'addresses a natural-number denominator, not convergence, real casts, or irrationality. '
        'Axioms output is a diagnostic, not a sufficient trust audit. No Mathlib build was run.\n\n'
        'Reproduce: `python3 scripts/run_pilot.py` (requires the pinned Lean toolchain).\n')
    print(output.relative_to(ROOT), record['outcome'])

if __name__ == '__main__':
    main()
