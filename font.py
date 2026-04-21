import os
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import List, Literal, Optional, Union

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, getTableClass, newTable
from fontTools.ttLib.tables import otTables

BORDER_WIDTH = 12


@dataclass
class FontBaselineStyle:
    stroke_style: str
    stroke_width: int


FontBaselineStyle.SOLID = FontBaselineStyle("solid", 12)
FontBaselineStyle.DASHED = FontBaselineStyle("dashed", 8)


@dataclass
class FontBaseline:
    id: str
    position: int
    table: Union[Literal["BASE", "OS/2", "hhea"], None]
    name: str
    label: str
    style: FontBaselineStyle


class FontGlyphKind(Enum):
    EMBOX_FILLED = auto()
    EMBOX_OUTLINE = auto()
    PAIR_LAYOUT = auto()
    PAIR_LABELED = auto()


@dataclass
class FontGlyph:
    char: str
    kind: FontGlyphKind
    baseline_ids: Optional[List[str]] = None


@dataclass
class Font:
    name: str
    description: str
    baselines: List[FontBaseline]
    glyphs: List[FontGlyph] = field(default_factory=list)


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int


@dataclass
class GlyphMetrics:
    glyph: any
    width: float


@dataclass
class TextMetrics:
    scale: float
    letter_gap: float
    glyphs: List[GlyphMetrics]

    def width(self) -> float:
        if len(self.glyphs) == 0:
            return 0
        return sum(g.width for g in self.glyphs) + (
            self.letter_gap * (len(self.glyphs) - 1)
        )


def measure_text(font, text: str, letter_gap=0.0) -> TextMetrics:
    font_head = font["head"]
    font_horizontal_metrics = font["hmtx"]
    em_units = font_head.unitsPerEm

    glyphs: List[GlyphMetrics] = []
    for char in text:
        glyph_name = font.getBestCmap()[ord(char)]
        glyph_set = font.getGlyphSet()
        glyph = glyph_set[glyph_name]
        glyphs.append(
            GlyphMetrics(glyph, font_horizontal_metrics[glyph_name][0] / em_units)
        )

    return TextMetrics(scale=1.0 / em_units, letter_gap=letter_gap, glyphs=glyphs)


def draw_text_centered(
    pen, font, text, x, y, font_size=50, scale_y=1.0, letter_gap=0.0, offset_y=-0.1
) -> Rect:
    text_metrics = measure_text(font, text, letter_gap)
    height = font_size * scale_y
    width = text_metrics.width() * font_size

    x_pos = x - width / 2
    y_pos = y - height / 2

    for glyph in text_metrics.glyphs:
        transform_pen = TransformPen(
            pen,
            (
                font_size * text_metrics.scale,
                0,
                0,
                font_size * scale_y * text_metrics.scale,
                x_pos,
                y_pos - height * offset_y,
            ),
        )
        glyph.glyph.draw(transform_pen)
        x_pos += font_size * (glyph.width + letter_gap)

    return Rect(x=(x - width / 2), y=(y - height / 2), width=width, height=height)


def draw_rectangle(pen, x1, y1, x2, y2):
    pen.moveTo((x1, y1))
    pen.lineTo((x2, y1))
    pen.lineTo((x2, y2))
    pen.lineTo((x1, y2))
    pen.closePath()


def draw_bordered_rectangle(pen, x1, y1, x2, y2, stroke_width=12):
    # Draw a rectangle for each edge
    draw_rectangle(pen, x1, y1, x2, y1 + stroke_width)
    draw_rectangle(pen, x1, y2 - stroke_width, x2, y2)
    draw_rectangle(pen, x1, y1 + stroke_width, x1 + stroke_width, y2 - stroke_width)
    draw_rectangle(pen, x2 - stroke_width, y1 + stroke_width, x2, y2 - stroke_width)


def draw_dashed_line(pen, y, start, end, stroke_width=4, dash_width=12, gap=6):
    for x in range(round(start), round(end), dash_width + gap):
        draw_solid_line(pen, y, x, x + dash_width, stroke_width)


def draw_solid_line(pen, y, start, end, stroke_width=4):
    draw_rectangle(pen, start, y - stroke_width / 2, end, y + stroke_width / 2)


def draw_line(pen, y, start, end, style="solid", stroke_width=8):
    if style == "solid":
        draw_solid_line(pen, y, start, end, stroke_width=stroke_width)
    elif style == "dashed":
        draw_dashed_line(pen, y, start, end, stroke_width=stroke_width)


def draw_baseline(pen, font, y, em_size, label, style="solid", stroke_width=8):
    if label:
        drawn_text = draw_text_centered(
            pen, font, label, em_size / 2, y, font_size=50, scale_y=1, letter_gap=0
        )
        draw_line(
            pen,
            style=style,
            stroke_width=stroke_width,
            y=y,
            start=BORDER_WIDTH,
            end=drawn_text.x - BORDER_WIDTH,
        )
        draw_line(
            pen,
            style=style,
            stroke_width=stroke_width,
            y=y,
            start=drawn_text.x + drawn_text.width + BORDER_WIDTH,
            end=em_size - BORDER_WIDTH,
        )
    else:
        draw_line(
            pen,
            style=style,
            stroke_width=stroke_width,
            y=y,
            start=BORDER_WIDTH,
            end=em_size - BORDER_WIDTH,
        )


def build_baselines_font(font: Font, out_path: str):
    baselines = font.baselines
    ascent = next(baseline.position for baseline in baselines if baseline.id == 'ascent')
    descent = next(baseline.position for baseline in baselines if baseline.id == 'descent')
    em_size = ascent - descent

    if not ascent or not descent:
        raise ValueError(f"Required ascent / descent but got {ascent} / {descent}")

    baseline_by_id = {}
    for baseline in baselines:
        if baseline.id not in baseline_by_id:
            baseline_by_id[baseline.id] = baseline

    # .notdef: bordered rectangle
    notdef_glyph_pen = TTGlyphPen(None)
    draw_bordered_rectangle(notdef_glyph_pen, 0, descent, em_size, ascent, BORDER_WIDTH)

    # X: all baselines with style drawn
    diag_glyph_pen = TTGlyphPen(None)
    draw_bordered_rectangle(diag_glyph_pen, 0, descent, em_size, ascent, BORDER_WIDTH)

    label_font = TTFont("./support/noto/NotoSansMono-Bold.ttf")

    for baseline in baselines:
        if baseline.style:
            draw_baseline(
                diag_glyph_pen,
                label_font,
                baseline.position,
                em_size,
                baseline.label,
                style=baseline.style.stroke_style,
                stroke_width=baseline.style.stroke_width,
            )

    glyph_order = [".notdef", "X"]
    char_map = {ord("X"): "X"}
    glyf_table = {".notdef": notdef_glyph_pen.glyph(), "X": diag_glyph_pen.glyph()}
    h_metrics = {".notdef": (em_size, 0), "X": (em_size, 0)}

    for glyph in font.glyphs:
        cp = ord(glyph.char)
        name = f"uni{cp:04X}" if cp <= 0xFFFF else f"u{cp:05X}"
        pen = TTGlyphPen(None)

        if glyph.kind == FontGlyphKind.EMBOX_FILLED:
            draw_rectangle(pen, 0, descent, em_size, ascent)

        elif glyph.kind == FontGlyphKind.EMBOX_OUTLINE:
            draw_bordered_rectangle(pen, 0, descent, em_size, ascent, BORDER_WIDTH)

        elif glyph.kind == FontGlyphKind.PAIR_LAYOUT:
            b1 = baseline_by_id[glyph.baseline_ids[0]]
            b2 = baseline_by_id[glyph.baseline_ids[1]]
            lower = min(b1.position, b2.position)
            upper = max(b1.position, b2.position)
            draw_rectangle(pen, 0, lower, em_size, upper)

        elif glyph.kind == FontGlyphKind.PAIR_LABELED:
            draw_bordered_rectangle(pen, 0, descent, em_size, ascent, BORDER_WIDTH)
            for b in baselines:
                if b.style and b.label is None:
                    draw_baseline(pen, label_font, b.position, em_size, None,
                                  style=b.style.stroke_style, stroke_width=b.style.stroke_width)
            for bid in glyph.baseline_ids:
                b = baseline_by_id[bid]
                style = b.style if b.style else FontBaselineStyle.SOLID
                draw_baseline(
                    pen,
                    label_font,
                    b.position,
                    em_size,
                    b.label,
                    style=style.stroke_style,
                    stroke_width=style.stroke_width,
                )

        glyph_order.append(name)
        char_map[cp] = name
        glyf_table[name] = pen.glyph()
        h_metrics[name] = (em_size, 0)

    fb = FontBuilder(em_size, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(char_map)
    fb.setupGlyf(glyf_table)

    os2_values = dict((base.name, base.position) for base in baselines if base.table == "OS/2")
    hhea_values = dict((base.name, base.position) for base in baselines if base.table == "hhea")
    vhea_values = dict((base.name, base.position) for base in baselines if base.table == "vhea")

    style_name = "Regular"
    fb.setupPost()
    fb.setupNameTable({
        "copyright": "Copyright (c) 2026, Sajid Anwar",
        "familyName": font.name,
        "styleName": style_name,
        "uniqueFontIdentifier": f"{font.name}-{style_name}",
        "fullName": f"{font.name}-{style_name}",
        "psName": f"{font.name}-{style_name}",
        "version": "Version 1.0",
    })
    fb.setupHorizontalMetrics(h_metrics)
    fb.setupOS2(**os2_values)
    fb.setupHorizontalHeader(**hhea_values)
    fb.setupVerticalHeader(**vhea_values)
    fb.setupHead(unitsPerEm=em_size)

    bases = list(sorted(filter(lambda base: base.table == "BASE", baselines), key=lambda base: base.name))
    base_names = list(base.name for base in bases)

    base_table = otTables.BASE()
    base_table.Version = 0x00010000
    base_table.HorizAxis = otTables.Axis()
    base_table.HorizAxis.BaseTagList = otTables.BaseTagList()
    base_table.HorizAxis.BaseTagList.BaselineTag = base_names
    base_table.HorizAxis.BaseScriptList = otTables.BaseScriptList()
    base_table.VertAxis = otTables.Axis()
    base_table.VertAxis.BaseTagList = otTables.BaseTagList()
    base_table.VertAxis.BaseTagList.BaselineTag = base_names
    base_table.VertAxis.BaseScriptList = otTables.BaseScriptList()

    base_coords = []
    for base in bases:
        base_coord = otTables.BaseCoord()
        base_coord.Coordinate = base.position
        base_coord.Format = 1
        base_coords.append(base_coord)

    base_script = otTables.BaseScriptRecord()
    base_script.BaseScriptTag = "DFLT"
    base_script.BaseScript = otTables.BaseScript()
    base_script.BaseScript.BaseValues = otTables.BaseValues()
    base_script.BaseScript.BaseValues.DefaultIndex = base_names.index("romn")
    base_script.BaseScript.BaseValues.BaseCoord = base_coords
    base_table.HorizAxis.BaseScriptList.BaseScriptRecord = [base_script]
    base_table.VertAxis.BaseScriptList.BaseScriptRecord = [base_script]
    fb.font["BASE"] = newTable("BASE")
    fb.font["BASE"].table = base_table

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fb.save(out_path)
    print(f"Created font at {out_path}")
