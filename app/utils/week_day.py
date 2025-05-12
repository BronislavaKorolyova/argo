from datetime import datetime

def get_day_of_week(date_string: str) -> str:
    """
    Get the day of the week from a date string in YYYY-MM-DD format.
    """
    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        return date_object.strftime("%A")
    except ValueError:
        return "Invalid date format"
