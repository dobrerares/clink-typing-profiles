# Rares Glass: Clink setup

One profile, four plugins, and an official Liquid Glass theme. It's for mixed Romanian/English typing, with fewer accidental periods, no tall keys and no sound.

## What you install

| Piece | Where | What it does |
|---|---|---|
| **Rares Glass** profile | `dobrerares/clink-typing-profiles` | Default key height and spacing. Compact number row, sound OFF, gentle haptics, floating popups, short glassy motion, spacebar cursor. Native auto-punctuation off. |
| **Liquid Violet** theme | Official Clink theme catalogue | Liquid Glass keys (translucent `liquidGlass` material) with a calm violet accent. Installed from the official catalogue, not republished. |
| **Bilingual Guard** plugin | `dobrerares/clink-typing-plugins` | Keeps each word as you typed it, so English is never "fixed" into Romanian or the reverse. Fixes appear as suggestions only. |
| **Quiet Feedback** plugin | same | Per-key haptics: gentle letters, firmer space, crisp return, light delete. |
| **Period Guard** plugin | same | Shrinks the period key's tap area after a one-time calibration, without changing how it looks. |
| **Explicit Proofread** plugin | same | A top-bar button that sends only the text you selected to Apple Intelligence. |

All four plugins install switched off. You turn on each one yourself.

## Setup on the phone (needs Clink Pro)

1. **Profile:** add `dobrerares/clink-typing-profiles` under Clink's repositories. Apply **Clink Default**, then **Rares Glass**. Check that sound is OFF and keys are normal height.
2. **Theme:** Themes → official catalogue → **Liquid Violet**. Appearance: Automatic.
3. **Languages:** enable **Romanian** and **English (UK)**, both QWERTY. Turn on **Combined Language Mode** and wait for both downloads to finish.
4. **Corrections:** native Autocorrect **OFF**, suggestions **ON**, auto-punctuation **OFF**, double-space period **OFF**, auto-capitalize and smart quotes **OFF**. Bilingual Guard handles corrections instead.
5. **Gestures:** swipe typing **OFF** for now. Cursor on spacebar drag. Floating popups with long-press accents on, for ă â î ș ț.
6. **Plugins:** add `dobrerares/clink-typing-plugins` and install all four. Turn on **Bilingual Guard** and **Quiet Feedback** first. From the official plugins, add **Language Flag** to show the active layout. Leave Adaptive Hitbox, Heavy Space, Shorthand and other correction or haptic plugins **off**, because they compete with ours.
7. **Period Guard:** turn it on. In a throwaway note, arm calibration, tap the period twice, and confirm. It starts at scale 0.92 with spacebar expansion off. If it says "unsupported", leave it off and tell Daedalus.
8. **Apple Intelligence:** Integrations → Apple Intelligence. Turn on **Explicit Proofread**, then add **Proofread selection** to the top bar. Select **English-only** text, then tap the button. Apple doesn't list Romanian as supported, so mixed text may be mangled.
9. **Permissions:** per-key haptics and AI may need Full Access. Plugins ask for Typing data. Read each prompt before allowing it.
10. **Save:** once it all works, export a backup of this setup. Clink Default stays available to roll back to.

## Quick test (in a throwaway note)

- No sound on any key. Haptics feel different on space, return and delete.
- Type: `Am făcut push pe branch, but tests încă fail.` and `Sorry, sunt late; ajung în 10 minutes.` No word should get replaced automatically.
- Also try: `s-a`, `mi-am`, `într-un`, `https://example.com`, `a@b.ro`, `3.14`.
- Compare accidental periods before and after calibrating Period Guard. A period you tap on purpose must still work.
- Proofread with nothing selected should do nothing.

## Limits

- Bilingual Guard trades automatic typo fixing for never mis-correcting language. You get suggestions, not silent fixes.
- These plugins are a v0.1 phone-test release. They're tested on a computer, not yet on the phone.
- No custom language pack or model is included yet.
