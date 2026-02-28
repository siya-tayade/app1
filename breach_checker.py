import json
import random

# Read the mock database into memory
import os
import io

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'mock_breaches.json')

def load_breaches():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

def check(email):
    """
    Checks if an email exists in the mock breach dataset.
    Returns status and list of breaches.
    """
    if not email:
        return {"status": "error", "message": "Email is required.", "breaches": []}
        
    breaches_data = load_breaches()
    email_lower = email.lower()
    
    found_breaches = []
    
    for entry in breaches_data:
        if email_lower in entry.get("emails", []):
            found_breaches.append({
                "breach_name": entry["name"],
                "date": entry["date"],
                "data_compromised": entry["data_compromised"],
                "description": entry["description"]
            })
            
    if found_breaches:
        return {
            "status": "breached",
            "message": f"Oh no! We found {len(found_breaches)} breach(es) associated with this email.",
            "breaches": found_breaches
        }
    else:
        return {
            "status": "safe",
            "message": "Good news! No breaches found for this email address.",
            "breaches": []
        }
