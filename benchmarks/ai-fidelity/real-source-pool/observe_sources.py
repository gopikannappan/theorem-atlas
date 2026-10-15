"""Bounded remote source observations; never a mathematical verifier."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import urllib.request

SOURCES = [
    dict(id="erdos152-companion", url="https://raw.githubusercontent.com/google-deepmind/alphaproof-nexus-results/0647711a71183c1ea492ad60860776617ce1ea88/NaturalLanguageProofs/ErdosProblems/erdos152.pdf", git_blob="10cf3a8b982d128816dc66aff4bfc8cb9d260147", excerpt=True),
    dict(id="imo2025-official", url="https://www.imo-official.org/assets/documents/problems/2025/2025_eng.pdf", git_blob=None, excerpt=False),
]

def observe(source):
    result = dict(source_id=source["id"], url=source["url"], status="failed", certification="none")
    try:
        request = urllib.request.Request(source["url"], headers={"User-Agent": "TheoremAtlas-SourceObservation/1"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read(4_000_001)
            result["resolved_url"] = response.url
        if len(data) > 4_000_000:
            raise ValueError("source size exceeds budget")
        result["sha256"] = hashlib.sha256(data).hexdigest()
        result["git_blob"] = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if source["git_blob"] and result["git_blob"] != source["git_blob"]:
            raise ValueError("pinned Git blob mismatch")
        if not data.startswith(b"%PDF-"):
            raise ValueError("expected PDF")
        result["byte_count"] = len(data)
        if source["excerpt"]:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "source.pdf"
                path.write_bytes(data)
                command = ["pdftotext", "-f", "1", "-l", "1", "-layout", str(path), "-"]
                process = subprocess.run(command, capture_output=True, text=True, timeout=20)
                result["extraction_exit_code"] = process.returncode
                result["extraction_stderr"] = process.stderr
                if process.returncode:
                    raise ValueError("PDF text extraction failed")
                result["page_one_excerpt"] = " ".join(process.stdout.split()[:180])
                result["excerpt_scope"] = "First 180 whitespace-separated words of page1; not a full manuscript review"
        result["status"] = "observed"
    except Exception as error:
        result["error"] = type(error).__name__ + ": " + str(error)
    return result

def main():
    observations = [observe(source) for source in SOURCES]
    report = dict(schema_version=1, observations=observations, certification="none",
                  scope="source_bytes_and_bounded_excerpt_only")
    path = Path("source-evidence")
    path.mkdir(exist_ok=True)
    (path / "observations.json").write_text(json.dumps(report, indent=2) + "\n")
    print("SOURCE_OBSERVATION " + json.dumps(report))
    raise SystemExit(0 if all(row["status"] == "observed" for row in observations) else 1)

if __name__ == "__main__":
    main()
