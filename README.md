# my-watch — Huawei Band 9 Watch Face

A watch face project for the **Huawei Band 9** (1.47" AMOLED, **194 × 368 px**, rectangular).

## Project structure

```
my-watch/
├── src/
│   ├── manifest.xml      # Metadata + device/screen info (→ Com.Huawei.watchface)
│   └── watchface.xml     # Layout: background, clock, date, complications
├── assets/
│   ├── backgrounds/      # Full-screen background(s), 194×368
│   ├── digits/           # Bitmap digits 0.png–9.png, colon.png (digital clock)
│   ├── hands/            # hour.png / minute.png / second.png (analog clock)
│   ├── icons/            # Complication icons (steps, heart, battery, …)
│   └── fonts/            # Bitmap/embedded fonts
├── preview/
│   └── preview.png       # Thumbnail shown in the watch-face picker
├── tools/
│   └── build.sh          # Assembles + zips the package into dist/
└── dist/                 # Build output (git-ignored)
```

## Color scheme

Canonical values live in [`src/colors.xml`](src/colors.xml). Refer to colors by
token name; the hex is inlined in `watchface.xml` with a matching comment.

| Token           | Hex       | Use                                            |
|-----------------|-----------|------------------------------------------------|
| `background`    | `#000000` | Absolute black canvas (AMOLED pixels off)      |
| `danger_red`    | `#FF2116` | Alerts / critical states — dashboard-telltale red |
| `primary`       | `#FFDA33` | Primary accent (amber-yellow)                  |
| `alternate`     | `#00FFD4` | Secondary accent (cyan/teal)                   |
| `standard`      | `#AB7C5F` | Regular text / labels (muted tan)              |
| `standard_dark` | `#1B130E` | Subtle fills / low emphasis (warm near-black)  |

## Typography

Project typeface: **Chakra Petch** (SIL OFL) — geometric and rectangular with
open 6/8/9 apertures that stay distinct at small sizes. Bundled in
[`assets/fonts/`](assets/fonts/) as Regular + Bold; see the
[fonts README](assets/fonts/README.md) for usage and adding weights.

- **Bold** — date, and the source for the clock digit bitmaps
- **Regular** — complication values and labels

## Building

```bash
./tools/build.sh
```

This stages the descriptors + assets into `dist/watchface/`, names the manifest
`Com.Huawei.watchface`, and produces `dist/my-watch.zip`.

## Installing on the device

Huawei does not offer a fully open, documented sideload path for band watch
faces. Typical routes:

1. **HUAWEI Watch Face Designer / Theme tooling** — import these assets, or use
   this repo as the source of truth and rebuild there.
2. **Huawei Health app** — official watch faces are pushed through the app's
   watch-face store.
3. **Sideloading** — the packaged archive usually must be renamed to Huawei's
   watch-face extension and **signed** before the device accepts it.

## ⚠️ Format caveat — verify before relying on this

The Huawei watch-face package format is **not fully publicly documented** and
varies by device and firmware. The XML tag/attribute names in `src/*.xml` follow
the **community-documented** Huawei format and are provided as a *starting
template*. Before investing heavily:

- Compare against a **known-good Band 9 watch face** (unzip an existing one), or
- Use the **HUAWEI Watch Face Designer** output as the schema reference,

and adjust `src/manifest.xml` / `src/watchface.xml` element names accordingly.
The directory layout, asset organization, and build script are sound regardless;
only the XML schema specifics need confirming.

## Asset specs (Band 9)

| Asset        | Size / notes                                  |
|--------------|-----------------------------------------------|
| Background   | 194 × 368 px PNG                              |
| Digits       | Consistent glyph box; transparent background  |
| Hands        | Pre-rotated at 12 o'clock; note pivot in XML  |
| Icons        | ~24–32 px, transparent PNG                    |
| Preview      | 194 × 368 px (or picker thumbnail size)       |

Keep the display **mostly dark** — AMOLED always-on style saves battery and
avoids burn-in.
