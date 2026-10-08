"""Offline release tests: all gh calls go to a temporary fake executable."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", ROOT / "tools/build-manifest.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "Profiles").mkdir()
        self.add_profile("b", "custom.b")
        self.add_profile("a", "custom.a")

    def add_profile(self, name, identifier):
        path = self.root / "Profiles" / (name + ".clinkprofile")
        path.write_text(json.dumps({"id": identifier, "name": name,
                                    "icon": "keyboard", "config": {}}))
        return path

    def build(self):
        return builder.build_manifest(self.root, "example/profiles")

    def test_matches_upstream_contract_and_asset_bytes(self):
        paths = sorted((self.root / "Profiles").glob("*.clinkprofile"))
        pairs = [(p.name, hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]
        expected = "profiles-" + hashlib.sha256(json.dumps(pairs, separators=(",", ":")).encode()).hexdigest()
        manifest = self.build()
        self.assertEqual(manifest["version"], expected)
        self.assertEqual(manifest, self.build())
        for pack, path in zip(manifest["profiles"], paths):
            self.assertEqual(pack["id"], path.stem)
            self.assertEqual(pack["version"], expected)
            self.assertEqual(pack["asset"]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(pack["asset"]["byteCount"], len(path.read_bytes()))
            self.assertEqual(pack["asset"]["url"], f"https://github.com/example/profiles/releases/download/{expected}/{path.name}")

    def test_bytes_names_and_membership_change_version(self):
        before = self.build()["version"]
        path = self.root / "Profiles/a.clinkprofile"
        original = path.read_bytes()
        path.write_bytes(original + b"\n")
        self.assertNotEqual(before, self.build()["version"])
        path.write_bytes(original)
        path.rename(path.with_name("c.clinkprofile"))
        self.assertNotEqual(before, self.build()["version"])
        path.with_name("c.clinkprofile").unlink()
        self.assertNotEqual(before, self.build()["version"])

    def test_hidden_files_are_excluded_consistently(self):
        before = self.build()
        (self.root / "Profiles/.ignored.clinkprofile").write_text("not JSON")
        self.assertEqual(before, self.build())

    def test_invalid_duplicate_and_oversized_profiles_fail(self):
        path = self.add_profile("c", "custom.a")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.build()
        path.write_text("not JSON")
        with self.assertRaisesRegex(ValueError, "not valid JSON"):
            self.build()
        path.write_bytes(b" " * (256 * 1024))
        with self.assertRaisesRegex(ValueError, "smaller than"):
            self.build()

    def test_non_object_profile_fails_plainly(self):
        path = self.add_profile("c", "custom.c")
        path.write_text("null")
        with self.assertRaisesRegex(ValueError, "must be a JSON object"):
            self.build()

    def test_empty_and_invalid_repository_fail(self):
        for path in (self.root / "Profiles").iterdir():
            path.unlink()
        with self.assertRaisesRegex(ValueError, "no visible"):
            self.build()
        with self.assertRaisesRegex(ValueError, "OWNER/REPO"):
            builder.build_manifest(self.root, "https://bad")

    def test_cli_output_and_check_never_touch_tracked_artifact(self):
        tracked = (ROOT / "manifest.json").read_bytes()
        output = self.root / "manifest.json"
        cmd = ["python3", "-B", str(ROOT / "tools/build-manifest.py"),
               "--repository", "example/profiles", "--output", str(output)]
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(cmd + ["--check"], capture_output=True).returncode, 0)
        output.write_text("{}\n")
        self.assertNotEqual(subprocess.run(cmd + ["--check"], capture_output=True).returncode, 0)
        self.assertEqual(output.read_text(), "{}\n")
        self.assertEqual((ROOT / "manifest.json").read_bytes(), tracked)


class WorkflowTests(unittest.TestCase):
    def run_release(self, mode, fail=""):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Profiles").mkdir()
            (root / "Profiles/a.clinkprofile").write_text("{}")
            (root / "manifest.json").write_text(json.dumps({"version": "profiles-" + "a" * 64}))
            fake = root / "gh"
            fake.write_text('''#!/usr/bin/env python3
import json, os, sys
with open(os.environ["LOG"], "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
action = sys.argv[2]
if action == os.environ.get("FAIL"):
    sys.exit(1)
if action == "view":
    mode = os.environ["MODE"]
    if mode == "missing":
        sys.exit(1)
    print(mode)
''')
            fake.chmod(0o755)
            workflow = (ROOT / ".github/workflows/release.yml").read_text()
            script = "\n".join(line[10:] for line in workflow.split("        run: |\n", 1)[1].splitlines())
            subprocess.run(["bash", "-n"], input=script, text=True, check=True)
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ["PATH"],
                       LOG=str(root / "calls"), MODE=mode, FAIL=fail, GITHUB_SHA="test-sha")
            result = subprocess.run(["bash", "-c", script], cwd=root, env=env, capture_output=True, text=True)
            calls = [json.loads(line) for line in (root / "calls").read_text().splitlines()]
            self.assertFalse(any("delete" in call for call in calls))
            self.assertTrue(all(call[2] == "profiles-" + "a" * 64 for call in calls))
            return result, calls

    def test_new_release_is_hidden_until_complete(self):
        result, calls = self.run_release("missing")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([c[1] for c in calls], ["view", "create", "edit"])
        self.assertIn("--draft", calls[1])
        self.assertIn("manifest.json", calls[1])
        self.assertIn("--draft=false", calls[2])

    def test_draft_can_resume(self):
        result, calls = self.run_release("true")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([c[1] for c in calls], ["view", "upload", "edit"])
        self.assertIn("--clobber", calls[1])

    def test_published_release_assets_are_never_modified(self):
        result, calls = self.run_release("false")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([c[1] for c in calls], ["view", "edit"])
        self.assertEqual(calls[1][3:], ["--latest"])

    def test_failed_upload_or_create_cannot_publish(self):
        for mode, action in [("true", "upload"), ("missing", "create")]:
            result, calls = self.run_release(mode, action)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual([c[1] for c in calls], ["view", action])

    def test_unknown_draft_state_fails_closed(self):
        result, calls = self.run_release("unknown")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([c[1] for c in calls], ["view"])


if __name__ == "__main__":
    unittest.main()
