from __future__ import annotations
from pathlib import Path
from typing import Optional

import typer
import yaml

from .core import generate_badges, Columns, Layout, FontSpec

app = typer.Typer(help="Generatore di badge PDF da Excel e template PDF.")


@app.command()
def run(
    excel: Path = typer.Option(..., "--excel", "-e", help="File Excel con i dati"),
    template: Path = typer.Option(..., "--template", "-t", help="Template PDF"),
    output: Path = typer.Option("badge_output", "--output", "-o", help="Cartella output"),
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="File YAML di config"),
    sheet: Optional[str] = typer.Option(None, "--sheet", help="Nome foglio Excel"),
):
    columns = Columns()
    layout = Layout()
    font = None

    if config:
        data = yaml.safe_load(config.read_text(encoding="utf-8"))
        if "columns" in data:
            c = data["columns"]
            columns = Columns(
                first_name=c.get("first_name", columns.first_name),
                full_name=c.get("full_name", columns.full_name),
                company=c.get("company", columns.company),
                lastname=c.get("lastname", columns.lastname),
            )
        if "layout" in data:
            l = data["layout"]
            layout = Layout(
                margin_x=float(l.get("margin_x", layout.margin_x)),
                top_offset=float(l.get("top_offset", layout.top_offset)),
                box_height=float(l.get("box_height", layout.box_height)),
                rows=int(l.get("rows", layout.rows)),
                cols=int(l.get("cols", layout.cols)),
                rotation_top=int(l.get("rotation_top", layout.rotation_top)),
                rotation_bottom=int(l.get("rotation_bottom", layout.rotation_bottom)),
                align=int(l.get("align", layout.align)),
            )
        if "font" in data:
            f = data["font"]
            font = FontSpec(
                path=Path(f["path"]),
                alias=f.get("alias", "custom"),
                big=int(f.get("big", 40)),
                small=int(f.get("small", 16)),
                min_big=int(f.get("min_big", 24)),
                min_small=int(f.get("min_small", 10)),
                step=int(f.get("step", 1)),
            )

    pages = generate_badges(
        excel_path=excel,
        template_pdf=template,
        output_dir=output,
        columns=columns,
        layout=layout,
        font_spec=font,
        sheet_name=sheet,
    )
    typer.echo(f"✅ Creati {pages} PDF in '{output.resolve()}'")


def main():
    app()


if __name__ == "__main__":
    main()
