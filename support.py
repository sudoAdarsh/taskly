import re
from datetime import datetime, timedelta



def parse_due_date(date: str):
    now = datetime.now()

    # default 1 day
    if date is None:
        return now + timedelta(days=1)
    # days from now
    if date.isdigit():
        return now + timedelta(int(date))
    # Custom format (3d, 1w, or 11h)
    match = re.fullmatch(r"(\d+)([dhw])", date)
    if match:
        amount, unit = match.groups()
        amount = int(amount)
        if unit == "d":
            return now + timedelta(days=amount)
        if unit == "h":
            return now + timedelta(hours=amount)
        if unit == "w":
            return now + timedelta(weeks=amount)
    # Full date
    try:
        date_only = datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        raise ValueError("\nDue date: N (days), Nd/Nw, DD-MM-YYY or (default: +1 day)")
    else:
        if date_only <= now:
            raise ValueError("Due date must be in the future.")
        return date_only
