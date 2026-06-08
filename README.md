# RGB565 Color Viewer

Convert 16-bit **RGB565** color values (as used by displays driven with
[TFT_eSPI](https://github.com/Bodmer/TFT_eSPI) and similar libraries) to
**RGB888**, and preview them right in your terminal.

Each value is printed as:

- a hex string (`#RRGGBB`),
- a decimal `rgb(r, g, b)` triple, and
- a solid color swatch rendered with ANSI 24-bit (truecolor) escape sequences.

## Requirements

- Python 3.9 or newer (no third-party dependencies)
- A terminal that supports 24-bit (truecolor) ANSI escape sequences for the
  color swatch (most modern terminals do)

## Usage

```bash
# Interactive prompt
python rgb565_color.py

# One-shot
python rgb565_color.py 0x9C3D

# Several values at once
python rgb565_color.py 0x9C3D F800 31
```

### Accepted value formats

| Format  | Example  | Notes                                      |
|---------|----------|--------------------------------------------|
| Hex     | `0x9C3D` | Explicit `0x` prefix                       |
| Hex     | `9C3D`   | Bare hex (detected by the presence of A-F) |
| Decimal | `39997`  | Plain decimal                              |

Exit interactive mode with a blank line, `q`, `Ctrl-D`, or `Ctrl-C`.

## Example

```text
$ python rgb565_color.py 0xF800

Input   : 0xF800  (RGB565)
RGB888  : #FF0000   rgb(255, 0, 0)
[red swatch]
```

## How it works

RGB565 packs a color into 16 bits — 5 bits red, 6 bits green, 5 bits blue.
Each channel is extracted and scaled up to the full 0-255 range using rounding
division, so a maximum channel value maps exactly to 255.

## Exit codes

| Code | Meaning                                  |
|------|------------------------------------------|
| `0`  | Success                                  |
| `1`  | One or more values could not be parsed   |

## Author

Anuraag
