"""Collect compiler and checker observations, never approve an audit."""
import json
from pathlib import Path
import subprocess
import time

g = json.loads(Path("/audit/group.json").read_text())
root = Path("/source") / g["root"]
deadline = time.monotonic() + 840
observations = []
def run(label, args, limit):
    remaining = min(limit, int(deadline - time.monotonic()))
    if remaining <= 0:
        return {"exit_code": None, "outcome": "group_budget_exhausted"}
    print("OBSERVATION_BEGIN " + json.dumps({"label": label, "command": args, "timeout_seconds": remaining}), flush=True)
    try:
        p = subprocess.run(args, cwd=root, timeout=remaining)
        result = {"exit_code": p.returncode, "outcome": "completed" if p.returncode == 0 else "failed"}
    except subprocess.TimeoutExpired:
        result = {"exit_code": None, "outcome": "timeout"}
    print("OBSERVATION_END " + json.dumps({"label": label, **result}), flush=True)
    return result
for target in g["targets"]:
    o = {"target_id": target["target_id"], "declaration": target["declaration"],
         "source_commit": g["commit"], "fidelity_review": "pending",
         "independent_trust_review": "pending", "external_checker": "not_run"}
    # Each build is scoped to the original target module; upstream options are retained.
    o["build"] = run(target["target_id"] + ":build", ["lake", "build", target["module"]], 480)
    if o["build"].get("exit_code") == 0:
        o["declaration_and_axioms"] = run(target["target_id"] + ":probe", ["lake", "env", "lean", target["probe"]], 90)
        checker = Path("/audit/checker-path").read_text().strip()
        o["kernel_replay"] = run(target["target_id"] + ":kernel_replay",
            ["lake", "env", checker, "--fresh", target["module"]], 180)
    observations.append(o)
    print("TARGET_OBSERVATION " + json.dumps(o), flush=True)
print("GROUP_OBSERVATIONS " + json.dumps({"group": g["id"], "targets": observations, "certification": "none"}), flush=True)
# Job failure reflects failed/incomplete operations, not mathematical invalidity.
if any(o["build"].get("exit_code") != 0 or
       o.get("declaration_and_axioms", {}).get("exit_code") != 0 or
       o.get("kernel_replay", {}).get("exit_code") != 0 for o in observations):
    raise SystemExit(1)
