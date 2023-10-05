from datetime import datetime

def convert_to_24_hour_format(time_str):
    # Converts a time string in the format of 'hh:mm AM/PM' to 24-hour format. 
    return datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')
