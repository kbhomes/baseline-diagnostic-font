
# Baseline Diagnostic Font

## Overview

Font that can be used for validating baseline alignments. Given the embedded
text in the font, this should be used with very large font sizes. There are
two glyphs in the font:

  - `X` (U+0058) which has all baselines drawn
  - `.notdef` (for all other characters) which is an empty box

It has the following baselines:

| Baseline/Metric   | Coordinate | BASE Value | OS/2 Value     | hhea Value |
|-------------------|------------|------------|----------------|------------|
| ascent            |        800 |            | sTypoAscender  | ascent     |
| ideographic-over  |        750 | idtp       |                |            |
| hanging           |        650 | hang       |                |            |
| cap-height        |        550 |            | sCapHeight     |            |
| math              |        450 | math       |                |            |
| /central/         |        350 |            |                |            |
| /em-middle/       |        300 |            |                |            |
| x-height          |        250 |            | sxHeight       |            |
| /x-middle/        |        150 |            |                |            |
| alphabetic        |         50 | romn       |                |            |
| /zero/            |            |            |                |            |
| ideographic-under |        -50 | ideo       |                |            |
| descent           |       -200 |            | sTypoDescender | descent    |

The `BaselineDiagnosticAlphabeticZero` variant is the same as `Baseline`,
except the alphabetic baseline is at the common value of 0. This also
results in the x-middle baseline being at 125.

## License

This font contains [Noto Sans Mono][noto-sans-mono] glyphs in the rendering
of its baseline labels. Like that font, this font is licensed under the
[SIL Open Font License, Version 1.1][ofl-1.1], and is available at `LICENSE.txt`.

[noto-sans-mono]: https://fonts.google.com/noto/specimen/Noto+Sans+Mono/license
[ofl-1.1]: https://openfontlicense.org/open-font-license-official-text/
