PHISHING_PHRASES = [
    'urgent', 'immediate action required', 'verify your account',
    'click here', 'click the link', 'update your account',
    'suspended account', 'billing error', 'payment declined',
    'login immediately', 'confirm your identity', 'dear customer',
    'dear user', 'attention required', 'validate your details',
    'kindly open the attached', 'won a prize', 'lottery winner'
]

def check_urgency(text_lower):
    urgency_words = ['urgent', 'immediately', 'now', 'action required', 'asap', 'within 24 hours', 'alert']
    return any(word in text_lower for word in urgency_words)

def check_financial(text_lower):
    financial_words = ['bank', 'credit card', 'payment', 'transfer', 'invoice', 'billing', 'charge', 'money']
    return any(word in text_lower for word in financial_words)

def check_links(text_lower):
    link_words = ['click here', 'verify', 'update', 'link below', 'login', 'portal', 'http', 'www']
    return any(word in text_lower for word in link_words)

def check_generic_greeting(text_lower):
    greetings = ['dear customer', 'dear user', 'dear member', 'sir/madam', 'attention account holder']
    return any(greetings in text_lower for greetings in greetings)

def analyze(text):
    """
    Heuristic analyzer for phishing emails or text messages.
    """
    if not text:
        return {"probability": 0, "verdict": "Safe", "reasons": []}
        
    text_lower = text.lower()
    score = 0
    reasons = []
    
    # Phase 1: Check known exact suspicious phrases
    found_phrases = []
    for phrase in PHISHING_PHRASES:
        if phrase in text_lower:
            found_phrases.append(phrase)
            score += 15
            
    if found_phrases:
        reasons.append({"label": "Suspicious Phrasing", "desc": f"Contains deceptive typical phrasing: '{', '.join(found_phrases)}'"})

    # Phase 2: Check Heuristics
    if check_urgency(text_lower):
        score += 25
        reasons.append({"label": "Urgency Tone", "desc": "Message tries to create a sense of panic or immediacy."})
        
    if check_financial(text_lower):
        score += 15
        reasons.append({"label": "Financial Relevance", "desc": "Message discusses money, billing, or banking."})
        
    if check_links(text_lower):
        score += 20
        reasons.append({"label": "Call to Action (Link)", "desc": "Message heavily pushes the user to click a link or log in."})
        
    if check_generic_greeting(text_lower):
        score += 10
        reasons.append({"label": "Generic Greeting", "desc": "Legitimate companies usually address you by name."})

    score = min(score, 100)
    
    if score < 30:
        verdict = "Likely Safe"
        badge_class = "safe"
    elif score < 65:
        verdict = "Suspicious"
        badge_class = "warning"
    else:
        verdict = "High Risk Phishing"
        badge_class = "danger"
        
    if score == 0:
        reasons.append({"label": "No Threats Found", "desc": "Text appears normal without typical phishing characteristics."})
        
    return {
        "probability": score,
        "verdict": verdict,
        "badge_class": badge_class,
        "reasons": reasons
    }
