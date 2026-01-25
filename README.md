# Baseline Diagnostic Font

## Overview

Font that can be used for validating baseline alignments. This project contains
the build system for the font using the [fonttools] Python library.

**Built font files can be found in the [./dist](./dist) folder.** An overview
of the font and demos can be found on https://sajidanwar.com/misc/baseline-diagnostic-font/.

## Building

This project uses [uv] for dependency management. Use `uv run main.py` to build
the font files into the `dist` folder.

## License

This project's source code is licensed under the [MIT license][mit-license], and
is available at `LICENSE.md`.

The built font contains [Noto Sans Mono][noto-sans-mono] glyphs in the rendering
of its baseline labels. Like that font, this font is licensed under the
[SIL Open Font License, Version 1.1][ofl-license], and is available at `dist/LICENSE.md`.

[uv]: https://docs.astral.sh/uv/#highlights
[fonttools]: https://fonttools.readthedocs.io/en/latest/
[mit-license]: https://opensource.org/license/mit
[noto-sans-mono]: https://fonts.google.com/noto/specimen/Noto+Sans+Mono/license
[ofl-license]: https://openfontlicense.org/open-font-license-official-text/
