# demo_pld_trace/generate_trace.py
import json
import os
from datetime import datetime, timedelta
from utils.pause_classifier import classify_pause
from utils.reentry_detector import detect_reentry

# --- helpers ---------------------------------------------------------------

def strip_icons(text: str) -> str:
    """Remove leading icons (⏸️/🔄) to avoid duplication in output."""
    if not text:
        return ""
    return text.lstrip("⏸️🔄 ").strip()

def safe(s: str) -> str:
    """Escape double quotes for Mermaid node labels."""
    return s.replace('"', '\\"')

def fmt_ts(ts: str) -> str:
    """Short human-friendly timestamp: YYYY-MM-DD HH:MM"""
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts

# ---- core ------------------------------------------------------------------

def parse_log(log_text: str):
    """
    Parse a simple conversation log in [User]/[Bot] format.
    Adds pseudo-timestamps in 3-second increments for visual realism.
    """
    turns = []
    t0 = datetime.now()
    i_user = 0
    for i, line in enumerate(log_text.strip().splitlines()):
        line = line.strip()
        if line.startswith('[User]'):
            content = line[7:].strip()
            ts = (t0 + timedelta(seconds=i_user * 3)).isoformat()
            turns.append({'role': 'user', 'content': content, 'timestamp': ts})
            i_user += 1
        elif line.startswith('[Bot]'):
            content = line[6:].strip()
            ts = (t0 + timedelta(seconds=max(i_user * 3 - 2, 0))).isoformat()
            turns.append({'role': 'bot', 'content': content, 'timestamp': ts})
    return turns

def analyze_trace(turns):
    """Attach pause/reentry annotations to user turns."""
    analyzed = []
    past_segments = []
    for i, turn in enumerate(turns):
        if turn['role'] == 'user':
            pause_result = classify_pause(turn['content']) if i > 0 else None
            reentry_result = detect_reentry(
                past_segments=[t['content'] for t in past_segments if t['role'] == 'user'],
                current_input=turn['content']
            ) if past_segments else None

            analyzed.append({
                **turn,
                'pld_analysis': {
                    'pause': pause_result,
                    'reentry': reentry_result
                }
            })
            past_segments.append(turn)
        else:
            analyzed.append(turn)
    return analyzed

def save_outputs(analyzed_data):
    """Generate Mermaid-based Markdown and JSON files under outputs/."""
    os.makedirs('outputs', exist_ok=True)

    # --- Mermaid nodes & styles ---
    md_lines = [
        "# PLD Trace Analysis",
        "```mermaid",
        "graph TD",
        "    %% Layout hints",
        "    classDef pauseUI stroke:#f90,stroke-width:2px;",
        "    classDef pauseRepair stroke:#f00,stroke-width:2px;",
        "    classDef pauseDefault stroke:#f66,stroke-width:2px;",
        "",
        "    %% Legend",
        "    subgraph Legend",
        "      L1[⏸️ UI Friction]:::pauseUI",
        "      L2[⏸️ Repair]:::pauseRepair",
        "    end",
    ]

    user_ids = []  # [(node_id, turn)]
    node_idx = 1

    # Create nodes with icons and apply class by pause type
    for turn in analyzed_data:
        if turn['role'] != 'user':
            continue

        # prepend icons in node label if present
        icons = []
        pa = (turn.get('pld_analysis') or {}).get('pause')
        if pa:
            label = strip_icons(pa.get('classification', ''))
            if "UI Friction" in label:
                icons.append("⏸️")
            elif "Repair" in label:
                icons.append("⏸️")
        re = (turn.get('pld_analysis') or {}).get('reentry')
        if re and re.get('is_reentry'):
            icons.append("🔄")

        icon_prefix = (" ".join(icons) + " ") if icons else ""
        nid = f"U{node_idx}"
        user_ids.append((nid, turn))
        md_lines.append(f'    {nid}["{icon_prefix}{safe(turn["content"])}"]')

        # class by pause type
        if pa:
            ptxt = strip_icons(pa.get('classification', ''))
            if "UI Friction" in ptxt:
                md_lines.append(f"    class {nid} pauseUI;")
            elif "Repair" in ptxt:
                md_lines.append(f"    class {nid} pauseRepair;")
            else:
                md_lines.append(f"    class {nid} pauseDefault;")
        node_idx += 1

    # Sequential edges (U1 --> U2 --> ...)
    for i in range(len(user_ids) - 1):
        a, b = user_ids[i][0], user_ids[i + 1][0]
        md_lines.append(f"    {a} --> {b}")

    # Optional: annotate “User turn sequence”
    if user_ids:
        md_lines.append("")
        md_lines.append("    %% User turn sequence annotation")
        md_lines.append(f'    note1(["User turns flow →"])')
        md_lines.append(f"    note1 --- {user_ids[0][0]}")

    md_lines.append("```")
    md_lines.append("")
    md_lines.append("## Pause / Reentry Tags (short timestamps)")

    # Pretty tags list
    for nid, turn in user_ids:
        pa = (turn.get('pld_analysis') or {}).get('pause')
        re = (turn.get('pld_analysis') or {}).get('reentry')
        md_lines.append(f"- **{fmt_ts(turn['timestamp'])}** [User] {turn['content']}")
        if pa:
            md_lines.append(f"  - ⏸️ {strip_icons(pa.get('classification'))}")
            reason = strip_icons(pa.get('reason'))
            if reason:
                md_lines.append(f"  - 💬 {reason}")
        if re and re.get('is_reentry'):
            match = re.get('matching_segment', '')
            if match:
                md_lines.append(f'  - 🔄 Reentry to: "{match}"')

    with open(os.path.join('outputs', 'pld_trace.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    # JSON remains the same (structured data for devs)
    with open(os.path.join('outputs', 'pld_trace.json'), 'w', encoding='utf-8') as f:
        json.dump(analyzed_data, f, ensure_ascii=False, indent=2)


# ---- main ------------------------------------------------------------------

if __name__ == "__main__":
    # Read as UTF-8 so special symbols (like "≡") don't get mangled
    with open('input_trace.txt', 'r', encoding='utf-8') as f:
        log_text = f.read()

    turns = parse_log(log_text)
    analyzed = analyze_trace(turns)
    save_outputs(analyzed)
    print("✅ Analysis completed. See outputs/pld_trace.md and outputs/pld_trace.json")
