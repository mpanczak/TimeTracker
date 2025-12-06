import json
import os
from datetime import datetime, timedelta

DATA_FILE = "data.json"

def load_data():
    """Loads the data, handling daily resets and history."""
    today_str = str(datetime.now().date())
    
    default_data = {
        "current_date": today_str,
        "work": 0.0,
        "personal": 0.0,
        "history": {}
    }

    if not os.path.exists(DATA_FILE):
        return default_data
    
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            
        # Check if we need to migrate old format (simple dict) to new format
        if "history" not in data:
            # Migration: Treat old data as "today" if date matches, else discard or archive?
            # Let's just reset to default structure to avoid complexity with incompatible old data
            # unless we really want to keep it. User didn't ask to keep old V1/V2 data specifically.
            # But let's try to be nice.
            old_date = data.get("last_updated")
            if old_date == today_str:
                return {
                    "current_date": today_str,
                    "work": data.get("work", 0.0),
                    "personal": data.get("personal", 0.0),
                    "history": {}
                }
            else:
                # Old data is from past, just start fresh
                return default_data

        # Check for day change
        saved_date = data.get("current_date")
        if saved_date != today_str:
            # It's a new day! Archive yesterday's data.
            # Only archive if there was some activity
            if data["work"] > 0 or data["personal"] > 0:
                data["history"][saved_date] = {
                    "work": data["work"],
                    "personal": data["personal"]
                }
            
            # Prune history to last 5 days
            sorted_dates = sorted(data["history"].keys(), reverse=True)
            if len(sorted_dates) > 5:
                for date_to_remove in sorted_dates[5:]:
                    del data["history"][date_to_remove]

            # Reset today's counters
            data["current_date"] = today_str
            data["work"] = 0.0
            data["personal"] = 0.0
            
            # Save the reset state immediately
            save_full_data(data)
             
        return data
    except (json.JSONDecodeError, IOError):
        return default_data

def save_data(work_time, personal_time):
    """Saves the current accumulated time data."""
    # We need to load first to preserve history, or we keep the full data object in memory in the app.
    # Better to have the app pass the full object or just update specific fields?
    # For simplicity, let's assume the app holds the state and we just save what we have.
    # BUT, this function signature was `save_data(work, personal)`. 
    # To avoid race conditions or overwriting history, we should probably load, update, save.
    # OR, we change the signature to accept the full data dict.
    # Let's change the signature in a new function `save_full_data` and keep `save_data` as a wrapper
    # that might be inefficient but safe, OR better:
    # The Monitor/App should hold the authoritative data object.
    pass 

def save_full_data(data):
    """Saves the full data dictionary."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")

def clear_today():
    """Resets today's counters."""
    data = load_data()
    data["work"] = 0.0
    data["personal"] = 0.0
    save_full_data(data)
    return data
