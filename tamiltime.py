import time

class TamilTime:
    @staticmethod
    def get_tamil_time():
        local_time = time.localtime()
        year = local_time.tm_year
        month = local_time.tm_mon
        month_day = local_time.tm_mday
        week_day = local_time.tm_wday
        hour, minute, second = local_time.tm_hour, local_time.tm_min, local_time.tm_sec

        return TamilTime.format_time(year, month, month_day, week_day, hour, minute, second)

    @staticmethod
    def format_time(year, month, day, week_day, hour, minute, second):
        tamil_weekdays = ["ஞாயிறு", "திங்கள்", "செவ்வாய்", "புதன்", "வியாழன்", "வெள்ளி", "சனி"]
        tamil_months = [
            "", "தை", "மாசி", "பங்குனி", "சித்திரை", "வைகாசி", 
            "ஆனி", "ஆடி", "ஆவணி", "புரட்டாசி", "ஐப்பசி", 
            "கார்த்திகை", "மார்கழி"
        ]
        time_periods = [
            "நள்ளிரவு", "அதிகாலை", "காலை", "மத்தியானம்", "மாலை", "இரவு"
        ]

        # Determine the time period
        if hour < 3:
            prefix = time_periods[0]
        elif hour < 6:
            prefix = time_periods[1]
        elif hour < 12:
            prefix = time_periods[2]
        elif hour < 15:
            prefix = time_periods[3]
        elif hour < 19:
            prefix = time_periods[4]
        else:
            prefix = time_periods[5]

        time_str = f"{prefix} {hour}:{minute:02}:{second:02}"
        date_str = f"{tamil_months[month]} {day}, {year} - {tamil_weekdays[week_day]}"
        return f"{time_str}\n{date_str}"

