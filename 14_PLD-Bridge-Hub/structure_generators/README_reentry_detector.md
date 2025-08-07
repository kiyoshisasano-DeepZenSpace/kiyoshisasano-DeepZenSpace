# 🔄 Reentry Detector — PLD-Based Intent Resumption Analysis

This module detects **reentry** in user input — when a user implicitly returns to a previously dropped or delayed topic.  
It is part of the **Phase Loop Dynamics (PLD)** toolkit, modeling interaction as cycles of **drift**, **repair**, and **reentry**.

---

## ⚙️ Functionality

Given a list of prior conversation segments and a current user input, this bot evaluates whether the new input constitutes a **reentry** — reconnecting with a past latent intent.

**PLD Concept Mapping**:  
| Code Element       | PLD Theory               |
|--------------------|--------------------------|
| `past_segments`    | Latent phase history     |
| `current_input`    | Recombination attempt    |
| `matching_segment` | Anchored reentry point   |

---

## 🧠 Theoretical Basis

📘 **Phase Loop Dynamics (PLD)** defines reentry as a return to a previously activated latent structure  
that may have been interrupted, delayed, or repaired.

- From Paper #1: *Reentry as loopwise resonance with initial semantic state*
- From Paper #2: *Segment → Delay → Recombination* model of dialogue

---

## 💡 How It Works

1. You pass in a list of `past_segments` (chronologically ordered).
2. Provide the `current_input` — the user’s latest message.
3. The LLM determines whether the new input reconnects with a past intent.
4. It returns:
   - `is_reentry` — whether reentry occurred
   - `reason` — explanation from the LLM
   - `matching_segment` — the past input it relates to (if any)

---

## 🧪 Usage Example

```python
from reentry_detector import detect_reentry

past = [
    "How do I export this as PDF?",
    "Wait, what does 'latency hold' mean again?",
    "Can I try this on mobile?"
]
new_input = "Actually, about the latency thing... is that why it paused?"

result = detect_reentry(past, new_input)
print(result)
```

🌀 Expected Output:

```json
{
  "is_reentry": true,
  "reason": "Yes — the input resumes the user's previous question about latency hold.",
  "matching_segment": "Wait, what does 'latency hold' mean again?"
}
```

---

### 🔍 Edge Case Testing (English Version)

```python
# Partial match
detect_reentry(["Trip to Tokyo"], "About that Tokyo thing...")

# Irrelevant input
detect_reentry(["I want to make a reservation"], "Totally unrelated, but...")
```

🧾 Sample Output:

```json
{
  "is_reentry": true,
  "reason": "Yes — user resumes a previously mentioned topic: Tokyo trip.",
  "matching_segment": "Trip to Tokyo"
}
```

```json
{
  "is_reentry": false,
  "reason": "The current input is unrelated to any prior segment.",
  "matching_segment": ""
}
```

---

## 🎛️ Configuration Notes

- **API Key:** Requires setting the OpenAI API key via environment variable:

```bash
export OPENAI_API_KEY="sk-..."  # (Linux/macOS)
set OPENAI_API_KEY="sk-..."     # (Windows)
```

- **Temperature Parameter:**  
  Default is `0.3`, to balance:
  - ✳️ Consistency (low randomness)  
  - ✳️ Nuanced pattern detection  

---

## 📚 Related Resources

- 📘 PLD Theories — [`docs/zenodo_paper_links.md`](../docs/zenodo_paper_links.md)  
- 📊 Generator Index — [`structure_generators/README_structure_generators.md`](../structure_generators/README_structure_generators.md)  
- 🧩 Notion Template — [`notion_ui_templates/README_notion_ui_templates.md`](../notion_ui_templates/README_notion_ui_templates.md)  

---

## 📜 License

**License:** Creative Commons BY-NC 4.0  
Structural reuse requires **attunement**, not extraction.  
Drift-aware contributions are preferred over speed or optimization.
