#!/usr/bin/env python3
"""Build an immutable Clink profile manifest; --output leaves old artifacts intact."""
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_REPOSITORY = "dobrerares/clink-typing-profiles"


def build_manifest(root, repository):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("repository must be OWNER/REPO")
    paths = sorted(p for p in (root / "Profiles").glob("*.clinkprofile")
                   if not p.name.startswith("."))
    if not paths:
        raise ValueError("no visible Profiles/*.clinkprofile files")
    profiles = []
    ids = set()
    for path in paths:
        raw = path.read_bytes()
        if len(raw) >= 256 * 1024:
            raise ValueError(f"{path.name}: profile must be smaller than 256 KB")
        result = subprocess.run([sys.executable, str(ROOT / "tools/validate-profile.py"),
                                 str(path)], capture_output=True, text=True)
        if result.returncode:
            raise ValueError(f"{path.name}: {result.stderr.strip() or result.stdout.strip()}")
        profile = json.loads(raw)
        if profile["id"] in ids:
            raise ValueError(f"duplicate profile id: {profile['id']}")
        ids.add(profile["id"])
        profiles.append((path, raw, profile, hashlib.sha256(raw).hexdigest()))
    # Match upstream's compact JSON encoding of sorted (filename, SHA-256) pairs.
    version = "profiles-" + hashlib.sha256(json.dumps(
        [(path.name, digest) for path, raw, profile, digest in profiles],
        separators=(",", ":")).encode()).hexdigest()
    packs = []
    for path, raw, profile, digest in profiles:
        # Retain upstream/catalog filename IDs; do not migrate existing profile IDs.
        packs.append({"id": path.stem, "name": profile["name"], "icon": profile["icon"],
                      "version": version, "asset": {
                          "path": path.name,
                          "url": f"https://github.com/{repository}/releases/download/{version}/{path.name}",
                          "sha256": digest, "byteCount": len(raw)}})
    return {"version": version, "profiles": packs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPOSITORY))
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "manifest.json")
    parser.add_argument("--check", action="store_true", help="compare output without writing")
    args = parser.parse_args()
    try:
        rendered = json.dumps(build_manifest(ROOT, args.repository), indent=2) + "\n"
        if args.check:
            if not args.output.is_file() or args.output.read_text() != rendered:
                raise ValueError(f"{args.output}: manifest is missing or stale; rebuild explicitly")
            print(f"Manifest matches: {args.output}")
        else:
            args.output.write_text(rendered)
            print(f"Built: {args.output}")
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
