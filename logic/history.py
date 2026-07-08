from datetime import datetime

history = []

def log_event(event, details=""):
    history.append({
        "timestamp": datetime.now().strftime("%I:%M %p"),
        "event": event,
        "details": details
    })