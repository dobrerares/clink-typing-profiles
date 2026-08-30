#!/usr/bin/env python3
"""Explain plainly whether a .clinkprofile is safe for Clink to publish."""
import json, pathlib, re, sys

path = pathlib.Path(sys.argv[1] if len(sys.argv) == 2 else "")
if not path.is_file():
    raise SystemExit("Usage: python3 tools/validate-profile.py Profiles/my-profile.clinkprofile")
try:
    profile = json.loads(path.read_text())
except Exception as error:
    raise SystemExit(f"This is not valid JSON: {error}")
for key in ("id", "name", "icon", "config"):
    if key not in profile:
        raise SystemExit(f"Missing '{key}'. Copy one of the included profiles and keep all four fields.")
if not isinstance(profile["id"], str) or not re.fullmatch(r"[a-z0-9_.-]+", profile["id"]):
    raise SystemExit("'id' must use lowercase letters, numbers, '.', '-' or '_'.")
if not isinstance(profile["name"], str) or not profile["name"].strip():
    raise SystemExit("'name' must be a non-empty name people will see.")
if not isinstance(profile["icon"], str) or not profile["icon"].strip():
    raise SystemExit("'icon' must be an SF Symbol name, such as 'keyboard'.")
if not isinstance(profile["config"], dict):
    raise SystemExit("'config' must be an object: { \"keyHeight\": 52 }.")
print(f"Looks good: {profile['name']} ({profile['id']})")
