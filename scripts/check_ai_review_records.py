"""Check AI review record integrity, not mathematical fidelity or certification."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"[0-9a-f]{40}")
VERDICTS = {"recommend_pass", "changes_requested", "inconclusive"}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def git_blob(body):
    return hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()

def safe_path(path):
    require(isinstance(path, str) and path.startswith("audits/ai-fidelity/"), "Unexpected record path")
    require("\\" not in path and ".." not in Path(path).parts and not Path(path).is_absolute(), "Invalid record path")
    return path

def validate_records(packet, session, read_bytes):
    """Validate declared metadata and hashes. No verdict is interpreted as approval."""
    require(packet.get("schema_version") == session.get("schema_version") == 1, "Unsupported schema")
    require(packet.get("certification") == session.get("certification") == "none", "Certification is unsupported")
    require(packet.get("policy_state") == session.get("policy_state") == "draft_independent_review_pending", "Policy approval is unsupported")
    require(packet.get("state") == "frozen" and session.get("state") == "recommendations_received", "Unsupported state")
    require(session.get("session_id") == packet.get("packet_id"), "Packet/session mismatch")
    ref = session["packet"]
    require(SHA.fullmatch(ref["freeze_commit"]) and SHA.fullmatch(ref["git_blob"]), "Invalid packet pin")
    require(git_blob(read_bytes(safe_path(ref["path"]))) == ref["git_blob"], "Packet bytes changed")
    target, manuscript = packet["target"], packet["manuscript"]
    for obj, blob_key in [(target, "source_git_blob"), (manuscript, "git_blob")]:
        require(SHA.fullmatch(obj["commit"]) and SHA.fullmatch(obj[blob_key]), "Unpinned source")
        require(obj["url"].startswith(obj["repository"] + "/blob/" + obj["commit"] + "/" + obj["file"]), "Source URL/pin mismatch")
    require(SHA.fullmatch(target["mathlib_commit"]) and SHA.fullmatch(target["manifest_git_blob"]), "Unpinned dependencies")
    require(target["file"].endswith(".lean") and target["declaration"] and target["toolchain"], "Missing Lean target")
    require(packet["generation"].get("author_rationale_included") is False, "Author rationale must be excluded")
    reviewers = session["reviewers"]
    require(len(reviewers) == 2 and len({r["id"] for r in reviewers}) == 2
            and len({r["agent_path"] for r in reviewers}) == 2, "Two distinct declared reviewer identities required")
    for r in reviewers:
        require(r["fresh_context"] is True and r["generated_target"] is False
                and r["other_review_seen_before_initial_freeze"] is False
                and r["author_rationale_seen_before_initial_freeze"] is False, "Declared reviewer separation failed")
        require(r["scope"] == "statement_fidelity_recommendation" and r["certification"] == "none", "Review scope cannot certify")
        require(r["initial_verdict"] in VERDICTS and r["amended_verdict"] in VERDICTS, "Unsupported verdict")
        require(bool(r["model_family"]) and SHA.fullmatch(r["archive_commit"]), "Missing reviewer provenance")
        require(len(r["files"]) >= 2, "Original report and amendment required")
        for f in r["files"]:
            require(SHA.fullmatch(f["git_blob"]), "Invalid report pin")
            require(git_blob(read_bytes(safe_path(f["path"]))) == f["git_blob"], "Frozen report bytes changed")
    require(session.get("provenance_complete") is False and session["reconciliation"]["unresolved"], "First session limitations must remain explicit")
    return {"session": session["session_id"], "reviewer_count": len(reviewers), "certification": "none"}

def main():
    for path in sorted((ROOT / "audits/ai-fidelity/sessions").glob("*.json")):
        session = json.loads(path.read_text())
        packet = json.loads((ROOT / safe_path(session["packet"]["path"])).read_text())
        result = validate_records(packet, session, lambda name: (ROOT / name).read_bytes())
        print(json.dumps(result) + " — record integrity only; no mathematical approval")

if __name__ == "__main__":
    main()
