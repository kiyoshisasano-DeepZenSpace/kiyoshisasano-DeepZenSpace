# demo_pld_trace/generate_trace.py
import json
from datetime import datetime
from utils.pause_classifier import classify_pause
from utils.reentry_detector import detect_reentry

def parse_log(log_text: str):
    """Parse pseudo conversation log"""
    turns = []
    for line in log_text.strip().split('\n'):
        if line.startswith('[User]'):
            turns.append({'role': 'user', 'content': line[7:], 'timestamp': datetime.now().isoformat()})
        elif line.startswith('[Bot]'):
            turns.append({'role': 'bot', 'content': line[6:], 'timestamp': datetime.now().isoformat()})
    return turns

def analyze_trace(turns):
    """Main PLD structure analysis logic"""
    analyzed = []
    past_segments = []
    
    for i, turn in enumerate(turns):
        if turn['role'] == 'user':
            # Pause analysis (assuming time gap with previous bot message)
            pause_result = classify_pause(turn['content']) if i > 0 else None
            
            # Reentry analysis
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
    """Generate Markdown and JSON outputs"""
    # Markdown generation
    md_lines = ["# PLD Trace Analysis", "```mermaid\ngraph TD"]
    for turn in analyzed_data:
        if turn['role'] == 'user':
            md_lines.append(f"    U{len(md_lines)}[\"{turn['content']}\"]")
            if turn.get('pld_analysis'):
                pause = turn['pld_analysis']['pause']
                if pause:
                    md_lines.append(f"    style U{len(md_lines)-1} stroke:#f00,stroke-width:2px")
    
    md_lines.append("```\n\n## Pause/Reentry Tags")
    for turn in analyzed_data:
        if turn.get('pld_analysis'):
            md_lines.append(f"- **{turn['timestamp']}** [User] {turn['content']}")
            if turn['pld_analysis']['pause']:
                md_lines.append(f"  - ⏸️ {turn['pld_analysis']['pause']['classification']}")
                md_lines.append(f"  - 💬 {turn['pld_analysis']['pause']['reason']}")
            if turn['pld_analysis']['reentry']['is_reentry']:
                md_lines.append(f"  - 🔄 Reentry: {turn['pld_analysis']['reentry']['matching_segment']}")
    
    with open('pld_trace_output.md', 'w') as f:
        f.write('\n'.join(md_lines))
    
    # JSON output
    with open('pld_trace_output.json', 'w') as f:
        json.dump(analyzed_data, f, indent=2)

if __name__ == "__main__":
    # Read sample log
    with open('input_trace.txt') as f:
        log_text = f.read()
    
    turns = parse_log(log_text)
    analyzed = analyze_trace(turns)
    save_outputs(analyzed)
    print("✅ Analysis completed. Check pld_trace_output.* files")
