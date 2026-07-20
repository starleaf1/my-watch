# Fonts

Project typeface: **Chakra Petch** — geometric, rectangular, with open 6/8/9
apertures for legibility at small sizes. Used throughout the watch face.

## Bundled files

| File                     | Weight  | Used for                          |
|--------------------------|---------|-----------------------------------|
| `ChakraPetch-Regular.ttf`| Regular | Complication values / labels      |
| `ChakraPetch-Bold.ttf`   | Bold    | Date, and source for clock digits |

The digital clock digits (`assets/digits/0.png`–`9.png`, `colon.png`) should be
rendered from **Chakra Petch Bold** so the bitmap clock matches the text.

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

Then reference it as `font="fonts/ChakraPetch-SemiBold"` in `src/watchface.xml`.
