# Fonts

Project typeface: **Chakra Petch** — geometric, rectangular, with open 6/8/9
apertures for legibility at small sizes.

**Important:** the Huawei Band format has no font engine — it cannot use a TTF at
runtime. These files are **design sources only**: `tools/render_assets.py`
rasterizes them into the glyph bitmaps in `build/rendered/`, which is what
actually ships in the watch face. The TTFs are not packaged into the `.hwt`.

## Files

| File                     | Weight  | Rendered into                          |
|--------------------------|---------|----------------------------------------|
| `ChakraPetch-Bold.ttf`   | Bold    | Hero clock digits (`build/rendered/clock/`) |
| `ChakraPetch-Regular.ttf`| Regular | Data digits (`build/rendered/data*/`)  |

## Source & license

- Source: Google Fonts — https://github.com/google/fonts/tree/main/ofl/chakrapetch
- License: SIL Open Font License 1.1 — see [`OFL.txt`](OFL.txt). Embedding in
  the watch-face package is permitted.

## Adding more weights

Chakra Petch also ships Light, Medium, and SemiBold (+ italics). To add one:

```bash
curl -fsSL -o "ChakraPetch-SemiBold.ttf" \
  "https://github.com/google/fonts/raw/main/ofl/chakrapetch/ChakraPetch-SemiBold.ttf"
```

Then point a `render_glyph_set(...)` call in `tools/render_assets.py` at it.
