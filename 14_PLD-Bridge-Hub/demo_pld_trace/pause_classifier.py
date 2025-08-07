# demo_pld_trace/utils/pause_classifier.py (simplified)
def classify_pause(text: str):
    """Simplified pause classifier"""
    if "wait" in text.lower():
        return {
            'classification': '⏸️ UI Friction',
            'reason': 'User cannot find UI element'
        }
    elif "never mind" in text.lower():
        return {
            'classification': '⏸️ Repair',
            'reason': 'User is returning to previous intent'
        }
    return None
