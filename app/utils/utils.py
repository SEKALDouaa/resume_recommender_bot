from datetime import datetime

def calculate_experience_years(start_month, start_year, end_month, end_year):
    try:
        start = datetime.strptime(f"{start_month or 'January'} {start_year}", "%B %Y")
        if end_year == "Present":
            end = datetime.now()
        else:
            end = datetime.strptime(f"{end_month or 'January'} {end_year}", "%B %Y")
        delta = end - start
        return round(delta.days / 365.25, 1)
    except Exception:
        return None
