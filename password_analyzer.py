from zxcvbn import zxcvbn
import math

def calculate_entropy(password: str) -> float:
    """Calculates password entropy based on length and character set."""
    if not password or not isinstance(password, str):
        return 0.0
        
    charset_size = 0
    if any(c.islower() for c in password): charset_size += 26
    if any(c.isupper() for c in password): charset_size += 26
    if any(c.isdigit() for c in password): charset_size += 10
    if any(not c.isalnum() for c in password): charset_size += 32
    
    if charset_size == 0 or len(password) == 0:
        return 0.0
    return float(len(password) * math.log2(charset_size))

def analyze(password):
    """
    Analyzes password strength using zxcvbn logic.
    Returns score, estimated crack time, and feedback details.
    """
    if not password:
        return {
            "score": 0,
            "entropy": 0,
            "crack_time": "Instant",
            "feedback": {"warning": "Empty password", "suggestions": ["Enter a password"]}
        }
        
    result = zxcvbn(password)
    entropy = calculate_entropy(password)
    
    # Map zxcvbn score (0-4) to a 0-100 scale for UI
    score_mapping = {0: 10, 1: 30, 2: 60, 3: 85, 4: 100}
    ui_score = score_mapping.get(result['score'], 0)
    
    # Adjust score based on length for better visual feedback
    if len(password) < 8:
        ui_score = min(ui_score, 40)
    elif len(password) >= 12 and ui_score < 70:
        ui_score = 70
        
    crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
    
    return {
        "score": ui_score,
        "entropy": round(float(entropy), 2),
        "crack_time": crack_time,
        "feedback": {
            "warning": result['feedback']['warning'],
            "suggestions": result['feedback']['suggestions']
        }
    }
