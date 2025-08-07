# 🏷️ badgegen

`badgegen` is a tiny utility (CLI + Python API) that turns

1. a **PDF template** (usually an A4 page with graphics),
2. a **spreadsheet** (Excel/CSV) containing participant data (name, surname, company), and
3. an optional **TrueType/OpenType font**

into ready‑to‑print PDF **badges**.

> **Typical use‑case**: a conference where you print and fold an A4 sheet in quarters to get front/back badges.

---

## 🚀 Installation

```bash
# inside a virtualenv
pip install -e .        # local clone in editable mode
# or directly from GitHub
```

Requires **Python ≥ 3.9** and these dependencies:

| Package               | Purpose                   |
| --------------------- | ------------------------- |
| **PyMuPDF**           | PDF editing & text layout |
| **pandas + openpyxl** | reading Excel/CSV         |
| **typer**             | command‑line interface    |
| **PyYAML**            | YAML configuration        |

---

## ⚡ Quick CLI

```bash
badgegen \
  --excel nomi.xlsx \
  --template template.pdf \
  --config src/badgegen/layouts/a4_2x2.yaml \
  --output badge_output
```

### Main options

| Flag             | Meaning                                   |
| ---------------- | ----------------------------------------- |
| `--excel,  -e`   | Spreadsheet with data (XLSX, CSV)         |
| `--template, -t` | Source PDF template                       |
| `--output,  -o`  | Directory where PDFs will be saved        |
| `--config,  -c`  | YAML defining **layout, columns, font**   |
| `--sheet`        | Sheet name/index if the workbook has many |

Run `badgegen --help` for full list.

---

## 🧩 YAML configuration

Example `a4_2x2.yaml` (shipped in `src/badgegen/layouts/`):

```yaml
layout:
  rows: 2          # 2×2 grid
  cols: 2
  margin_x: 30
  top_offset: 125
  box_height: 200
  rotation_top: 0
  rotation_bottom: 180
  align: 1

columns:
  first_name: "NAME"
  full_name:  "FULL NAME"
  company:    "COMPANY"
  lastname:   "LASTNAME"   # used for filename only

font:
  path:  "fonts/DejaVuSans.ttf"
  alias: "dejavu"
  big:        40   # max size first line
  small:      16   # max size lines 2‑3
  min_big:    24
  min_small:  10
```

Feel free to add more presets (e.g. `a4_3x1.yaml`, `a6_single.yaml`) and pass them with `--config`.

---

## 🐍 Library usage

```python
from pathlib import Path
from badgegen.core import generate_badges, FontSpec, Columns, Layout

pages = generate_badges(
    excel_path=Path("nomi.xlsx"),
    template_pdf=Path("template.pdf"),
    output_dir=Path("badge_output"),
    font_spec=FontSpec(path=Path("fonts/calibri-regular.ttf")),
    layout=Layout(rows=2, cols=2),
)
print(f"Generated {pages} PDFs!")
```

---

## 📂 Project layout

```
badgegen/
│  pyproject.toml – metadata & deps
└─ src/badgegen/
   ├─ core.py        – main functions
   ├─ cli.py         – Typer CLI
   ├─ layouts/       – YAML presets
   └─ …
```

---

## ⚖️ License

MIT – free to use, modify and distribute. If you improve it, please open a PR!

---

## 🤝 Contributing

1. Fork / create a branch
2. `pre-commit install` (lint & format)
3. `pytest -q`
4. Open your pull‑request 🙌
