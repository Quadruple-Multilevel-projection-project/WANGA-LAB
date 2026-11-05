#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

usage() {
  echo "Usage: scripts/export.sh <version> <output-directory>" >&2
  echo "Requires: git, python3, syft, gitleaks, cosign, tar, sha256sum, and a clean tracked/untracked tree." >&2
  exit 2
}
[[ $# -eq 2 ]] || usage
VERSION="$1"
OUT_DIR="$2"
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([+-][0-9A-Za-z.-]+)?$ ]] || { echo "Invalid semantic version: $VERSION" >&2; exit 2; }
command -v git >/dev/null && command -v python3 >/dev/null && command -v syft >/dev/null && command -v gitleaks >/dev/null && command -v cosign >/dev/null && command -v tar >/dev/null && command -v sha256sum >/dev/null || {
  echo "BLOCKED: a required export tool is missing." >&2; exit 3;
}
: "${COSIGN_KEY:?Set COSIGN_KEY to the approved signing-key path; key contents are never printed.}"

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
if [[ -n "$(git status --porcelain)" ]]; then
  echo "BLOCKED: source tree is not clean; commit or remove changes before exporting." >&2
  exit 4
fi
COMMIT="$(git rev-parse HEAD)"
REPO_URL="$(git config --get remote.origin.url || true)"
[[ -n "$REPO_URL" ]] || { echo "BLOCKED: origin URL is missing." >&2; exit 4; }
[[ "$REPO_URL" == https://* ]] || { echo "BLOCKED: origin must be an HTTPS URL for the manifest." >&2; exit 4; }

mkdir -p "$OUT_DIR"
OUT_DIR="$(cd "$OUT_DIR" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
STAGE="$WORK/stage"
mkdir -p "$STAGE"
git archive "$COMMIT" | tar -x -C "$STAGE"

# Fail closed if disallowed tracked paths are present in the staged source.
if find "$STAGE" \( -name '.env' -o -name '.env.*' -o -iname '*.pem' -o -iname '*.key' -o -iname '*private-key*' -o -iname 'uploads' -o -iname 'customer-data' \) -print -quit | grep -q .; then
  echo "BLOCKED: staged source contains a prohibited secret/key/upload/customer-data path." >&2
  exit 5
fi

# Scan staged source content for likely secrets. Any finding blocks export.
gitleaks dir --no-git --redact "$STAGE"

# Generate an SPDX SBOM from the staged source. This is not a vulnerability scan.
syft "dir:$STAGE" -o spdx-json="$STAGE/SBOM.spdx.json"
mkdir -p "$STAGE"
export VERSION COMMIT REPO_URL
python3 - "$STAGE" <<'PY'
import hashlib, json, os, pathlib, sys
from datetime import datetime, timezone

stage = pathlib.Path(sys.argv[1])
version = os.environ["VERSION"]
commit = os.environ["COMMIT"]
repo_url = os.environ["REPO_URL"]
provenance = stage / "provenance.jsonl"
record = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "operation": "export-stage",
    "repository": repo_url,
    "commit_sha": commit,
    "version": version,
    "status": "PROPOSED"
}
provenance.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

files = []
for path in sorted(p for p in stage.rglob("*") if p.is_file()):
    if path.name in {"manifest.json", "SHA256SUMS"}:
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    files.append({
        "path": path.relative_to(stage).as_posix(),
        "sha256": digest,
        "size_bytes": path.stat().st_size
    })
manifest = {
    "bundle_id": f"wanga-deployment-{version}",
    "version": version,
    "source": {"repository": repo_url, "commit_sha": commit},
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "PROPOSED",
    "files": files,
    "sbom_ref": "SBOM.spdx.json",
    "provenance_ref": "provenance.jsonl",
    "signature_ref": "external cosign signature sidecar",
    "deployment_targets": ["compose", "kubernetes", "airgap"],
    "test_evidence_refs": []
}
(stage / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

(
  cd "$STAGE"
  find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
)
BUNDLE="$OUT_DIR/wanga-deployment-$VERSION.tar.gz"
tar -czf "$BUNDLE" -C "$STAGE" .
cosign sign-blob --yes --key "$COSIGN_KEY" --output-signature "$BUNDLE.sig" "$BUNDLE"
sha256sum "$BUNDLE" > "$BUNDLE.sha256"
echo "Created unsigned-status bundle artifact and signature sidecar:"
echo "  $BUNDLE"
echo "  $BUNDLE.sig"
echo "  $BUNDLE.sha256"
echo "STATUS: PROPOSED. This script does not run build/typecheck, smoke tests, vulnerability scans, deployment, or rollback."
