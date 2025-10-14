import re
def classify_pause(text: str):
    """Simplified pause classifier"""
    t = (text or "")
    if re.search(r"\bwait\b", t, re.I):
        return {'classification': '⏸️ UI Friction','reason': 'User cannot find UI element'}
    if re.search(r"\bnever\s+mind\b", t, re.I):
        return {'classification': '⏸️ Repair','reason': 'User is returning to previous intent'}
    return None
