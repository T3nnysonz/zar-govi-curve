from datetime import date
import pandas as pd

def generate_cashflows(settle_date, mature_date, coupon_freq, coupon_rate, face_value = 100): # The accepted standard is apparently to record cashflows as (date, cashflow)
    cashflows = []
    
    working_date = mature_date
    
    while(working_date>settle_date):
        working_date = (pd.Timestamp(working_date) - pd.DateOffset(months=(12//coupon_freq))).date()
        coupon_payment = round(face_value*(coupon_rate/coupon_freq), 5)
        cashflows.append((working_date, coupon_payment))
    
    cashflows.append((mature_date, face_value))
    
    return sorted(cashflows);

def price_from_curve():
    return 0;