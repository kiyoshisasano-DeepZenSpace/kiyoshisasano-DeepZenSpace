import re
def detect_reentry(past_segments, current_input):
    """Simplified reentry detection"""
    t = (current_input or "").lower()
    if not past_segments:
        return {'is_reentry': False, 'reason': '', 'matching_segment': ''}
    if re.search(r"\b(never\s+mind|go\s+back|previous)\b", t, re.I):
        return {'is_reentry': True,'reason': 'User is resuming previous intent','matching_segment': past_segments[-1]}
    return {'is_reentry': False, 'reason': '', 'matching_segment': ''}
