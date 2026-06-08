#!/usr/bin/env python3
"""RGB565 color viewer.

Convert 16-bit RGB565 color values (as used by displays driven with
TFT_eSPI and similar libraries) to RGB888 and preview them in the terminal.

The converted value is printed as hex (``#RRGGBB``), as a decimal
``rgb(r, g, b)`` triple, and as a solid color swatch rendered with ANSI
24-bit (truecolor) escape sequences.

Usage:
    python rgb565_color.py                 # interactive prompt
    python rgb565_color.py 0x9C3D          # one-shot
    python rgb565_color.py 0x9C3D F800 31  # several values at once

Accepted value formats:
    0x9C3D   explicit hex
    9C3D     bare hex (detected by the presence of A-F digits)
    39997    decimal

Exit interactive mode with a blank line, ``q``, Ctrl-D, or Ctrl-C.

Author: Anuraag
Date:   2026-06-08
"""

from __future__ import annotations

__author__ = "Anuraag"

import argparse
import sys

# ANSI escape sequences for rendering a truecolor swatch in the terminal.
_ANSI_RESET = "\033[0m"
_ANSI_BG_TRUECOLOR = "\033[48;2;{r};{g};{b}m"


def rgb565_to_rgb888(value: int) -> tuple[int, int, int]:
    """Convert a 16-bit RGB565 value to an 8-bit ``(r, g, b)`` tuple.

    The 5- and 6-bit channels are scaled to the full 0-255 range using
    rounding division so that, for example, a maximum channel value maps
    exactly to 255.

    Args:
        value: A 16-bit RGB565 color. Bits above bit 15 are ignored.

    Returns:
        A ``(red, green, blue)`` tuple, each component in the range 0-255.
    """
    value &= 0xFFFF
    r5 = (value >> 11) & 0x1F  # 5 bits red
    g6 = (value >> 5) & 0x3F   # 6 bits green
    b5 = value & 0x1F          # 5 bits blue

    r8 = (r5 * 255 + 15) // 31
    g8 = (g6 * 255 + 31) // 63
    b8 = (b5 * 255 + 15) // 31
    return r8, g8, b8


def color_box(r: int, g: int, b: int, width: int = 10, height: int = 3) -> str:
    """Return a solid color box drawn with ANSI 24-bit (truecolor) escapes.

    Args:
        r: Red component (0-255).
        g: Green component (0-255).
        b: Blue component (0-255).
        width: Box width in characters.
        height: Box height in lines.

    Returns:
        A multi-line string containing the rendered box.
    """
    line = _ANSI_BG_TRUECOLOR.format(r=r, g=g, b=b) + " " * width + _ANSI_RESET
    return "\n".join(line for _ in range(height))


def format_color(value: int) -> str:
    """Return a multi-line human-readable description of an RGB565 value."""
    r, g, b = rgb565_to_rgb888(value)
    return (
        f"Input   : 0x{value:04X}  (RGB565)\n"
        f"RGB888  : #{r:02X}{g:02X}{b:02X}   rgb({r}, {g}, {b})\n"
        f"{color_box(r, g, b)}"
    )


def parse_value(token: str) -> int:
    """Parse a color token such as ``'0x9C3D'``, ``'9C3D'``, or ``'39997'``.

    A token is treated as hexadecimal if it is prefixed with ``0x`` or if it
    contains any of the hex-only digits ``A-F``. Otherwise it is parsed as
    decimal.

    Args:
        token: The raw token to parse.

    Returns:
        The parsed integer value.

    Raises:
        ValueError: If the token cannot be parsed as an integer.
    """
    token = token.strip()
    if not token:
        raise ValueError("empty token")
    is_hex = token.lower().startswith("0x") or any(
        c in "abcdefABCDEF" for c in token
    )
    return int(token, 16 if is_hex else 10)


def show(value: int) -> None:
    """Print the description of an RGB565 value with surrounding spacing."""
    print(f"\n{format_color(value)}\n")


def run_interactive() -> None:
    """Run the interactive read-eval-print loop."""
    print("RGB565 color viewer. Enter a value like 0x9C3D (blank or 'q' to quit).")
    while True:
        try:
            token = input("color> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not token or token.lower() == "q":
            break
        try:
            show(parse_value(token))
        except ValueError:
            print(f"Could not parse: {token!r}")


def main(argv: list[str] | None = None) -> int:
    """Program entry point.

    Args:
        argv: Optional argument list (defaults to ``sys.argv[1:]``).

    Returns:
        Process exit code: 0 on success, 1 if any value failed to parse.
    """
    parser = argparse.ArgumentParser(
        description="Convert RGB565 color values to RGB888 and preview them.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "values",
        nargs="*",
        metavar="VALUE",
        help="RGB565 color(s), e.g. 0x9C3D, 9C3D, or 39997. "
        "If omitted, an interactive prompt is shown.",
    )
    args = parser.parse_args(argv)

    if not args.values:
        run_interactive()
        return 0

    exit_code = 0
    for token in args.values:
        try:
            show(parse_value(token))
        except ValueError:
            print(f"Could not parse: {token!r}")
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
