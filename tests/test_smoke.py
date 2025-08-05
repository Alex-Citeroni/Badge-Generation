from pathlib import Path
import pytest
from badgegen.core import generate_badges, Columns, Layout, FontSpec

def test_generate_smoke(tmp_path: Path):
    template = Path("examples/template.pdf")
    excel    = Path("examples/nomi.xlsx")
    if not (template.exists() and excel.exists()):
        pytest.skip("Risorse esempio mancanti")
    outdir   = tmp_path / "out"
    pages = generate_badges(
        excel_path=excel,
        template_pdf=template,
        output_dir=outdir,
        columns=Columns(),
        layout=Layout(),
        font_spec=FontSpec(path=Path("fonts/DejaVuSans.ttf")),
    )
    assert pages >= 1
