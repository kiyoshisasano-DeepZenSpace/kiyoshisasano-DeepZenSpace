# 🤝 Contributing to PLD-Bridge Hub

Welcome, contributor!  
This repository connects theory and code under the **Phase Loop Dynamics (PLD)** framework.  
We welcome contributions across code, templates, theory alignment, and more.

---

## 📘 Theory Alignment Checklist

Before submitting a pull request, please confirm the theoretical consistency of your changes:

- [ ] Does your change correspond to a **phase** or **operator** in PLD theory?
- [ ] If UI-related:  
  - Drift → *Paper 1* Section 3.2  
  - Repair → *Paper 2* Figure 4  
- [ ] If code-related:  
  - Phase ops → *Paper 1* Table 1
- [ ] Reference relevant DOIs from [`docs/zenodo_paper_links.md`](../docs/zenodo_paper_links.md)

---

## ✨ Contribution Types

| Type            | Description                            | Emoji     |
|-----------------|----------------------------------------|-----------|
| ✨ New Feature   | Add new detection operators            | 🧠        |
| 🐞 Bug Fix       | Fix incorrect classifications          | 🚑        |
| 📝 Docs Update   | Improve guides or theory references    | 📚        |
| 🔧 Refactoring   | Improve code structure without behavior changes | 🧰    |

---

## 🧪 Tests & Evaluation

Ensure your contributions include tests where applicable.  
For PLD-specific functions, include **phase-aware test coverage**.

**Drift → Reentry Example**:
```python
def test_drift_reentry():
    # 1. Induce artificial delay
    # 2. Detect reentry pattern
    # 3. Validate repair mechanism
```
Use pytest with 80%+ coverage when possible.
Run tests via:
bash```
pytest --cov=./ --cov-report=term
```
## 🧩 Tone & Formatting

Please use language aligned with PLD theory when writing commits, comments, or documentation:

- ✅ Good: `"This enables smoother reentry after drift."`
- 🚫 Avoid: `"This just makes it faster."`

**Preferred Emoji:**
- 🌀 Loops / Rhythm tracking  
- ⏸️ Pause classification  
- 🔄 Repair transitions  
- 🌊 Phase shift

---

## 🔐 Licensing Note

All contributions are under **CC BY-NC 4.0**:

- **Derivative Works**:  
  Contributions must maintain a recognizable PLD phase structure.

- **Attribution Required**:  
  Please cite the original Zenodo papers (see `docs/zenodo_paper_links.md`).

---

## 🛠️ Development Setup

```bash
# Optional: Create local symlink to theory docs
ln -s ../docs/zenodo_paper_links.md ./theory_ref.md

# Install required libraries
pip install -r requirements.txt
```
## 📄 File Layout
```
├── structure_generators/
│   ├── pause_classifier.py
│   ├── reentry_detector.py
│   └── latency_tracker.py
├── notion_ui_templates/
│   └── README_notion_ui_templates.md
├── docs/
│   └── zenodo_paper_links.md
├── CONTRIBUTING.md
└── LICENSE
```

Thank you for helping shape a more rhythm-aware, theory-grounded interface future.
Let your contributions echo, reenter, and resonate. 🔁
