# Clink typing profiles

Profiles tuned for fewer fat-finger punctuation misses.

## Import

Publish only after approval. The workflow creates an immutable `profiles-<sha256>` release and marks it as GitHub's latest release; it does not use or replace a moving `latest` tag. Add `OWNER/REPO` using Clink's community repository controls and install the profile from its profile catalogue. See the setup guide and https://www.anti.ltd/docs/clink/packs for current app navigation.

## Recommended fresh setup: Rares Quiet Bilingual

Apply Clink Default, then `Rares Quiet Bilingual`. This profile explicitly turns
sound off, inherits normal Default key height/spacing, adds a compact number
row, uses calm direct motion and floating popups, and prepares gentle native
feedback. Finish the deliberate theme/language/gesture/AI choices in
[SETUP-rares-quiet-bilingual.md](SETUP-rares-quiet-bilingual.md), including the
separate opt-in custom plugins. Mixed-safe mode preserves typed words and uses
manual correction suggestions; it is not a promise of flawless automatic repair.

## Retained legacy profiles (not recommended for this setup)

- **Anti-Period**: bigger keys, more spacing, calmer press feedback.
- **Anti-Period Fast**: same direction, but keeps the fast typing feel.
- **Thumb Room**: maximum space/height profile for larger thumbs.

These can reduce accidental nearby taps, but profiles cannot directly remove or move the period key unless Clink exposes a config key for that.

## Local release checks (no publishing)

```sh
python3 -B -m unittest discover -s tests -v
python3 tools/build-manifest.py --output "$TMPDIR/clink-profile-manifest.json"
python3 tools/build-manifest.py --output "$TMPDIR/clink-profile-manifest.json" --check
```

The builder defaults to `dobrerares/clink-typing-profiles` locally and uses
`GITHUB_REPOSITORY` in Actions; `--repository OWNER/REPO` overrides either.
The release version matches upstream: SHA-256 of compact JSON containing sorted
`[filename, file-SHA-256]` pairs. Names, membership, or any byte changes produce a
new permanent release URL. Hidden files are excluded from both hashing and the
manifest. Validation runs before the output is written, checks unique internal
IDs and the profile size limit, and retains upstream's filename-based catalog IDs.

The local `manifest.json` has been explicitly regenerated and `--check` passes.
Its new immutable release URLs are not live until an approved publication.
CI builds a fresh manifest in its checkout, uploads all assets in a draft, and publishes only after upload
succeeds. Retries may replace draft assets, never published assets. Existing
releases, including any old `latest` tag, are not deleted. Workflow changes take
effect only after an approved push to `main` (or an approved manual dispatch).

The offline workflow tests run the publishing shell against a fake `gh`; they
never contact GitHub. They do not verify real GitHub permissions or Clink import.
The validator checks basic structure, not supported config keys or actual SF
Symbol availability. Existing `custom.*` internal IDs differ from catalog
filename IDs; both are preserved pending an explicit compatibility decision.
