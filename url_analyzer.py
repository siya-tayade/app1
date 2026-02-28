import re
import math
from urllib.parse import urlparse

# Suspicious keywords commonly found in phishing URLs
SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'update', 'secure', 'account', 'banking', 'billing', 
    'support', 'admin', 'pay', 'confirm', 'service', 'validation', 'alert',
    'webscr', 'password', 'credential', 'auth'
]

def calculate_entropy(url):
    """Calculates the Shannon entropy of a string."""
    if not url:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(url.count(chr(x))) / len(url)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def analyze(url):
    """
    Analyzes a URL for phishing characteristics.
    Returns a dictionary with score, verdict, and breakdown details.
    """
    if not url.startswith(('http://', 'https://')):
        # For parsing to work well, ensure a scheme exists
        parsed_url = urlparse('http://' + url)
    else:
        parsed_url = urlparse(url)

    domain = parsed_url.netloc.lower()
    path = parsed_url.path.lower()
    full_url_lower = url.lower()

    score = 0
    reasons = []

    # 1. Check for HTTPS
    if url.startswith('https://'):
        reasons.append({"label": "HTTPS Used", "type": "safe", "desc": "Information is encrypted."})
    else:
        score += 20
        reasons.append({"label": "No HTTPS", "type": "danger", "desc": "Connection is not secure (HTTP)."})

    # 2. Check URL Length
    url_length = len(url)
    if url_length > 75:
        score += 15
        reasons.append({"label": "URL Too Long", "type": "warning", "desc": f"Length ({url_length} chars) is suspiciously long."})
    else:
        reasons.append({"label": "Standard Length", "type": "safe", "desc": "URL length is within normal limits."})

    # 3. Check for Suspicious Keywords
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in full_url_lower]
    if found_keywords:
        score += len(found_keywords) * 15 # Add 15 points per keyword
        reasons.append({
            "label": "Suspicious Keywords", 
            "type": "danger", 
            "desc": f"Found deceptive terms: {', '.join(found_keywords)}."
        })
    else:
        reasons.append({"label": "No Phishing Terms", "type": "safe", "desc": "No common deceptive keywords detected."})

    # 4. Check for IP Address instead of Domain
    if re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', domain):
        score += 30
        reasons.append({"label": "IP Address Usage", "type": "danger", "desc": "Domain is an IP address, hiding true origin."})

    # 5. Check Number of Subdomains
    parts = domain.split('.')
    if len(parts) > 3:
        score += 15
        reasons.append({"label": "Excessive Subdomains", "type": "warning", "desc": f"Found {len(parts)} parts in domain."})

    # 6. Check Entropy
    entropy = calculate_entropy(url)
    if entropy > 4.5:
        score += 10
        reasons.append({"label": "High Entropy", "type": "warning", "desc": "URL looks randomly generated (obfuscation attempt)."})
    
    # Cap score at 100
    score = min(100, score)

    # Determine Verdict
    if score < 20:
        verdict = "Safe"
        badge_class = "safe"
    elif score < 60:
        verdict = "Suspicious"
        badge_class = "warning"
    else:
        verdict = "Malicious"
        badge_class = "danger"

    return {
        "risk_score": score,
        "verdict": verdict,
        "badge_class": badge_class,
        "reasons": reasons
    }
