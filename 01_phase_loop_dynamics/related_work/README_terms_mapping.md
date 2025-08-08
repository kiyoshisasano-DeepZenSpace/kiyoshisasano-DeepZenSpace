# 📘 Terms Mapping — PLD Related Work & Frameworks

This directory contains the **cross-domain mapping** between **Phase Loop Dynamics (PLD)** concepts and  
**external academic fields, theories, and references**.

---

## 📍 Primary Source

All mappings originate from **`mapping.canonical.yaml`** — the single source of truth.  
From this YAML file, the following outputs are automatically generated:

- `README_terms_mapping.md` — **Forward mapping** (PLD → related fields)
- `academic_to_pd_reverse_mapping.md` — **Reverse mapping** (Related fields → PLD)
- Additional derived tables or visualizations as needed

> **Editing rule:**  
> Never edit the `.md` mapping files directly.  
> Always update `mapping.canonical.yaml` and regenerate.

---

## 📂 File Structure

| File | Description | Source |
|------|-------------|--------|
| `mapping.canonical.yaml` | Canonical mapping data (terms, domains, references) | Manual edit |
| `README_terms_mapping.md` | Forward mapping from PLD terms to related research | Auto-generated |
| `academic_to_pd_reverse_mapping.md` | Reverse mapping from research areas to PLD terms | Auto-generated |
| `foundational_terms.md` | Definitions of core PLD terms | Manual edit |
| `academic_links.md` | Annotated list of related domains and key references | Manual edit |

---

## 🔄 Update Workflow

1. **Edit** `mapping.canonical.yaml`  
   - Add new PLD terms  
   - Add related research or references  
   - Add descriptions or annotations

2. **Regenerate mapping files**  
   ```bash
   python generate_mappings.py
   ```
This will update the forward and reverse `.md` mapping files.

3. **Commit & submit a pull request**  
   - Contributors only need to change the YAML file  
   - `.md` changes are reviewed as generated output

---

## 🤝 Contribution Guidelines

- Contributions of new terms or references are welcome  
- Always set the classification (`@core`, `@support`, `@derived`, etc.) for each term  
- Use stable links for references (DOI, permanent archives preferred)  

---

## 📜 License

All materials in this directory are licensed under **Creative Commons BY-NC 4.0**.  
Non-commercial use is allowed with attribution.

---

> *This mapping is designed as a **navigation tool** to clarify PLD’s interdisciplinary position  
> and facilitate collaboration between different research domains.*
