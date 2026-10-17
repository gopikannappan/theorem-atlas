"""Bounded compiler/module observations, not fidelity approval."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

SOURCE = Path("/work/PrimeOffsetTwo.lean")
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
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    compiler = run(["lake", "env", "lean", "-o", "/tmp/PrimeOffsetTwo.olean",
                    str(SOURCE)], 120)
    report = dict(schema_version=1, source_sha256=source_hash, compiler=compiler,
                  fidelity_review="pending independent review", certification="none")
    (root / "observation.json").write_text(json.dumps(report, indent=2) + "\n")
    if compiler["exit_code"] == 0:
        report["module_replay"] = run(["lake", "env", "bash", "-c",
            'export LEAN_PATH="/tmp:$LEAN_PATH"; leanchecker PrimeOffsetTwo'], 90)
        report["module_replay_scope"] = "selected_module_only_imports_assumed; no fresh dependency replay"
        (root / "observation.json").write_text(json.dumps(report, indent=2) + "\n")
    print("FAMILY_OBSERVATION " + json.dumps(report))
    # This workflow observes compilation. Optional replay outcome stays explicit.
    sys.exit(0 if compiler["exit_code"] == 0 else 1)

if __name__ == "__main__":
    main()
