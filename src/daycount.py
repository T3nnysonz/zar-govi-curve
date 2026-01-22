import numpy

def year_fraction(start_date, end_date, day_count="ACT/365F"):#
    '''
    Description: returns amount of time between the start and end date as a float number of years
    
    start_date: Start date in standard datetime.date() format
    end_date: End date in standard datetime.date() format
    day_count: Convention used for measuring year length and duration between 2 dates
    '''

    if day_count == "ACT/365F":
        # Computes the decimal amount of 365 day years between 2 dates
        days = (end_date-start_date).days
        return round(days/365.0, 5)
    elif day_count == "ACT/360":
        # Computes the decimal amount of 360 day years between 2 dates
        days = (end_date-start_date).days
        return round(days/360.0, 5)
    elif day_count == "30/360":
        # Computes the decimal amount of complete 30 day month, 360 day years between 2 dates
        months = numpy.floor(((end_date-start_date).days)/30)
        return round(months/12.0, 5)
    else:
        raise ValueError(f"Unknown day count: {day_count}")