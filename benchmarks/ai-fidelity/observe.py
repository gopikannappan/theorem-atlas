"""Compile synthetic fixtures; never judge fidelity or grant certification."""
import hashlib
import json
import subprocess
from pathlib import Path

packet = json.loads(Path("/cases/cases.json").read_text())
observations = []
for case in packet["cases"]:
    relative = Path(case["lean_file"]).relative_to("benchmarks/ai-fidelity/v1")
    source = Path("/cases") / relative
    body = source.read_bytes()
    command = ["lean", str(source)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        observation = {"id": case["id"], "command": command, "source_sha256": hashlib.sha256(body).hexdigest(),
                       "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
                       "scope": "compiler_and_axioms_only", "fidelity": "not_evaluated", "certification": "none"}
    except subprocess.TimeoutExpired as error:
        observation = {"id": case["id"], "source_sha256": hashlib.sha256(body).hexdigest(),
                       "exit_code": None, "outcome": "timeout", "stdout": (error.stdout or b"").decode(errors="replace") if isinstance(error.stdout, bytes) else error.stdout,
                       "stderr": (error.stderr or b"").decode(errors="replace") if isinstance(error.stderr, bytes) else error.stderr,
                       "fidelity": "not_evaluated", "certification": "none"}
    observations.append(observation)
    print("FIXTURE_OBSERVATION " + json.dumps(observation), flush=True)
print("BENCHMARK_COMPILER_REPORT " + json.dumps({"benchmark_id": packet["benchmark_id"], "observations": observations, "certification": "none"}), flush=True)
if any(o["exit_code"] != 0 for o in observations):
    raise SystemExit(1)
