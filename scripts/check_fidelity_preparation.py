"""Check preparation integrity only; never infer fidelity or authenticate experts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = Path("benchmarks/ai-fidelity/real-source-pool")

def validate(pool, form, pilot, targets, observations):
    def require(condition, message):
        if not condition:
            raise ValueError(message)
    require(pool["state"] == "preparation_only" and pool["held_out"] is False,
            "public development pool cannot claim hidden evaluation")
    require(pool["performance_results"] is None and pool["human_reference_available"] is False,
            "no harder benchmark or human reference results exist")
    require(pool["certification"] == form["certification"] == "none", "no certification")
    require(form["state"] == "unassigned_template" and form["reference_status"] == "expert_pending",
            "template must not impersonate completed expert review")
    require(form["human_reference_available"] is False, "no expert reference available")
    require(all(value is None for value in form["reviewer"].values()), "reviewer slots are unassigned")
    known = {(row["repository"], row["commit"], row["file"], row["declaration"]): row for row in targets}
    seen = set()
    for family in pool["families"]:
        require(family["state"] == "public_development_candidate" and family["held_out_eligible"] is False,
                "family is public")
        require(family["reference_status"] == "expert_pending" and family["human_reviewer"] is None,
                "family not expert approved")
        require(family["variants_state"] == "design_only_not_compiled" and family["performance_results"] is None,
                "proposed designs are not compiled benchmark cases")
        require(family["certification"] == "none", "no family certification")
        require(family["questions"] and family["readiness_gaps"], "review gaps must be visible")
        require(family["source"].get("git_blob") or family["source"].get("sha256"), "source content identity missing")
        for row in family["targets"]:
            identity = (row["repository"], row["commit"], row["file"], row["declaration"])
            require(identity in known and identity not in seen, "unknown or duplicate target")
            seen.add(identity)
            expected = known[identity]
            for field in ("source_git_blob", "toolchain", "mathlib_commit", "url", "line", "dependencies"):
                require(row[field] == expected[field], "target evidence identity mismatch: " + field)
    first, second = form["first_pass"], form["second_pass"]
    require(first["status"] == second["status"] == "not_started", "review has not started")
    require(first["sealed_commit"] is None and first["exposure_declaration"] is None, "no seal or exposure evidence")
    require(second["reference_amendments"] == [], "no expert reference amendments")
    expected_ids = {row["id"] for row in pilot["cases"]}
    judgments = first["case_judgments"]
    require(len(judgments) == len(expected_ids) and {row["case_id"] for row in judgments} == expected_ids,
            "pilot judgment coverage mismatch")
    for row in judgments:
        require(row["source_commit"] == "5ad31c8ce250d75bec9acc65ec3bd05781dcb987" and
                row["packet_git_blob"] == "cc185fe638d76d954c3910af287b01d4660d10d4", "wrong frozen pilot")
        require(row["status"] == "pending" and all(row[key] is None for key in
                ("verdict", "source_obligation", "definition_trace", "scope_argument")), "unassigned judgments must stay blank")
        require(row["citations"] == row["ambiguities"] == [], "no adjudication evidence yet")
    real_rows = first["real_source_judgments"]
    expected_real = {(row["url"], row["source_git_blob"]) for family in pool["families"] for row in family["targets"]}
    require(len(real_rows) == len(expected_real) and
            {(row["target_url"], row["target_git_blob"]) for row in real_rows} == expected_real,
            "real source judgment coverage mismatch")
    for row in real_rows:
        require(row["status"] == "pending" and all(row[key] is None for key in
                ("verdict", "source_revision_adequate", "definition_trace", "scope_argument")),
                "real expert judgments must stay blank")
    grades = second["diagnostic_judgments"]
    expected_grades = {(reviewer, case) for reviewer in ("blind-pilot-a", "blind-pilot-b") for case in expected_ids}
    require(len(grades) == len(expected_grades) and
            {(row["reviewer_id"], row["case_id"]) for row in grades} == expected_grades, "diagnostic coverage mismatch")
    for row in grades:
        require(row["status"] == "pending" and all(row[key] is None for key in
                ("verdict_supported", "explanation_correct", "location_correct", "scope_argument_correct",
                 "unsupported_claims", "reason")), "no explanation grades yet")
    observed = {row["source_id"]: row for row in observations["observations"]}
    for family_id, source_id in (("erdos-152", "erdos152-companion"), ("imo-2025-p4", "imo2025-official")):
        source = next(row["source"] for row in pool["families"] if row["family_id"] == family_id)
        require(observed[source_id]["status"] == "observed" and
                observed[source_id]["sha256"] == source["sha256"], "PDF source hash mismatch")
        if source.get("git_blob"):
            require(observed[source_id]["git_blob"] == source["git_blob"], "PDF Git blob mismatch")
    return dict(families=len(pool["families"]), declarations=len(seen), pilot_slots=len(judgments),
                explanation_slots=len(grades), reference_status="expert_pending", certification="none")

def main():
    read = lambda path: json.loads((ROOT / path).read_text())
    targets = []
    for name in ("alphaproof", "harmonic-imo"):
        targets.extend(read(Path("audits/linked-declarations/groups") / (name + ".json"))["targets"])
    print(json.dumps(validate(read(PREFIX / "pool.json"), read(PREFIX / "adjudication-template.json"),
                              read("benchmarks/ai-fidelity/v1/cases.json"), targets,
                              read(PREFIX / "source-observations.json")), indent=2))

if __name__ == "__main__":
    main()
