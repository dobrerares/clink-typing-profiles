#!/usr/bin/env python3
"""Build manifest.json for a Clink profile release from Profiles/*.clinkprofile."""
import hashlib, json, pathlib

root = pathlib.Path(__file__).resolve().parents[1]
packs = []
for path in sorted((root / "Profiles").glob("*.clinkprofile")):
    raw = path.read_bytes(); profile = json.loads(raw)
    packs.append({"id": path.stem, "name": profile["name"], "icon": profile["icon"], "version": "latest", "asset": {"path": path.name, "url": f"https://github.com/{__import__('os').environ.get('GITHUB_REPOSITORY', 'anti-ltd/clink-profiles')}/releases/download/latest/{path.name}", "sha256": hashlib.sha256(raw).hexdigest(), "byteCount": len(raw)}})
(root / "manifest.json").write_text(json.dumps({"version": "latest", "profiles": packs}, indent=2) + "\n")
