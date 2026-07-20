# my-watch — Huawei Band 9 Watch Face

A watch face for the **Huawei Band 9** (1.47" AMOLED, **194 × 368 px**), designed
to be sideloaded via **Gadgetbridge**.

## How this project is structured (and why)

The Huawei Band watch-face format is **bitmap-only**: the firmware has no font
engine and no color attributes — every digit and label is a pre-rendered image,
and colors are baked into those images. The installable package is a `.hwt` ZIP
containing a **compiled binary blob** (`com.huawei.watchface`).

**There is no open-source tool that compiles that blob** — only Huawei's closed
**Theme Studio** (or a closed GUI packer) can produce it. Gadgetbridge is purely
an *installer*: it validates and uploads a finished `.hwt`, it does not build one.

So this repo is the **design source of truth** for everything upstream of that
compile step, and Theme Studio does the final compile:

```
my-watch/
├── src/
│   ├── colors.xml            # Palette — source colors for rendering (single source of truth)
│   └── description.xml       # HwTheme package descriptor (what Gadgetbridge validates)
├── assets/
│   ├── fonts/                # Chakra Petch TTFs — design source, rasterized (NOT packaged)
│   ├── backgrounds/          # Hand-made background art (if any)
│   └── icons/                # Hand-made complication icons
├── tools/
│   └── render_assets.py      # Renders glyph bitmaps from fonts + palette → build/rendered/
├── docs/
│   └── layout-spec.md        # Widget layout to reproduce in Theme Studio
├── build/                    # Generated bitmaps (git-ignored, reproducible)
└── preview/                  # cover.jpg (git-ignored, generated)
```

## Workflow

```
  colors.xml + fonts ─▶ render_assets.py ─▶ build/rendered/*.png ─┐
                                                                  ├─▶ Theme Studio ─▶ my-watch.hwt ─▶ Gadgetbridge ─▶ Band 9
  docs/layout-spec.md  (place widgets by hand in Theme Studio) ───┘
  src/description.xml  (metadata / screen size, reconcile in Theme Studio)
```

1. **Render assets** — `python3 tools/render_assets.py` (needs Pillow). Writes
   glyph bitmaps to `build/rendered/` and a preview to `preview/cover.jpg`.
2. **Compile in Theme Studio** — import `build/rendered/` + `assets/` art, place
   widgets following [docs/layout-spec.md](docs/layout-spec.md), set metadata to
   match [src/description.xml](src/description.xml), export the `.hwt`.
3. **Install** — open the `.hwt` on your phone, choose Gadgetbridge's
   "FW/App installer", tap Install.

## Design system

- **Colors** — [src/colors.xml](src/colors.xml). `background` is absolute black
  (AMOLED pixels off). See the table below.
- **Typeface** — **Chakra Petch** (SIL OFL), geometric/rectangular with open
  6/8/9. Rasterized into glyph bitmaps; see [fonts README](assets/fonts/README.md).

| Token           | Hex       | Use                                            |
|-----------------|-----------|------------------------------------------------|
| `background`    | `#000000` | Absolute black canvas (AMOLED pixels off)      |
| `danger_red`    | `#FF2116` | Alerts / heart rate — dashboard-telltale red   |
| `primary`       | `#FFDA33` | Hero elements (the clock)                      |
| `alternate`     | `#00FFD4` | Secondary accent                               |
| `standard`      | `#AB7C5F` | Regular data / labels (muted tan)              |
| `standard_dark` | `#1B130E` | Subtle fills / low emphasis                    |

## ⚠️ Reality checks before you invest heavily

These are verified from Gadgetbridge's source and Huawei's Band widget reference:

- **Band 9 support in Gadgetbridge is experimental** (added May 2024, "coordinator
  support only"). Watch-face upload on Band 9 is **unproven**, and **HarmonyOS
  6.1+ firmware cannot install faces via Gadgetbridge at all**. Before building a
  full face, confirm your Band 9 can install *any* custom face.
- **The exact internal layout dialect for Band 9 is unverified.** `data_type`
  names in the layout spec come from the older Band widget reference. The
  reliable check: extract an existing Band 9 face and read its config.
- **`description.xml` `<screen>` must match the device** or Gadgetbridge rejects
  the file. Band 9 194×368 → code `HWHD07` / `368*194`.
