import re
from font import Font, FontBaseline, FontBaselineStyle, build_baselines_font
from textwrap import dedent, indent
from typing import Dict, List

def main():
    fonts = []
    fonts.append(Font(
        name="BaselineDiagnostic",
        description=(dedent("""\
            Font that can be used for validating baseline alignments. Given the embedded
            text in the font, this should be used with very large font sizes. There are
            two glyphs in the font.""")),
        baselines=[
            FontBaseline("ascent",               800,   "OS/2", "sTypoAscender",  None,                 None),
            FontBaseline("ascent",               800,   "hhea", "ascent",         None,                 None),
            FontBaseline("ideographic-over",     750,   "BASE", "idtp",           "IDEOGRAPHIC-OVER",   FontBaselineStyle.SOLID),
            FontBaseline("hanging",              650,   "BASE", "hang",           "HANGING",            FontBaselineStyle.SOLID),
            FontBaseline("cap-height",           550,   "OS/2", "sCapHeight",     "CAP-HEIGHT",         FontBaselineStyle.SOLID),
            FontBaseline("math",                 450,   "BASE", "math",           "MATH",               FontBaselineStyle.SOLID),
            FontBaseline("central",              350,   None,   None,             "CENTRAL",            FontBaselineStyle.SOLID),
            FontBaseline("em-middle",            300,   None,   None,             None,                 FontBaselineStyle.DASHED),
            FontBaseline("x-height",             250,   "OS/2", "sxHeight",       "X-HEIGHT",           FontBaselineStyle.SOLID),
            FontBaseline("x-middle",             150,   None,   None,             "X-MIDDLE",           FontBaselineStyle.SOLID),
            FontBaseline("alphabetic",            50,   "BASE", "romn",           "ALPHABETIC",         FontBaselineStyle.SOLID),
            FontBaseline("zero",                   0,   None,   None,             None,                 FontBaselineStyle.DASHED),
            FontBaseline("ideographic-under",    -50,   "BASE", "ideo",           "IDEOGRAPHIC-UNDER",  FontBaselineStyle.SOLID),
            FontBaseline("descent",             -200,   "OS/2", "sTypoDescender", None,                 None),
            FontBaseline("descent",             -200,   "hhea", "descent",        None,                 None),
        ]
    ))
    fonts.append(Font(
        name="BaselineDiagnosticAlphabeticZero",
        description=(dedent("""\
            Same as the "BaselineDiagnostic" font, but uses the common alphabetic baseline
            of 0. This also results in the x-middle baseline being at 125.""")),
        baselines=[
            FontBaseline("ascent",               800,   "OS/2", "sTypoAscender",  None,                 None),
            FontBaseline("ascent",               800,   "hhea", "ascent",         None,                 None),
            FontBaseline("ideographic-over",     750,   "BASE", "idtp",           "IDEOGRAPHIC-OVER",   FontBaselineStyle.SOLID),
            FontBaseline("hanging",              650,   "BASE", "hang",           "HANGING",            FontBaselineStyle.SOLID),
            FontBaseline("cap-height",           550,   "OS/2", "sCapHeight",     "CAP-HEIGHT",         FontBaselineStyle.SOLID),
            FontBaseline("math",                 450,   "BASE", "math",           "MATH",               FontBaselineStyle.SOLID),
            FontBaseline("central",              350,   None,   None,             "CENTRAL",            FontBaselineStyle.SOLID),
            FontBaseline("em-middle",            300,   None,   None,             None,                 FontBaselineStyle.DASHED),
            FontBaseline("x-height",             250,   "OS/2", "sxHeight",       "X-HEIGHT",           FontBaselineStyle.SOLID),
            FontBaseline("x-middle",             125,   None,   None,             "X-MIDDLE",           FontBaselineStyle.SOLID),
            FontBaseline("alphabetic",             0,   "BASE", "romn",           None,                 FontBaselineStyle.DASHED),
            FontBaseline("zero",                   0,   None,   None,             None,                 None),
            FontBaseline("ideographic-under",    -50,   "BASE", "ideo",           "IDEOGRAPHIC-UNDER",  FontBaselineStyle.SOLID),
            FontBaseline("descent",             -200,   "OS/2", "sTypoDescender", None,                 None),
            FontBaseline("descent",             -200,   "hhea", "descent",        None,                 None),
        ]
    ))

    write_font_files(fonts)
    write_font_stylesheet(fonts)
    write_font_readme()
    write_font_license()


def write_font_files(fonts: List[Font]):
    for font in fonts:
        build_baselines_font(font.name, f'dist/{font.name}.ttf', font.baselines)


def write_font_stylesheet(fonts: List[Font]):
    out_path = "dist/baseline-diagnostic-font.css"
    with open(out_path, "w") as f:
        for font in fonts:
            template = dedent('''
                @font-face {{
                  /**
                {description}
                   */
                  font-family: "{name}";
                  src: url('./{name}.ttf') format('opentype');
                }}

                :root {{
                  /**
                   * Variables representing the positions of the given baselines/metrics from the top
                   * of the em-box as a percentage of the em-height. The top of the em-box (ascent) has
                   * a position of 0, and the bottom of the em-box (descent) has a position of 1.
                   */
                {variables}
                }}
            ''')
            description = indent(font.description, '   * ')
            positions: Dict[str, int] = {}
            ascent = None
            descent = None

            for baseline in font.baselines:
                if baseline.id in positions and positions[baseline.id] != baseline.position:
                    raise ValueError(f"Baseline metric {baseline.id} has different position values")
                if baseline.id == 'ascent':
                    ascent = baseline.position
                if baseline.id == 'descent':
                    descent = -1 * baseline.position
                positions[baseline.id] = baseline.position

            if not ascent or not descent:
                raise ValueError(f"Required ascent / descent but got {ascent} / {descent}")

            variables = []
            for baseline, position in positions.items():
                variables.append(
                    "--{font_name}-{baseline}: calc(1 - ({position} + {descent}) / {height});".format(
                        font_name=dashing(font.name),
                        baseline=baseline,
                        position=position,
                        descent=descent,
                        height=(ascent + descent),
                    )
                )

            f.write(template.format(
                name=font.name,
                description=description,
                variables=indent('\n'.join(variables), '  '),
            ))
        print(f"Wrote stylesheet at {out_path}")


# TODO: Generate this README and tables programmatically from the fonts.
def write_font_readme():
    out_path = "dist/README.md"
    with open(out_path, "w") as f:
        f.write(dedent(r'''
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

            ## Source and Downloads
            Both the source code and built font files can be found in the [`@sajidanwar.com/baseline-diagnostic-font`][tangled-repo]
            repository on [Tangled][tangled-home] or the [`kbhomes/baseline-diagnostic-font`][github-repo]
            repository on [GitHub][github-home].

            This font is built using Python with the [fonttools](https://fonttools.readthedocs.io/en/latest/) library.

            [tangled-repo]: https://tangled.org/sajidanwar.com/baseline-diagnostic-font
            [tangled-home]: https://tangled.org/
            [github-repo]: https://github.com/kbhomes/baseline-diagnostic-font
            [github-home]: https://github.com/

            ## License

            This font contains [Noto Sans Mono][noto-sans-mono] glyphs in the rendering
            of its baseline labels. Like that font, this font is licensed under the
            [SIL Open Font License, Version 1.1][ofl-1.1], and is available at `LICENSE.txt`.

            [noto-sans-mono]: https://fonts.google.com/noto/specimen/Noto+Sans+Mono/license
            [ofl-1.1]: https://openfontlicense.org/open-font-license-official-text/
        '''))
        print(f"Wrote README at {out_path}")


def write_font_license():
    out_path = "dist/LICENSE.md"
    with open(out_path, "w") as f:
        f.write(dedent(r'''
            Copyright (c) 2026, Sajid Anwar.

            This Font Software is licensed under the SIL Open Font License, Version 1.1.
            This license is copied below, and is also available with a FAQ at:
            https\://openfontlicense.org
            &nbsp;

            \----------------------------------------------------------------------

            #### SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007

            \----------------------------------------------------------------------

            &nbsp;

            PREAMBLE
            -----------

            The goals of the Open Font License (OFL) are to stimulate worldwide
            development of collaborative font projects, to support the font creation
            efforts of academic and linguistic communities, and to provide a free and
            open framework in which fonts may be shared and improved in partnership
            with others.

            The OFL allows the licensed fonts to be used, studied, modified and
            redistributed freely as long as they are not sold by themselves. The
            fonts, including any derivative works, can be bundled, embedded,
            redistributed and/or sold with any software provided that any reserved
            names are not used by derivative works. The fonts and derivatives,
            however, cannot be released under any other type of license. The
            requirement for fonts to remain under this license does not apply
            to any document created using the fonts or their derivatives.

            DEFINITIONS
            -----------

            "Font Software" refers to the set of files released by the Copyright
            Holder(s) under this license and clearly marked as such. This may
            include source files, build scripts and documentation.

            "Reserved Font Name" refers to any names specified as such after the
            copyright statement(s).

            "Original Version" refers to the collection of Font Software components as
            distributed by the Copyright Holder(s).

            "Modified Version" refers to any derivative made by adding to, deleting,
            or substituting -- in part or in whole -- any of the components of the
            Original Version, by changing formats or by porting the Font Software to a
            new environment.

            "Author" refers to any designer, engineer, programmer, technical
            writer or other person who contributed to the Font Software.

            PERMISSION & CONDITIONS
            -----------

            Permission is hereby granted, free of charge, to any person obtaining
            a copy of the Font Software, to use, study, copy, merge, embed, modify,
            redistribute, and sell modified and unmodified copies of the Font
            Software, subject to the following conditions:

            1) Neither the Font Software nor any of its individual components,
            in Original or Modified Versions, may be sold by itself.

            2) Original or Modified Versions of the Font Software may be bundled,
            redistributed and/or sold with any software, provided that each copy
            contains the above copyright notice and this license. These can be
            included either as stand-alone text files, human-readable headers or
            in the appropriate machine-readable metadata fields within text or
            binary files as long as those fields can be easily viewed by the user.

            3) No Modified Version of the Font Software may use the Reserved Font
            Name(s) unless explicit written permission is granted by the corresponding
            Copyright Holder. This restriction only applies to the primary font name as
            presented to the users.

            4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
            Software shall not be used to promote, endorse or advertise any
            Modified Version, except to acknowledge the contribution(s) of the
            Copyright Holder(s) and the Author(s) or with their explicit written
            permission.

            5) The Font Software, modified or unmodified, in part or in whole,
            must be distributed entirely under this license, and must not be
            distributed under any other license. The requirement for fonts to
            remain under this license does not apply to any document created
            using the Font Software.

            TERMINATION
            -----------

            This license becomes null and void if any of the above conditions are
            not met.

            DISCLAIMER
            -----------

            THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
            EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
            MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
            OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
            COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
            INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
            DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
            FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
            OTHER DEALINGS IN THE FONT SOFTWARE.
        '''))
        print(f"Wrote OFL 1.1 license at {out_path}")

def dashing(value: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', value).lower()

if __name__ == "__main__":
    main()
