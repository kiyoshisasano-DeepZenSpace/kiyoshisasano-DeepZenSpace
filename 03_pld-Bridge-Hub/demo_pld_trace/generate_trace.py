import json, os
from pathlib import Path
from datetime import datetime, timedelta, timezone
from utils.pause_classifier import classify_pause
from utils.reentry_detector import detect_reentry
BASE = Path(__file__).resolve().parent

def strip_icons(text: str) -> str:
    if not text: return ""
    return text.lstrip("⏸️🔄 ").strip()

def safe(s: str) -> str:
    return (s or "").replace('"', '\\"').replace("[", "(").replace("]", ")").replace("`", "'")

def fmt_ts(ts: str) -> str:
    try:
        dt = datetime.fromisoformat(ts.replace("Z","+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts

def parse_log(log_text: str):
    turns = []
    t0_env = os.environ.get("PLD_TRACE_T0")
    if t0_env:
        t0 = datetime.fromisoformat(t0_env.replace("Z","+00:00"))
    else:
        t0 = datetime(2024,1,1,0,0,0,tzinfo=timezone.utc)
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
    analyzed = []
    past_segments = []
    for i, turn in enumerate(turns):
        if turn['role'] == 'user':
            pause_result = classify_pause(turn['content']) if i > 0 else None
            reentry_result = detect_reentry(
                past_segments=[t['content'] for t in past_segments if t['role'] == 'user'],
                current_input=turn['content']
            ) if past_segments else None
            analyzed.append({**turn,'pld_analysis': {'pause': pause_result,'reentry': reentry_result}})
            past_segments.append(turn)
        else:
            analyzed.append(turn)
    return analyzed

def save_outputs(analyzed_data):
    outdir = BASE / 'outputs'
    outdir.mkdir(exist_ok=True)

    md_lines = [
        "# PLD Trace Analysis",
        "```mermaid",
        "graph TD",
        "    classDef pauseUI stroke:#f90,stroke-width:2px;",
        "    classDef pauseRepair stroke:#f00,stroke-width:2px;",
        "    classDef pauseDefault stroke:#f66,stroke-width:2px;",
        "",
        "    subgraph Legend",
        "      L1[⏸️ UI Friction]:::pauseUI",
        "      L2[⏸️ Repair]:::pauseRepair",
        "    end",
    ]
    user_ids = []
    node_idx = 1
    for turn in analyzed_data:
        if turn['role'] != 'user':
            continue
        icons = []
        pa = (turn.get('pld_analysis') or {}).get('pause')
        if pa:
            label = strip_icons(pa.get('classification', ''))
            if "UI Friction" in label: icons.append("⏸️")
            elif "Repair" in label:   icons.append("⏸️")
        re = (turn.get('pld_analysis') or {}).get('reentry')
        if re and re.get('is_reentry'): icons.append("🔄")
        icon_prefix = (" ".join(icons) + " ") if icons else ""
        nid = f"U{node_idx}"
        user_ids.append((nid, turn))
        md_lines.append(f'    {nid}["{icon_prefix}{safe(turn["content"])}"]')
        if pa:
            ptxt = strip_icons(pa.get('classification', ''))
            if "UI Friction" in ptxt:  md_lines.append(f"    class {nid} pauseUI;")
            elif "Repair" in ptxt:     md_lines.append(f"    class {nid} pauseRepair;")
            else:                      md_lines.append(f"    class {nid} pauseDefault;")
        node_idx += 1
    for i in range(len(user_ids) - 1):
        a, b = user_ids[i][0], user_ids[i + 1][0]
        md_lines.append(f"    {a} --> {b}")
    if user_ids:
        md_lines += ["","    %% User turn sequence annotation", '    note1(["User turns flow →"])', f"    note1 --- {user_ids[0][0]}"]
    md_lines.append("```")
    md_lines.append("")
    md_lines.append("## Pause / Reentry Tags (short timestamps)")
    analyzed_data = sorted(analyzed_data, key=lambda x: x.get("timestamp",""))
    for nid, turn in user_ids:
        pa = (turn.get('pld_analysis') or {}).get('pause')
        re = (turn.get('pld_analysis') or {}).get('reentry')
        md_lines.append(f"- **{fmt_ts(turn['timestamp'])}** [User] {turn['content']}")
        if pa:
            md_lines.append(f"  - ⏸️ {strip_icons(pa.get('classification'))}")
            reason = strip_icons(pa.get('reason'))
            if reason: md_lines.append(f"  - 💬 {reason}")
        if re and re.get('is_reentry'):
            match = re.get('matching_segment', '')
            if match: md_lines.append(f'  - 🔄 Reentry to: "{match}"')
    md_lines.append("\n> NOTE: This is a demo trace. Timestamps are synthetic (UTC). Classification is heuristic.")
    (outdir / 'pld_trace.md').write_text('\n'.join(md_lines), encoding='utf-8')
    (outdir / 'pld_trace.json').write_text(json.dumps(analyzed_data, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == "__main__":
    log_text = (BASE / 'input_trace.txt').read_text(encoding='utf-8')
    turns = parse_log(log_text)
    analyzed = analyze_trace(turns)
    save_outputs(analyzed)
    print("✅ Analysis completed. See outputs/pld_trace.md and outputs/pld_trace.json")
