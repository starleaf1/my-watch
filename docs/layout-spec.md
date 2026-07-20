# Layout spec — my-watch (Huawei Band 9)

Panel: **194 × 368 px**, origin top-left, x → right, y → down.

This is the design spec to **reproduce in Huawei Theme Studio**. Theme Studio is
a GUI: you place widgets on a canvas and it writes the internal
`watch_face_config.xml` and compiles the `com.huawei.watchface` binary for you.
This file records *what* to place and *where*, so the layout is repeatable.

## How the Band format works (why this looks the way it does)

The Band firmware has **no font engine and no vector drawing** — it only blits
bitmaps. So:

- Every digit is a **DIGITALIMAGE** widget pointing at a folder of glyph images
  (`0.png`–`9.png`); the firmware picks which image to show from a `data_type`
  (e.g. `DATA_HOUR_HIGH`). We render those glyphs from Chakra Petch — see
  `tools/render_assets.py` → `build/rendered/`.
- Colors are **baked into the bitmaps** (there is no color attribute), so a
  widget's color = the color we rendered its glyphs in.
- Static art (background, icons) is a **SINGLEIMAGE** widget.

## Widgets to place

| # | Element        | Widget type   | `data_type`(s)                          | Asset folder / file            | Color (rendered) | Position (x,y) |
|---|----------------|---------------|-----------------------------------------|--------------------------------|------------------|----------------|
| 1 | Background     | SINGLEIMAGE   | `DATA_BACKGROUND`                       | *(solid black — see note)*     | `background`     | 0, 0           |
| 2 | Hour tens      | DIGITALIMAGE  | `DATA_HOUR_HIGH`                         | `build/rendered/clock/`        | `primary`        | ~20, 140       |
| 3 | Hour ones      | DIGITALIMAGE  | `DATA_HOUR_LOW`                          | `build/rendered/clock/`        | `primary`        | ~60, 140       |
| 4 | Colon          | SINGLEIMAGE   | —                                       | `build/rendered/clock/colon`   | `primary`        | ~97, 140       |
| 5 | Minute tens    | DIGITALIMAGE  | `DATA_MINITE_HIGH` *(sic — Huawei spelling)* | `build/rendered/clock/`   | `primary`        | ~120, 140      |
| 6 | Minute ones    | DIGITALIMAGE  | `DATA_MINITE_LOW`                       | `build/rendered/clock/`        | `primary`        | ~160, 140      |
| 7 | Date           | DIGITALIMAGE  | `DATA_DATE`, `DATA_MONTH`               | `build/rendered/data/`         | `standard`       | ~97, 235       |
| 8 | Steps          | DIGITALIMAGE  | `DATA_STEPS`                            | `build/rendered/data/`         | `standard`       | ~50, 300       |
| 9 | Heart rate     | DIGITALIMAGE  | `DATA_HEARTRATE`                        | `build/rendered/data_hr/`      | `danger_red`     | ~144, 300      |
| 10| Battery        | DIGITALIMAGE  | `DATA_BATTERY` / `DATA_BATTERYNUM`      | `build/rendered/data/`         | `standard`       | ~97, 340       |

Positions are a starting layout — fine-tune on the Theme Studio canvas. The
colors above are produced by the render script; to recolor an element, render a
new glyph set in a different palette token and point the widget at it.

## Notes / open items to verify on-device

- **Background:** on AMOLED, absolute black = pixels off. Prefer a black
  `DATA_BACKGROUND` (or no background image) over shipping a black PNG.
- **`data_type` names** come from the older *Band Widget Reference*; the exact
  enum on Band 9 firmware is unverified. Confirm against an extracted Band 9
  face (use a community extractor to unzip one and read its config).
- **Fixed digit counts:** the Band format supports leading-zero padding via a
  digit-count attribute — set hour/minute to 2 digits in Theme Studio.
- **`filter_color`** is a chroma-key (transparency), not a fill; leave at 0
  since our glyphs already ship with transparent backgrounds.
