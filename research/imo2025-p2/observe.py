"""Record a genuine full-problem attempt separately from coordinate lemmas.
No mathematical fidelity or catalogue acceptance decision is made here.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def run(command, seconds):
    try:
        p = subprocess.run(command, capture_output=True, text=True, timeout=seconds)
        return dict(command=command, exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr,
                    outcome="completed", timeout_seconds=seconds)
    except subprocess.TimeoutExpired as error:
        normalize = lambda value: value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        return dict(command=command, exit_code=None, stdout=normalize(error.stdout),
                    stderr=normalize(error.stderr), outcome="timeout", timeout_seconds=seconds)

def main():
    root = Path("/evidence")
    paths = ["/work/CoordinateCore.lean", "/work/FullTargetAttempt.lean"]
    report = dict(schema_version=1, source_sha256={path: hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in paths},
                  fidelity_review="pending independent review", certification="none")
    def save():
        (root / "observation.json").write_text(json.dumps(report, indent=2) + "\n")
    save()
    report["coordinate_core"] = run(["lake", "env", "lean", "-o", "/tmp/CoordinateCore.olean", paths[0]], 150)
    save()
    if report["coordinate_core"]["exit_code"] == 0:
        report["coordinate_module_replay"] = run(["lake", "env", "bash", "-c",
            'export LEAN_PATH="/tmp:$LEAN_PATH"; leanchecker CoordinateCore'], 90)
        report["replay_scope"] = "coordinate_module_only_imports_assumed; no fresh dependency replay"
        save()
    report["full_target_attempt"] = run(["lake", "env", "lean", paths[1]], 60)
    report["full_problem_complete"] = report["full_target_attempt"]["exit_code"] == 0
    report["scope_note"] = "Coordinate proofs alone do not prove the full affine-geometry target. Full-target diagnostics decide the attempt outcome; a failed target keeps this workflow red."
    save()
    print("IMO_P2_OBSERVATION " + json.dumps(report))
    sys.exit(0 if report["coordinate_core"]["exit_code"] == 0 and report["full_target_attempt"]["exit_code"] == 0 else 1)

if __name__ == "__main__":
    main()
