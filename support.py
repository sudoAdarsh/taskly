import re
from datetime import datetime, timedelta



def parse_due_date(date: str):
    # default 1 day
    if date is None:
        return datetime.now() + timedelta(days=1)
    # days from now
    if date.isdigit():
        return datetime.now() + timedelta(int(date))
    # Custom format (3d, 1w, or 11h)
    match = re.fullmatch(r"(\d+)([dhw])", date)
    if match:
        amount, unit = match.groups()
        amount = int(amount)
        if unit == "d":
            return datetime.now() + timedelta(days=amount)
        if unit == "h":
            return datetime.now() + timedelta(hours=amount)
        if unit == "w":
            return datetime.now() + timedelta(weeks=amount)
    # Full date
    try:
        date_only = datetime.strptime(date, "%d-%m-%Y")
        return date_only
    except ValueError:
        raise ValueError("\nDue date: N (days), Nd/Nw, YYYY-MM-DD or (default: +1 day)")
