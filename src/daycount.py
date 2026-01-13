import numpy
import datetime

def df_from_rate(rate, t, compounding = True):
    '''
    Description: returns the Discount Factor of a bond given the interest rate and investment period
    
    rate: float, the interest rate of the bond
    t: integer, the number of compounding periods the bond experiences
    compounding: boolean, True if the interest on the bond is compounding and otherwise false
    '''
    if(compounding):
        df = 1/(1+rate)**t
    else:
        df = 1/(1+rate*t)
    return df

def year_fraction(start_date, end_date, day_count="ACT/365F"):

    if day_count == "ACT/365F":
        # Computes the decimal amount of 365 day years between 2 dates
        days = (end_date-start_date).days
        return days/365.0
    elif day_count == "ACT/360":
        # Computes the decimal amount of 360 day years between 2 dates
        days = (end_date-start_date).days
        return days/360.0
    elif day_count == "30/360":
        # Computes the decimal amount of complete 30 day month, 360 day years between 2 dates
        months = numpy.floor(((end_date-start_date).days)/30)
        return months/12.0
    else:
        raise ValueError(f"Unknown day count: {day_count}")