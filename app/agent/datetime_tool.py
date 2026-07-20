from datetime import datetime

def current_datetime():
    """Fetches system operational time directly."""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
