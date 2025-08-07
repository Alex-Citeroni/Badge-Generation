from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

import fitz  # PyMuPDF
import pandas as pd


@dataclass
class Columns:
    first_name: str = "NAME"
    full_name: str = "FULL NAME"
    company: str = "COMPANY"
    lastname: str = "LASTNAME"


@dataclass
class FontSpec:
    path: Path
    alias: str = "custom"
    big: int = 40
    small: int = 16
    min_big: int = 24
    min_small: int = 10
    step: int = 1


@dataclass
class Layout:
    margin_x: float = 30.0
    top_offset: float = 125.0
    box_height: float = 200.0
    rows: int = 2
    cols: int = 2
    rotation_top: int = 0
    rotation_bottom: int = 180
    align: int = 1


def _clean_filename(s: Optional[str], fallback: str = "anon") -> str:
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return fallback
    s = re.sub(r"[\W]", "_", str(s).strip(), flags=re.U)
    return s or fallback


def _insert_textbox_fit(
    page, rect, text, font, fontfile, start_size, min_size, step, rotate, align
):
    size = start_size
    while size >= min_size:
        if font.text_length(text, size) <= rect.width:
            break
        size -= step
    page.insert_textbox(
        rect,
        text,
        fontname="use_cust_font",
        fontfile=str(fontfile),
        fontsize=size,
        rotate=rotate,
        align=align,
    )


def _write_block(
    page, outer_rect, first_name, full_name, company, layout, font_spec, custom_font, rotate
):
    inner = fitz.Rect(
        outer_rect.x0 + layout.margin_x,
        (
            outer_rect.y0 + layout.top_offset
            if rotate == 0
            else outer_rect.y1 - layout.top_offset - layout.box_height
        ),
        outer_rect.x1 - layout.margin_x,
        (
            outer_rect.y0 + layout.top_offset + layout.box_height
            if rotate == 0
            else outer_rect.y1 - layout.top_offset
        ),
    )

    _insert_textbox_fit(
        page,
        inner,
        first_name,
        custom_font,
        font_spec.path,
        font_spec.big,
        font_spec.min_big,
        font_spec.step,
        rotate,
        layout.align,
    )

    shift_full = font_spec.big + 2
    direction = 1 if rotate == 0 else -1
    line2 = inner + (0, direction * shift_full, 0, direction * shift_full)
    _insert_textbox_fit(
        page,
        line2,
        full_name,
        custom_font,
        font_spec.path,
        font_spec.small,
        font_spec.min_small,
        font_spec.step,
        rotate,
        layout.align,
    )

    shift_comp = shift_full + font_spec.small + 4
    line3 = inner + (0, direction * shift_comp, 0, direction * shift_comp)
    _insert_textbox_fit(
        page,
        line3,
        company,
        custom_font,
        font_spec.path,
        font_spec.small,
        font_spec.min_small,
        font_spec.step,
        rotate,
        layout.align,
    )


def _make_grid(rect, rows, cols) -> List:
    W, H = rect.width, rect.height
    cell_w, cell_h = W / cols, H / rows
    return [
        fitz.Rect(c * cell_w, r * cell_h, (c + 1) * cell_w, (r + 1) * cell_h)
        for r in range(rows)
        for c in range(cols)
    ]


def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def generate_badges(
    excel_path: Path,
    template_pdf: Path,
    output_dir: Path,
    columns: Columns = Columns(),
    layout: Layout = Layout(),
    font_spec: Optional[FontSpec] = None,
    sheet_name: Optional[str] = None,
    duplicates_fill_last_page: bool = True,
) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)

    if font_spec is None:
        font_spec = FontSpec(path=Path("fonts/calibri-regular.ttf"), alias="calibri")

    custom_font = fitz.Font(fontfile=str(font_spec.path))

    df_raw = pd.read_excel(excel_path, dtype=str, sheet_name=sheet_name)
    if isinstance(df_raw, dict):
        df = next(iter(df_raw.values()))
    else:
        df = df_raw
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    df = df.dropna(
        subset=[columns.first_name, columns.full_name, columns.company], how="all"
    ).reset_index(drop=True)

    slots_per_page = layout.rows * layout.cols
    created = 0

    for i in range(0, len(df), slots_per_page):
        rows = df.iloc[i : i + slots_per_page]
        if duplicates_fill_last_page and len(rows) < slots_per_page:
            last = rows.iloc[-1:]
            while len(rows) < slots_per_page:
                rows = pd.concat([rows, last], ignore_index=True)

        doc = fitz.open(str(template_pdf))
        page = doc[0]
        rects = _make_grid(page.rect, layout.rows, layout.cols)

        for idx, rect in enumerate(rects):
            if idx >= len(rows):
                break

            if idx < layout.cols:
                row = rows.iloc[idx]
            else:
                row = rows.iloc[idx - layout.cols]
            fname_raw = str(row.get(columns.first_name, "") or "")
            first_name = fname_raw.split()[0].upper() if fname_raw else ""
            full_name = _normalize(str(row.get(columns.full_name, "") or ""))
            company = _normalize(str(row.get(columns.company, "") or "")).upper()

            r_idx = idx // layout.cols
            rotate = layout.rotation_top if r_idx == 0 else layout.rotation_bottom

            _write_block(
                page, rect, first_name, full_name, company, layout, font_spec, custom_font, rotate
            )

        r0, r1 = rows.iloc[0], rows.iloc[min(1, len(rows) - 1)]
        out_name = (
            f"badge_{_clean_filename(getattr(r0, columns.lastname, None))}_{_clean_filename(getattr(r0, columns.first_name, None))}"
            f"__{_clean_filename(getattr(r1, columns.lastname, None))}_{_clean_filename(getattr(r1, columns.first_name, None))}.pdf"
        )
        doc.save(output_dir / out_name)
        doc.close()
        created += 1

    return created
