"""Score agreement with synthetic author intentions, never expert accuracy."""
import argparse
import hashlib
import json
from pathlib import Path

VERDICTS = {"aligned", "mismatch", "inconclusive"}

def score(packet, key, report, source_commit, packet_blob):
    ids = [case["id"] for case in packet["cases"]]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate packet IDs")
    if key["reference_status"] != "author_intent_only_expert_pending":
        raise ValueError("unexpected reference status")
    if report["source_commit"] != source_commit or report["packet_git_blob"] != packet_blob:
        raise ValueError("review is bound to different input")
    if report["benchmark_id"] != packet["benchmark_id"] or key["benchmark_id"] != packet["benchmark_id"]:
        raise ValueError("benchmark mismatch")
    def indexed(rows):
        result = {}
        for row in rows:
            if row["id"] in result:
                raise ValueError("duplicate case")
            result[row["id"]] = row
        if set(result) != set(ids):
            raise ValueError("missing or extra case")
        return result
    references, responses = indexed(key["cases"]), indexed(report["cases"])
    counts = dict(aligned_agreements=0, intended_defects_flagged=0,
                  intended_defects_missed=0, control_false_alarms=0,
                  inconclusive=0, category_agreements=0)
    rows = []
    for case_id in ids:
        expected, response = references[case_id], responses[case_id]
        verdict = response["verdict"]
        if verdict not in VERDICTS:
            raise ValueError("unknown verdict")
        for field in ("source_obligation", "lean_location", "explanation", "counterexample_or_scope_argument"):
            if not isinstance(response.get(field), str) or not response[field].strip():
                raise ValueError("missing diagnostic text")
        # Presence is checked; the mathematical correctness of diagnostics is ungraded.
        if verdict == "inconclusive":
            counts["inconclusive"] += 1
        elif expected["intended_label"] == "aligned":
            counts["aligned_agreements" if verdict == "aligned" else "control_false_alarms"] += 1
        else:
            counts["intended_defects_flagged" if verdict == "mismatch" else "intended_defects_missed"] += 1
            if verdict == "mismatch" and response["category"] == expected["intended_category"]:
                counts["category_agreements"] += 1
        rows.append(dict(id=case_id, author_intention=expected["intended_label"],
                         reviewer_verdict=verdict, agrees_with_author=verdict == expected["intended_label"]))
    return dict(benchmark_id=packet["benchmark_id"], reviewer_id=report["reviewer_id"],
                reference_status=key["reference_status"], expert_accuracy=None,
                diagnostic_correctness="ungraded", certification="none",
                total=len(ids), counts=counts, cases=rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default="benchmarks/ai-fidelity/v1")
    args = parser.parse_args()
    root = Path(args.directory)
    read = lambda name: json.loads((root / name).read_text())
    run = read("run.json")
    for filename, expected in (("cases.json", run["packet_git_blob"]), ("answer-key.json", run["key_git_blob"])):
        data = (root / filename).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if actual != expected:
            raise ValueError("frozen input content changed: " + filename)
    results = [score(read("cases.json"), read("answer-key.json"), read(path),
                     run["source_commit"], run["packet_git_blob"]) for path in run["reports"]]
    print(json.dumps(dict(reference_status="author_intent_only_expert_pending",
                          human_reference_available=False, results=results), indent=2))

if __name__ == "__main__":
    main()
