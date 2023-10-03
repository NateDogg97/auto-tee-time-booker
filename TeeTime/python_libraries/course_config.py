from datetime import datetime

def get_multiple_courses():
    if datetime.today().weekday() == 6:  # Sunday is represented by 6
        return 5
    else:
        return 1
