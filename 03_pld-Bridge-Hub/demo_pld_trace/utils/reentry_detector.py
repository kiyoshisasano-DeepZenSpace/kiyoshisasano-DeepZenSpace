# demo_pld_trace/utils/reentry_detector.py (simplified)
def detect_reentry(past_segments, current_input):
    """Simplified reentry detection"""
    for seg in past_segments:
        if any(word in current_input.lower() for word in ["never mind", "go back", "previous"]):
            return {
                'is_reentry': True,
                'reason': 'User is resuming previous intent',
                'matching_segment': seg
            }
    return {'is_reentry': False, 'reason': '', 'matching_segment': ''}
