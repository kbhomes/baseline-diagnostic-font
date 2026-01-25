# Baseline Diagnostic Font

## Overview

Font that can be used for validating baseline alignments. This project contains
the build system for the font using the [fonttools] Python library.

**Built font files can be found in the [./dist](./dist) folder.**

## Building

This project uses [uv] for dependency management. Use `uv run` to build the font
files into the `dist` folder.

## License

This font contains [Noto Sans Mono][noto-sans-mono] glyphs in the rendering
of its baseline labels. Like that font, this font is licensed under the
[SIL Open Font License, Version 1.1][ofl-1.1], and is available at `LICENSE.txt`.

[uv]: https://docs.astral.sh/uv/#highlights
[fonttools]: https://fonttools.readthedocs.io/en/latest/