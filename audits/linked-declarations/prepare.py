"""Prepare a pinned public project inside a credential-free CI image."""
import hashlib
import json
import os
import pwd
from pathlib import Path
import re
import subprocess

g = json.loads(Path("/audit/group.json").read_text())
def run(args, cwd=None):
    print("PREP_COMMAND " + json.dumps(args), flush=True)
    subprocess.run(args, cwd=cwd, check=True, timeout=600)
def clone(url, sha, dest):
    if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?", url):
        raise ValueError("Only public GitHub repository URLs are supported")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("A full commit pin is required")
    run(["git", "init", str(dest)])
    run(["git", "remote", "add", "origin", url], dest)
    run(["git", "fetch", "--depth=1", "origin", sha], dest)
    run(["git", "checkout", "--detach", "FETCH_HEAD"], dest)
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=dest, text=True).strip()
    if actual != sha:
        raise ValueError("Source commit mismatch")

release = g["lean_release"]
version = release["version"]
if not re.fullmatch(r"v4\.\d+\.\d+(?:-rc\d+)?", version):
    raise ValueError("Unsupported Lean version")
expected_url = "https://github.com/leanprover/lean4/releases/download/" + version + "/lean-" + version[1:] + "-linux.tar.zst"
if release["url"] != expected_url:
    raise ValueError("Unexpected release URL")
archive = Path("/tmp/lean.tar.zst")
run(["curl", "--fail", "--location", "--connect-timeout", "20", "--max-time", "180", "--retry", "2", release["url"], "-o", str(archive)])
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
print("LEAN_ARCHIVE " + json.dumps({"url": release["url"], "asset_id": release["asset_id"], "observed_sha256": digest, "expected_sha256": release["sha256"], "sha256_basis": release.get("sha256_basis", "github_asset_digest"), "published_sha256": release["sha256"] if release.get("sha256_basis", "github_asset_digest") == "github_asset_digest" else None}), flush=True)
if release["sha256"] and digest != release["sha256"]:
    raise ValueError("Lean release checksum mismatch")
Path("/opt/lean").mkdir()
run(["tar", "--zstd", "-xf", str(archive), "-C", "/opt/lean", "--strip-components=1"])
archive.unlink()
os.environ["PATH"] = "/opt/lean/bin:" + os.environ["PATH"]
clone(g["repository"], g["commit"], Path("/source"))
root = Path("/source") / g["root"]
if root.joinpath("lean-toolchain").read_text().strip() != g["toolchain"]:
    raise ValueError("Toolchain differs from inventory")
manifest_file = root / "lake-manifest.json"
manifest_bytes = manifest_file.read_bytes()
manifest = json.loads(manifest_bytes)
if next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib") != g["mathlib_commit"]:
    raise ValueError("Mathlib pin differs from inventory")
for package in manifest["packages"]:
    if package["type"] != "git" or not re.fullmatch(r"[0-9a-f]{40}", package["rev"]):
        raise ValueError("Unpinned or unsupported dependency")
    if not package["url"].startswith("https://github.com/"):
        raise ValueError("Unexpected dependency host")
print("SOURCE_MANIFEST_SHA256 " + hashlib.sha256(manifest_bytes).hexdigest(), flush=True)
# Lake configuration executes here, inside the image build, without credentials.
# No target proof is built in this network-enabled preparation phase.
# Upstream configuration/cache commands run unprivileged; protect observer and tools.
observer = pwd.getpwuid(1000).pw_name
run(["chown", "-R", "1000:1000", "/source"])
os.environ["MATHLIB_CACHE_DIR"] = "/tmp/atlas-mathlib-cache"
run(["runuser", "-u", observer, "--", "/opt/lean/bin/lake", "exe", "cache", "get"], root)
if manifest_file.read_bytes() != manifest_bytes:
    raise ValueError("Lake changed the upstream lockfile; retain diagnostics and review")
for package in manifest["packages"]:
    folder = root / manifest["packagesDir"] / package["name"]
    if not folder.is_dir():
        folder = root / manifest["packagesDir"] / package["name"].strip("«»")
    actual = subprocess.check_output(["git", "-c", "safe.directory=" + str(folder), "rev-parse", "HEAD"], cwd=folder, text=True).strip()
    if actual != package["rev"]:
        raise ValueError("Dependency HEAD differs from lockfile: " + package["name"])
    print("DEPENDENCY_PIN " + json.dumps({"name": package["name"], "commit": actual}), flush=True)
# Apply only the patch files supplied by the exact upstream source commit.
# This mirrors its recorded post_update patch step without resolving moving refs.
observer_uid = pwd.getpwuid(1000).pw_name
for label in g.get("upstream_patch_labels", []):
    match = next(p for p in manifest["packages"] if p["name"].strip("«»") == label)
    folder = root / manifest["packagesDir"] / match["name"]
    if not folder.is_dir():
        folder = root / manifest["packagesDir"] / label
    patch = root / "patches" / (label + "-lean4341.patch")
    body = patch.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
    published_blob = subprocess.check_output(
        ["git", "-c", "safe.directory=/source", "rev-parse",
         g["commit"] + ":" + str(patch.relative_to(Path("/source")))],
        cwd="/source", text=True).strip()
    if blob != published_blob:
        raise ValueError("Upstream patch differs from committed source: " + label)
    base = ["runuser", "-u", observer_uid, "--", "git", "-C", str(folder), "apply"]
    reverse = subprocess.run(base + ["--reverse", "--check", str(patch)], capture_output=True)
    if reverse.returncode != 0:
        run(base + ["--check", str(patch)])
        run(base + [str(patch)])
    run(base + ["--reverse", "--check", str(patch)])
    print("UPSTREAM_PATCH " + json.dumps({
        "package": label, "source_commit": g["commit"],
        "path": str(patch.relative_to(Path("/source"))),
        "git_blob": blob, "sha256": hashlib.sha256(body).hexdigest(),
        "already_applied": reverse.returncode == 0}), flush=True)

checker = g["checker"]
if checker["kind"] == "lean4checker":
    clone(checker["repository"], checker["commit"], Path("/checker"))
    if Path("/checker/lean-toolchain").read_text().strip() != g["toolchain"]:
        raise ValueError("Checker toolchain mismatch")
    run(["lake", "build", "lean4checker"], Path("/checker"))
    checker_binary = "/checker/.lake/build/bin/lean4checker"
else:
    checker_binary = "/opt/lean/bin/leanchecker"
if not Path(checker_binary).is_file():
    raise ValueError("Pinned checker binary is unavailable")
Path("/audit/checker-path").write_text(checker_binary + "\n")
Path("/audit/probes").mkdir()
for target in g["targets"]:
    probe = "import " + target["module"] + "\n\nset_option pp.fullNames true\nset_option pp.universes true\nset_option pp.notation false\n#check @" + target["declaration"] + "\n#print axioms " + target["declaration"] + "\n"
    Path("/audit/probes").joinpath(target["probe"]).write_text(probe)
union = "\n".join("import " + t["module"] for t in g["targets"]) + "\n"
Path("/audit/probes/AtlasAuditGroup.lean").write_text(union)
run(["chmod", "-R", "a+rX", "/source", "/audit"])
run(["chown", "-R", "1000:1000", "/source"])
if Path("/checker").exists():
    run(["chmod", "-R", "a+rX", "/checker"])

