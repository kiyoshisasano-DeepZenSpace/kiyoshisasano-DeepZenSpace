# PLD Bridge Hub — One-Command Demo

This demo creates a tiny event set, validates it against `pld_event.schema.json`, and writes a short report.  
**You only copy & run commands.**

---

## 1) Move to the Bridge Hub folder

```bash
cd 03_pld-Bridge-Hub
```

> If this folder doesn't exist on your machine, clone your repo first and `cd` into it.

---

## 2) Create a Python environment (pick ONE of these)

### macOS/Linux
```bash
python3 -m venv .venv && source .venv/bin/activate
```

### Windows (PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 3) Install the only dependency
We use `jsonschema` for validation (optional but recommended).

```bash
pip install --upgrade pip
pip install jsonschema
```

---

## 4) Download the demo script
Save the file as `03_pld-Bridge-Hub/bootstrap_demo.py` and run it.

If you downloaded from the link in ChatGPT, place it at the path above.
Otherwise, copy the provided file content into that path.

---

## 5) Run the demo

```bash
python bootstrap_demo.py
```

**What happens**
- Writes `03_pld-Bridge-Hub/demo_quick/events_demo.jsonl`
- Validates each line against `../02_quickstart_kit/30_metrics/schemas/pld_event.schema.json`
  - If not found, uses a built-in fallback schema
- Writes `03_pld-Bridge-Hub/demo_quick/demo_report.md`

---

## 6) Open the report

- `03_pld-Bridge-Hub/demo_quick/demo_report.md`

You should see: valid count, event tallies, and calculated demo metrics.

---

## 7) Troubleshooting

- **ModuleNotFoundError: jsonschema**  
  → Run `pip install jsonschema` and re-run step 5.

- **Schema file not found**  
  → The script will use a fallback schema automatically. To use the repo schema, ensure this path exists relative to the script:  
  `../02_quickstart_kit/30_metrics/schemas/pld_event.schema.json`

- **Permission denied on Windows**  
  → Try running PowerShell as Administrator or use `py bootstrap_demo.py`.

---

## 8) Next steps

- Replace the demo events with your real telemetry and re-run.  
- Wire into your dashboard (e.g., `reentry_success_dashboard.json`) to compare metrics.  
- Keep using the same validator so your events always comply.
