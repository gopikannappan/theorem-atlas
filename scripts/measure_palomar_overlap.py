"""Read-only, bounded Atlas/Palomar source-overlap measurement; no proof claims."""
import concurrent.futures
import hashlib
import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "comparison-output"
BASE = "https://data.palomar-registry.org/"
DIRECT = {"formalizes", "adapts", "independently-proves"}
OUT.mkdir(exist_ok=True)
(OUT / "snapshots").mkdir(exist_ok=True)
manifest = []
deadline = time.monotonic() + 480

def fetch(path):
    if time.monotonic() > deadline:
        raise RuntimeError("Overall comparison budget exhausted")
    url = urllib.parse.urljoin(BASE, path)
    if urllib.parse.urlsplit(url).netloc != "data.palomar-registry.org":
        raise ValueError("Unexpected data host")
    name = hashlib.sha256(url.encode()).hexdigest()
    error = None
    for _ in range(2):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "TheoremAtlasOverlap/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(request, timeout=20) as response:
                body = response.read(8 * 1024 * 1024 + 1)
            if len(body) > 8 * 1024 * 1024:
                raise ValueError("Response exceeds bound")
            value = json.loads(body)
            (OUT / "snapshots" / (name + ".json")).write_bytes(body)
            manifest.append({"url": url, "sha256": hashlib.sha256(body).hexdigest(), "file": "snapshots/" + name + ".json"})
            return value
        except (urllib.error.URLError, TimeoutError) as exc:
            error = exc
    raise RuntimeError("Data read failed: " + url) from error

def title_key(text):
    text = unicodedata.normalize("NFKD", text or "")
    return " ".join(re.findall(r"[a-z0-9]+", text.encode("ascii", "ignore").decode().lower()))

def document_key(url):
    if not isinstance(url, str):
        return None
    match = re.fullmatch(r"(?:arxiv:|https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/)([^?#]+)", url.strip(), re.I)
    if match:
        return "arxiv:" + re.sub(r"(?:\.pdf)?$", "", match.group(1), flags=re.I)
    match = re.fullmatch(r"(?:doi:|https?://(?:dx\.)?doi\.org/)(.+)", url.strip(), re.I)
    if match:
        return "doi:" + match.group(1).lower()
    parsed = urllib.parse.urlsplit(url.strip())
    pieces = urllib.parse.unquote(parsed.path).strip("/").split("/")
    if parsed.netloc.lower() == "github.com" and len(pieces) >= 5 and pieces[2] in {"blob", "raw"}:
        return "github:" + "/".join(pieces[:2]).lower() + "/" + "/".join(pieces[4:])
    if parsed.netloc.lower() == "raw.githubusercontent.com" and len(pieces) >= 4:
        return "github:" + "/".join(pieces[:2]).lower() + "/" + "/".join(pieces[3:])
    if parsed.scheme in {"https", "http"}:
        return parsed.netloc.lower() + parsed.path.rstrip("/")
    return None

def repo_key(url):
    return (url or "").removeprefix("https://github.com/").rstrip("/").removesuffix(".git").lower()

def measure(atlas, entries):
    direct = {}
    background = {}
    title_matches = {}
    exact = {}
    evidence = []
    for row in atlas:
        docs = {document_key(m["url"]) for m in row["manuscripts"]}
        docs.update(document_key(r["url"]) for r in row.get("references", []))
        docs.discard(None)
        titles = {title_key(m["title"]) for m in row["manuscripts"]}
        titles.add(title_key(row["title"]))
        titles.discard("")
        for entry in entries:
            source = entry.get("source", {})
            provenance = entry.get("provenance", {})
            locations = [source]
            substantive = provenance.get("substantive_formalization")
            if substantive:
                locations.append(substantive)
            proofs = entry.get("formalization", {}).get("theorem_names", [])
            for proof in row["proofs"]:
                if proof["declaration"] in proofs and any(repo_key(loc.get("repository")) == repo_key(proof["repository"]) and loc.get("commit") == proof["commit"] for loc in locations):
                    exact.setdefault(row["id"], set()).add(entry["id"])
            for paper in provenance.get("mathematical_sources", []):
                key = document_key(paper.get("identifier"))
                title = title_key(paper.get("title"))
                url_match = key is not None and key in docs
                title_match = bool(title and title in titles)
                if url_match or title_match:
                    relationship = paper["relationship"]
                    if relationship in DIRECT:
                        target = direct if url_match else title_matches
                    else:
                        target = background
                    target.setdefault(row["id"], set()).add(entry["id"])
                    evidence.append({"atlas_id": row["id"], "atlas_title": row["title"], "palomar_id": entry["id"], "palomar_version": entry["version"], "palomar_title": entry["title"], "relationship": relationship, "basis": "source_document_identifier" if url_match else "exact_normalized_source_title", "paper": paper})
    research = [r for r in atlas if r["kind"] in {"result_family", "formalization_project"}]
    openai = [r for r in atlas if r["source"] == "OpenAI mathematics"]
    candidates = set(direct) | set(title_matches)
    def metric(rows):
        ids = {r["id"] for r in rows}
        def count(matches):
            n = len(ids & set(matches))
            return {"matched": n, "denominator": len(ids), "percent": round(100 * n / len(ids), 3) if ids else None}
        return {"exact_selected_declaration_and_commit": count(exact), "direct_source_document_identifiers_ignoring_github_commit": count(direct), "source_identifier_or_exact_title_candidates": count(candidates), "background_source_references": count(background)}
    return {"all_atlas_records": metric(atlas), "research_family_or_project_records": metric(research), "openai_result_families": metric(openai), "candidate_evidence": evidence, "exact_matches": {k: sorted(v) for k,v in exact.items()}, "limitations": ["Source references and exact normalized titles identify candidate relationships, not theorem equivalence or full family coverage.", "GitHub source-document matching ignores commit but preserves repository and file path, so different manuscript revisions remain a limitation.", "No fuzzy title matching, dependency-reuse counting, LLM judgment, or proof execution is used.", "A zero exact selected-declaration match does not mean zero mathematical overlap."]}

def main():
    atlas_bytes = (ROOT / "catalog/results.json").read_bytes()
    atlas = json.loads(atlas_bytes)["results"]
    summaries = []
    cursor = None
    release = None
    totals = None
    for page in range(100):
        query = {"order": "updated"}
        if cursor:
            query["cursor"] = cursor
        document = fetch("api/v1/results?" + urllib.parse.urlencode(query))
        print("PAGE", page + 1, "keys", sorted(document), flush=True)
        if release is None:
            release, totals = document["release"], document["totals"]
        if document["release"] != release:
            raise RuntimeError("Registry changed during traversal; no complete percentage produced")
        summaries.extend(document["entries"])
        cursor = document["next"]
        if cursor is None:
            break
    else:
        raise RuntimeError("Listing exceeds page budget")
    ids = [r["id"] for r in summaries]
    if len(ids) != len(set(ids)) or len(ids) != totals["results"]:
        raise RuntimeError("Listing incomplete or duplicate IDs")
    paths = ["entries/" + row["id"] + "-v" + str(row["version"]) + ".json" for row in summaries]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        entries = list(executor.map(fetch, paths))
    if any(e["id"] != row["id"] or e["version"] != row["version"] for e,row in zip(entries,summaries)):
        raise RuntimeError("Entry identity mismatch")
    report = measure(atlas, entries)
    report.update({"measured_at": datetime.now(timezone.utc).isoformat(), "atlas_catalogue_sha256": hashlib.sha256(atlas_bytes).hexdigest(), "palomar_release": release, "palomar_totals": totals, "palomar_entries_read": len(entries), "source_snapshots": manifest, "complete_registry_listing": True})
    (OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (OUT / "registry-entries.json").write_text(json.dumps(entries, ensure_ascii=False))
    print("OVERLAP_REPORT " + json.dumps({k:v for k,v in report.items() if k != "source_snapshots"}, ensure_ascii=False), flush=True)

if __name__ == "__main__":
    try:
        main()
    finally:
        (OUT / "fetch-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
