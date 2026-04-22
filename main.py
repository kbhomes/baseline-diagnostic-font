import re
from font import Font, FontBaseline, FontBaselineStyle, FontGlyph, FontGlyphKind, build_baselines_font
from jinja2 import Environment, FileSystemLoader
from textwrap import dedent, indent
from typing import Dict, List

AUTHOR = "Sajid Anwar"

def main():
    glyphs = [
        FontGlyph("x", FontGlyphKind.PAIR_LAYOUT,  ["x-height", "alphabetic"]),
        FontGlyph("χ", FontGlyphKind.PAIR_LABELED, ["x-height", "alphabetic"]),
        FontGlyph("B", FontGlyphKind.PAIR_LAYOUT,  ["cap-height", "alphabetic"]),
        FontGlyph("β", FontGlyphKind.PAIR_LABELED, ["cap-height", "alphabetic"]),
        FontGlyph("口", FontGlyphKind.PAIR_LAYOUT,  ["ideographic-over", "ideographic-under"]),
        FontGlyph("日", FontGlyphKind.PAIR_LABELED, ["ideographic-over", "ideographic-under"]),
        FontGlyph("中", FontGlyphKind.PAIR_LAYOUT,  ["ideographic-face-over", "ideographic-face-under"]),
        FontGlyph("田", FontGlyphKind.PAIR_LABELED, ["ideographic-face-over", "ideographic-face-under"]),
        FontGlyph("अ", FontGlyphKind.PAIR_LAYOUT,  ["hanging", "alphabetic"]),
        FontGlyph("आ", FontGlyphKind.PAIR_LABELED, ["hanging", "alphabetic"]),
        FontGlyph("+", FontGlyphKind.PAIR_LAYOUT,  ["math", "alphabetic"]),
        FontGlyph("±", FontGlyphKind.PAIR_LABELED, ["math", "alphabetic"]),
        FontGlyph("█", FontGlyphKind.EMBOX_FILLED),
        FontGlyph("□", FontGlyphKind.EMBOX_OUTLINE),
    ]

    fonts = []
    fonts.append(Font(
        name="BaselineDiagnostic",
        description=(dedent("""\
            Font that can be used for validating baseline alignments. Given the embedded
            text in the font, this should be used with very large font sizes. There are
            two glyphs in the font.""")),
        baselines=[
            FontBaseline("ascent",                    800,   "OS/2", "sTypoAscender",  None,                  None),
            FontBaseline("ascent",                    800,   "hhea", "ascent",         None,                  None),
            FontBaseline("ascent",                    800,   "vhea", "ascent",         None,                  None),
            FontBaseline("ideographic-over",          750,   "BASE", "idtp",           "IDEOGRAPHIC-OVER",    FontBaselineStyle.SOLID),
            FontBaseline("hanging",                   650,   "BASE", "hang",           "HANGING",             FontBaselineStyle.SOLID),
            FontBaseline("ideographic-face-over",     650,   "BASE", "icft",           "IDEO-FACE-OVER",      None),
            FontBaseline("cap-height",                550,   "OS/2", "sCapHeight",     "CAP-HEIGHT",          FontBaselineStyle.SOLID),
            FontBaseline("math",                      450,   "BASE", "math",           "MATH",                FontBaselineStyle.SOLID),
            FontBaseline("central",                   350,   None,   None,             "CENTRAL",             FontBaselineStyle.SOLID),
            FontBaseline("em-middle",                 300,   None,   None,             None,                  FontBaselineStyle.DASHED),
            FontBaseline("x-height",                  250,   "OS/2", "sxHeight",       "X-HEIGHT",            FontBaselineStyle.SOLID),
            FontBaseline("x-middle",                  150,   None,   None,             "X-MIDDLE",            FontBaselineStyle.SOLID),
            FontBaseline("alphabetic",                 50,   "BASE", "romn",           "ALPHABETIC",          FontBaselineStyle.SOLID),
            FontBaseline("ideographic-face-under",     50,   "BASE", "icfb",           "IDEO-FACE-UNDER",     None),
            FontBaseline("zero",                        0,   None,   None,             None,                  FontBaselineStyle.DASHED),
            FontBaseline("ideographic-under",         -50,   "BASE", "ideo",           "IDEOGRAPHIC-UNDER",   FontBaselineStyle.SOLID),
            FontBaseline("descent",                  -200,   "OS/2", "sTypoDescender", None,                  None),
            FontBaseline("descent",                  -200,   "hhea", "descent",        None,                  None),
            FontBaseline("descent",                  -200,   "vhea", "descent",        None,                  None),
        ],
        glyphs=glyphs,
    ))
    fonts.append(Font(
        name="BaselineDiagnosticAlphabeticZero",
        description=(dedent("""\
            Same as the "BaselineDiagnostic" font, but uses the common alphabetic baseline
            of 0. This also results in the x-middle baseline being at 125.""")),
        baselines=[
            FontBaseline("ascent",                    800,   "OS/2", "sTypoAscender",  None,                  None),
            FontBaseline("ascent",                    800,   "hhea", "ascent",         None,                  None),
            FontBaseline("ascent",                    800,   "vhea", "ascent",         None,                  None),
            FontBaseline("ideographic-over",          750,   "BASE", "idtp",           "IDEOGRAPHIC-OVER",    FontBaselineStyle.SOLID),
            FontBaseline("hanging",                   650,   "BASE", "hang",           "HANGING",             FontBaselineStyle.SOLID),
            FontBaseline("ideographic-face-over",     650,   "BASE", "icft",           "IDEO-FACE-OVER",      None),
            FontBaseline("cap-height",                550,   "OS/2", "sCapHeight",     "CAP-HEIGHT",          FontBaselineStyle.SOLID),
            FontBaseline("math",                      450,   "BASE", "math",           "MATH",                FontBaselineStyle.SOLID),
            FontBaseline("central",                   350,   None,   None,             "CENTRAL",             FontBaselineStyle.SOLID),
            FontBaseline("em-middle",                 300,   None,   None,             None,                  FontBaselineStyle.DASHED),
            FontBaseline("x-height",                  250,   "OS/2", "sxHeight",       "X-HEIGHT",            FontBaselineStyle.SOLID),
            FontBaseline("x-middle",                  125,   None,   None,             "X-MIDDLE",            FontBaselineStyle.SOLID),
            FontBaseline("alphabetic",                  0,   "BASE", "romn",           None,                  FontBaselineStyle.DASHED),
            FontBaseline("ideographic-face-under",     50,   "BASE", "icfb",           "IDEO-FACE-UNDER",     None),
            FontBaseline("zero",                        0,   None,   None,             None,                  None),
            FontBaseline("ideographic-under",         -50,   "BASE", "ideo",           "IDEOGRAPHIC-UNDER",   FontBaselineStyle.SOLID),
            FontBaseline("descent",                  -200,   "OS/2", "sTypoDescender", None,                  None),
            FontBaseline("descent",                  -200,   "hhea", "descent",        None,                  None),
            FontBaseline("descent",                  -200,   "vhea", "descent",        None,                  None),
        ],
        glyphs=glyphs,
    ))

    write_font_files(fonts)
    write_font_stylesheet(fonts)
    write_font_html(fonts)
    write_font_readme(fonts)
    write_font_license()


def write_font_files(fonts: List[Font]):
    for font in fonts:
        build_baselines_font(font, f'dist/{font.name}.ttf')


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


def prepare_template_data(fonts: List[Font]) -> dict:
    font = fonts[0]
    font_az = fonts[1]

    dfn_tooltips = {
        'central':   'Computed at halfway between ideographic-under and ideographic-over',
        'em-middle': 'Computed at halfway between ascent and descent',
        'x-middle':  'Computed at halfway between alphabetic and x-height',
        'zero':      'Zero coordinate',
    }

    seen: Dict[str, dict] = {}
    baseline_table = []
    for b in font.baselines:
        if b.id not in seen:
            entry = {'id': b.id, 'position': b.position, 'base': '', 'os2': '', 'hhea': '', 'tooltip': dfn_tooltips.get(b.id)}
            seen[b.id] = entry
            baseline_table.append(entry)
        if b.table == 'BASE':   seen[b.id]['base'] = b.name
        elif b.table == 'OS/2': seen[b.id]['os2']  = b.name
        elif b.table == 'hhea': seen[b.id]['hhea'] = b.name

    az_positions = {}
    for b in font_az.baselines:
        if b.id not in az_positions:
            az_positions[b.id] = b.position
    az_diffs = [{'id': e['id'], 'position': az_positions[e['id']]}
                for e in baseline_table
                if e['id'] in az_positions and az_positions[e['id']] != e['position']]
    az_diffs.sort(key=lambda baseline: baseline['id'])

    pair_map: Dict[tuple, dict] = {}
    pair_order = []
    for g in font.glyphs:
        if g.baseline_ids:
            key = tuple(g.baseline_ids)
            if key not in pair_map:
                pair_map[key] = {'ids': list(key), 'layout': None, 'labeled': None}
                pair_order.append(key)
            glyph_data = {'char': g.char, 'codepoint': f'U+{ord(g.char):04X}'}
            if g.kind == FontGlyphKind.PAIR_LAYOUT:   pair_map[key]['layout']  = glyph_data
            elif g.kind == FontGlyphKind.PAIR_LABELED: pair_map[key]['labeled'] = glyph_data

    def embox_data(kind):
        g = next((g for g in font.glyphs if g.kind == kind), None)
        return {'char': g.char, 'codepoint': f'U+{ord(g.char):04X}'} if g else None

    return {
        'font_name':    font.name,
        'font_az_name': font_az.name,
        'baseline_table': baseline_table,
        'az_diffs':     az_diffs,
        'pairs':        [pair_map[k] for k in pair_order],
        'embox_filled':  embox_data(FontGlyphKind.EMBOX_FILLED),
        'embox_outline': embox_data(FontGlyphKind.EMBOX_OUTLINE),
    }


def _jinja_env():
    return Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)


def write_font_html(fonts: List[Font]):
    out_path = "dist/index.html"
    data = prepare_template_data(fonts)
    html = _jinja_env().get_template('index.html.jinja').render(**data)
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"Wrote HTML at {out_path}")


def write_font_readme(fonts: List[Font]):
    out_path = "dist/README.md"
    data = prepare_template_data(fonts)
    md = _jinja_env().get_template('README.md.jinja').render(**data)
    with open(out_path, 'w') as f:
        f.write(md)
    print(f"Wrote README at {out_path}")


def write_font_license():
    out_path = "dist/LICENSE.md"
    md = _jinja_env().get_template('LICENSE.md.jinja').render(author=AUTHOR)
    with open(out_path, 'w') as f:
        f.write(md)
    print(f"Wrote OFL 1.1 license at {out_path}")

def dashing(value: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', value).lower()

if __name__ == "__main__":
    main()
