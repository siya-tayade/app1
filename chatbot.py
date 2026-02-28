import random
import time

def respond(message):
    """
    A mock cybersecurity AI chatbot.
    Returns a predefined response based on keywords.
    """
    msg_lower = message.lower()
    
    delay = random.uniform(0.5, 1.5)
    time.sleep(delay) # Simulate thinking
    
    import re
    
    # Prioritize specific commands/topics
    if any(keyword in msg_lower for keyword in ['what can you do', 'features', 'help', 'tools']):
        return {"response": "I am connected to the Cyber Exposure Intelligence Platform. I can provide cybersecurity advice, and you can also use the tools on the left to: \n1. Analyze URLs for phishing \n2. Test password strength \n3. Scan texts/emails for scams \n4. Check if your email is in a data breach."}
        
    if any(keyword in msg_lower for keyword in ['who made you', 'creator', 'science expo', 'project']):
        return {"response": "I was developed as part of a demonstration for the Science Expo, designed to analyze cyber exposure and educate users on security concepts."}

    if any(keyword in msg_lower for keyword in ['phishing', 'email', 'scam']):
        return {"response": "Phishing involves sending fraudulent communications that appear to come from a reputable source. **Always verify the sender's address** and never click on suspicious links. You can use my 'Phishing Detector' tool on the left to scan suspicious messages."}
        
    if any(keyword in msg_lower for keyword in ['password', 'secure', 'strong']):
        return {"response": "A strong password should be at least 12 characters long, mixing uppercase, lowercase, numbers, and symbols. I recommend using a **Passphrase** (e.g., 'CorrectHorseBatteryStaple') rather than random complex strings, and always use a Password Manager. Try my 'Password Strength' tool to test yours."}
        
    if any(keyword in msg_lower for keyword in ['breach', 'hack', 'stolen']):
        return {"response": "If you suspect your data has been breached, immediately change your passwords on affected sites and any other site where you reused that password. Enable **Two-Factor Authentication (2FA)** everywhere possible. You can check if your email is in known breaches using the 'Breach Checker' tool."}
        
    if any(keyword in msg_lower for keyword in ['malware', 'virus', 'ransomware']):
        return {"response": "Malware is malicious software designed to harm or exploit your device. Ransomware is a specific type that encrypts your files until a ransom is paid. Always keep your OS updated, avoid downloading software from untrusted sources, and use reputable Antivirus software."}

    if any(keyword in msg_lower for keyword in ['vpn', 'public wifi', 'network']):
        return {"response": "When using Public Wi-Fi, your data can be intercepted by attackers on the same network. A **Virtual Private Network (VPN)** encrypts your internet traffic, keeping it safe from prying eyes. Avoid logging into sensitive accounts on public networks without a VPN."}

    if any(keyword in msg_lower for keyword in ['cyber security', 'cybersecurity', 'security', 'cyber', 'infosec']):
        return {"response": "Cybersecurity is the practice of defending computers, servers, mobile devices, electronic systems, networks, and data from malicious attacks. It's essential in today's digital world to protect your personal and financial information."}

    # Only match greetings if they are distinct words (to avoid matching 'hi' inside 'this' or 'phishing', or triggering on "hi i need help with cybersecurity")
    words = re.sub(r'[^\w\s]', '', msg_lower).split()
    if sum(1 for w in words if w in ['hello', 'hi', 'hey', 'greetings']) > 0 and len(words) <= 3:
        return {"response": "Greetings! I am Sentinel AI, your personal cybersecurity assistant. How can I help you secure your digital life today?"}

    # Default fallback
    responses = [
        "That's an interesting question. In cybersecurity, we always recommend adopting a 'Zero Trust' mindset. Never trust, always verify.",
        "I'm an AI specialized in cybersecurity. Can you rephrase that in the context of digital security, threats, or privacy?",
        "Security is an ongoing process. Always ensure your software is updated and you are using Multi-Factor Authentication (MFA).",
        "While I cannot perform a live scan right now, I highly recommend using the built-in heuristic analysis tools in this platform for URLs and Passwords."
    ]
    
    return {"response": random.choice(responses)}
