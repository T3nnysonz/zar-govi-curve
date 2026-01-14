from datetime import date
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.daycount import year_fraction
import src.curve

def generate_cashflows(settle_date, mature_date, coupon_rate, coupon_freq = 2, face_value = 100): # The accepted standard is apparently to record cashflows as (date, cashflow)    
    cashflows = []
    
    if(coupon_rate == 0):
        #if(initial_payments):
        #    cashflows.append((settle_date, -face_value))
        cashflows.append((mature_date, face_value))
        return cashflows;
    else:
    
        working_date = mature_date
    
        while(working_date>settle_date):
            coupon_payment = round(face_value*(coupon_rate/coupon_freq), 5)
            cashflows.append((working_date, coupon_payment))
            working_date = (pd.Timestamp(working_date) - pd.DateOffset(months=(12//coupon_freq))).date()
    
        #accrued_period = (settle_date-working_date).days
        #accrued_interest = face_value*(accrued_period/365.0)*coupon_rate
    
        #if(initial_payments):
        #    cashflows.append((settle_date, -(face_value+accrued_interest)))
        cashflows.append((mature_date, face_value))
    
        return sorted(cashflows);

def price_from_curve(settle_date, cashflows, discount_curve):
    pv = 0
    for date, amount in cashflows:
        time = year_fraction(settle_date, date)
        df = discount_curve.calcDF(time)
        pv += amount*df
    return pv;