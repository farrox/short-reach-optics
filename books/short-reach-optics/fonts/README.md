# Fonts (SIL Open Font License)

The template defaults to **Alegreya Sans** (Juan Pablo del Peral). TTFs are
vendored in this directory; `OFL.txt` carries the license text.

## Active font (Alegreya Sans)

| File | Used as |
|------|---------|
| `AlegreyaSans-Regular.ttf` | `\setmainfont` upright (body) |
| `AlegreyaSans-Italic.ttf` | italic |
| `AlegreyaSans-Bold.ttf` | bold |
| `AlegreyaSans-BoldItalic.ttf` | bold italic |
| `AlegreyaSans-Light.ttf` / `LightItalic.ttf` | `\AlegreyaLight` |
| `AlegreyaSans-Medium.ttf` / `MediumItalic.ttf` | medium weight |
| `AlegreyaSans-Black.ttf` / `BlackItalic.ttf` | display titles |

To switch the body to **EB Garamond** (serif), change the `\setmainfont` block
in `preamble.tex` to use the `EBGaramond-*.ttf` files also present here.
