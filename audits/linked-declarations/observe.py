"""Collect compiler and checker observations, never approve an audit."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

g = json.loads(Path("/audit/group.json").read_text())
root = Path("/source") / g["root"]
deadline = time.monotonic() + g.get("observation_seconds", 900) - 60
observations = []
def run(label, args, limit):
    remaining = min(limit, int(deadline - time.monotonic()))
    if remaining <= 0:
        return {"exit_code": None, "outcome": "group_budget_exhausted"}
    print("OBSERVATION_BEGIN " + json.dumps({"label": label, "command": args, "timeout_seconds": remaining}), flush=True)
    p = subprocess.Popen(args, cwd=root, start_new_session=True)
    try:
        rc = p.wait(timeout=remaining)
        result = {"exit_code": rc, "outcome": "completed" if rc == 0 else "failed"}
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        p.wait()
        result = {"exit_code": None, "outcome": "timeout"}
    print("OBSERVATION_END " + json.dumps({"label": label, **result}), flush=True)
    return result
# Finish compiler observations before spending the budget on replay.
for target in g["targets"]:
    o = {"target_id": target["target_id"], "declaration": target["declaration"],
         "source_commit": g["commit"], "fidelity_review": "pending",
         "independent_trust_review": "pending", "external_checker": "not_run"}
    source = Path("/source") / target["file"]
    o["source_sha256_before"] = hashlib.sha256(source.read_bytes()).hexdigest()
    o["build"] = run(target["target_id"] + ":build", ["lake", "build", target["module"]], g.get("build_seconds", 480))
    if o["build"].get("exit_code") == 0:
        o["declaration_and_axioms"] = run(target["target_id"] + ":probe",
            ["lake", "env", "lean", "--root=/audit/probes", "/audit/probes/" + target["probe"]], 90)
    o["source_sha256_after"] = hashlib.sha256(source.read_bytes()).hexdigest()
    o["source_unchanged"] = o["source_sha256_before"] == o["source_sha256_after"]
    observations.append(o)
    print("TARGET_COMPILER_OBSERVATION " + json.dumps(o), flush=True)

checker = Path("/audit/checker-path").read_text().strip()
built = []
for target, o in zip(g["targets"], observations):
    if o["build"].get("exit_code") == 0:
        built.append(target)
        o["module_replay_imports_assumed"] = run(target["target_id"] + ":module_replay",
            ["lake", "env", checker, target["module"]], 60)

# One fresh replay of the union of successfully built modules avoids repeating
# the same large imported environment for every alternative proof.
fresh = {"exit_code": None, "outcome": "no_built_modules"}
if built:
    union_source = Path("/audit/probes/AtlasAuditGroup.lean")
    # The immutable union probe is prepared by the controller before proof builds.
    # If a target build failed, do not silently shrink the replay scope.
    if len(built) != len(g["targets"]):
        fresh = {"exit_code": None, "outcome": "incomplete_group_build"}
    else:
        output = root / ".lake/build/lib/lean/AtlasAuditGroup.olean"
        output.parent.mkdir(parents=True, exist_ok=True)
        probe = run(g["id"] + ":union_probe",
            ["lake", "env", "lean", "--root=/audit/probes", "-o", str(output), str(union_source)], 90)
        if probe.get("exit_code") == 0:
            fresh = run(g["id"] + ":fresh_group_replay",
                ["lake", "env", checker, "--fresh", "AtlasAuditGroup"], g.get("fresh_replay_seconds", 180))
        else:
            fresh = {"exit_code": None, "outcome": "union_probe_failed"}
for o in observations:
    o["fresh_group_replay"] = fresh
    print("TARGET_OBSERVATION " + json.dumps(o), flush=True)
print("GROUP_OBSERVATIONS " + json.dumps({"group": g["id"], "targets": observations, "certification": "none"}), flush=True)
if any(o["build"].get("exit_code") != 0 or
       o.get("declaration_and_axioms", {}).get("exit_code") != 0 or
       o.get("module_replay_imports_assumed", {}).get("exit_code") != 0 or
       not o["source_unchanged"] for o in observations) or fresh.get("exit_code") != 0:
    raise SystemExit(1)
