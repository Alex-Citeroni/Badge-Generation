# 🏷️ badgegen

`badgegen` è un piccolo tool (CLI + API Python) che genera badge PDF partendo da:

1. un **template** PDF (in genere pagina A4 con grafica e campi vuoti),
2. un **foglio Excel / CSV** contenente dati dei partecipanti (nome, cognome, azienda),
3. un **font TrueType/OpenType** da incorporare nei PDF finali (opzionale se usi un font di sistema).

> **Use‑case tipico**: congresso o workshop dove stampi e pieghi un foglio A4 in quattro per avere fronte/retro dei badge.

---

## 🚀 Installazione

```bash
# dentro un virtualenv
pip install -e .   # clone + editable
# oppure direttamente da GitHub
```

Richiede **Python ≥ 3.9** e dipendenze:

| Pacchetto               | Perché serve                   |
| ----------------------- | ------------------------------ |
| **PyMuPDF** (`pymupdf`) | editing PDF e text‑layout      |
| **pandas + openpyxl**   | lettura Excel/CSV              |
| **typer**               | interfaccia a riga di comando  |
| **PyYAML**              | parsing file di configurazione |

---

## ⚡ CLI rapida

```bash
badgegen \
  --excel nomi.xlsx \
  --template template.pdf \
  --config src/badgegen/layouts/a4_2x2.yaml \
  --output badge_output
```

### Argomenti principali

| Flag             | Significato                                      |
| ---------------- | ------------------------------------------------ |
| `--excel,  -e`   | Workbook con i dati (XLSX, CSV)                  |
| `--template, -t` | PDF sorgente con la grafica                      |
| `--output,  -o`  | Cartella dove salvare i PDF generati             |
| `--config,  -c`  | YAML che definisce **layout, colonne, font**     |
| `--sheet`        | Nome/indice foglio Excel se ce ne sono più d’uno |

> Usa `badgegen --help` per la lista completa di opzioni.

---

## 🧩 Configurazione YAML

Esempio `a4_2x2.yaml` (in repo sotto `src/badgegen/layouts/`):

```yaml
layout:
  rows: 2     # griglia 2×2
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
  lastname:   "LASTNAME"   # usato per il nome file

font:
  path:  "fonts/DejaVuSans.ttf"
  alias: "dejavu"
  big:        40   # dimensione max prima riga
  small:      16   # dimensione max righe 2‑3
  min_big:    24
  min_small:  10
```

Puoi avere più preset (A6 singolo, A4 3×1…) e passarli con `--config`.

---

## 🐍 Uso come libreria

```python
from pathlib import Path
from badgegen.core import generate_badges, FontSpec, Columns, Layout

pages = generate_badges(
    excel_path=Path("nomi.xlsx"),
    template_pdf=Path("template.pdf"),
    output_dir=Path("badge_output"),
    font_spec=FontSpec(path=Path("fonts/DejaVuSans.ttf")),
    layout=Layout(rows=2, cols=2),
)
print(f"Creati {pages} PDF!")
```

---

## 📂 Struttura progetto

```
badgegen/
│  pyproject.toml – metadata & deps
└─ src/badgegen/
   ├─ core.py        – funzioni principali
   ├─ cli.py         – Typer CLI
   ├─ layouts/       – preset YAML
   └─ …
```

---

## ⚖️ Licenza

MIT – usa, modifica e distribuisci liberamente. Se pubblichi modifiche, fai una PR!

---

## 🤝 Contribuire

1. Fork / branch
2. `pre-commit install` (lint + format)
3. `pytest -q`
4. Apri la tua pull‑request 🙌
