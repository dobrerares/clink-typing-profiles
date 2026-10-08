# Clink typing profiles (Rares)

One profile: **Rares Glass**. It keeps Clink Default key height and spacing, adds a compact number row, turns sound OFF, and uses gentle haptics, floating popups and short glassy motion. Pair it with the official **Liquid Violet** Liquid Glass theme and the plugins in [`dobrerares/clink-typing-plugins`](https://github.com/dobrerares/clink-typing-plugins).

Full setup: [SETUP-rares-glass.md](SETUP-rares-glass.md).

## Install

In Clink, add `dobrerares/clink-typing-profiles` under repositories. Then go to Customize → Profiles → Profile packs → **Rares Glass**.

## Publishing

Each change publishes a permanent, content-hashed `profiles-<sha256>` release, the same scheme as the official `anti-ltd/clink-profiles`. There's no moving `latest` tag. CI uploads everything to a draft release and only publishes it once every upload has succeeded.

```sh
python3 -B -m unittest discover -s tests -v
python3 tools/build-manifest.py --output "$TMPDIR/m.json" --check
```

Older profiles (Anti-Period, Thumb Room and others) were removed; they remain in git history.
