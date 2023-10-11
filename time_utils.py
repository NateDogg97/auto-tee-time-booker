from datetime import datetime, timedelta
import pytz


def day_to_weekday_num(day_name):
    """Converts a day name to its corresponding weekday number."""
    days = ["monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"]
    return days.index(day_name.lower())


def get_target_date_xpath(target_day=None, timezone_str="America/Chicago"):
    local_timezone = pytz.timezone(timezone_str)
    today = datetime.now(local_timezone)

    if target_day:
        # Convert the desired day to its corresponding weekday number
        target_day_num = day_to_weekday_num(target_day)
        days_ahead = (target_day_num - today.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7  # If today is the desired day, move a week ahead
    else:
        days_ahead = 7  # Default behavior

    target_date = today + timedelta(days=days_ahead)
    day = target_date.day
    month = target_date.month - 1  # Adjust month for zero-based index in HTML

    date_xpath = f"//td[@data-month='{month}'][a[text()='{day}']]"
    return date_xpath


def convert_to_24_hour_format(time_str):
    # Converts a time string in the format of 'hh:mm AM/PM' to 24-hour format.
    from datetime import datetime
    return datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')
