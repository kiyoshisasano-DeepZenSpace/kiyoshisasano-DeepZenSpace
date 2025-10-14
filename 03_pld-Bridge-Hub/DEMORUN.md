# PLD Bridge Hub — One-Command Demo

This demo creates a tiny event set, validates it against `pld_event.schema.json`, and writes a short report.  
**You only copy & run commands.**

---

## 1️⃣ Move to the Bridge Hub folder

```bash
cd 03_pld-Bridge-Hub
```

---

## 2️⃣ Create a Python environment (pick ONE of these)

### macOS / Linux

```bash
python3 -m venv .venv && source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 3️⃣ Install the only dependency

We use **jsonschema** for validation (optional but recommended).

```bash
pip install --upgrade pip
pip install jsonschema
```

---

## 4️⃣ Run the demo

```bash
python bootstrap_demo.py
```

### What happens

- Writes `03_pld-Bridge-Hub/demo_quick/events_demo.jsonl`
- Validates each line against `../02_quickstart_kit/30_metrics/schemas/pld_event.schema.json`
- If not found, uses a built-in fallback schema
- Writes `03_pld-Bridge-Hub/demo_quick/demo_report.md`

> 💡 If `jsonschema` is not installed, validation is skipped (the report will mention this).

---

## 5️⃣ Open the report

Open:

```
03_pld-Bridge-Hub/demo_quick/demo_report.md
```

You should see:  
- Valid event count  
- Event tallies  
- Calculated demo metrics

---

## 6️⃣ Troubleshooting

| Error | Solution |
|-------|-----------|
| `ModuleNotFoundError: jsonschema` | Run `pip install jsonschema` then retry |
| `Schema file not found` | Script uses fallback schema automatically. To use repo schema, ensure this path exists:<br>`../02_quickstart_kit/30_metrics/schemas/pld_event.schema.json` |
| `Permission denied` (Windows) | Run PowerShell as Administrator, or try:<br>`py bootstrap_demo.py` |

---

## 7️⃣ Next steps

Replace the demo events with your real telemetry and re-run.

Validate your own JSONL via:

```bash
./scripts/validate_events.sh path/to/your_events.jsonl
```

Wire into your dashboard (e.g., `reentry_success_dashboard.json`) to compare metrics.

Keep using the same validator so your events always comply.

---
