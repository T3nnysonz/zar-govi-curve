import numpy as np
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.daycount import year_fraction

def generate_cashflows(settle_date, mature_date, coupon_rate, coupon_freq = 2, face_value = 100): # The accepted standard is apparently to record cashflows as (date, cashflow)    
    cashflows = []
    
    if(coupon_rate == 0):
        cashflows.append((mature_date, face_value))
        return cashflows;
    elif(settle_date == mature_date):
        return cashflows;
    else:
    
        working_date = mature_date
        cashflows.append((mature_date, round(face_value*(1+coupon_rate/coupon_freq),5)))
        working_date = (pd.Timestamp(working_date) - pd.DateOffset(months=(12//coupon_freq))).date()
    
        while(working_date>settle_date):
            coupon_payment = round(face_value*(coupon_rate/coupon_freq), 5)
            cashflows.append((working_date, coupon_payment))
            working_date = (pd.Timestamp(working_date) - pd.DateOffset(months=(12//coupon_freq))).date()
    
        return sorted(cashflows);

def accrued_interest(settle_date, last_coupon, next_coupon, coupon_rate, face_value = 100, coupon_freq = 2, method = "linear"):
    if(method == "linear"):
        accrued_period = (settle_date-last_coupon).days # How long since last coupon issue.
        full_accrue = (next_coupon-last_coupon).days # Full gap between coupons.
        full_coupon = face_value * (coupon_rate/coupon_freq) # How much a full coupon payout would be.
        fraction = accrued_period/full_accrue # What fraction of the current accruation period has been completed.
        accrued_interest = full_coupon * fraction  # The correct fraction of the accruement of the full coupon.
        
    elif(method == "midpoint"):
        accrued_interest = 0.5 * face_value * coupon_rate * 0.5
        
    elif(method == "none"):
        accrued_interest = 0;
        
    elif(method == "log_linear"):
        accrued_period = (settle_date-last_coupon).days # How long since last coupon issue.
        full_accrue = (next_coupon-last_coupon).days # Full gap between coupons.
        full_coupon = face_value * (coupon_rate/coupon_freq) # How much a full coupon payout would be.
        ln_full_coupon = np.log(full_coupon)
        fraction = accrued_period/full_accrue # What fraction of the current accruation period has been completed.
        ln_accrued_interest = ln_full_coupon * fraction  # The correct fraction of the accruement of the full coupon.
        accrued_interest = np.exp(ln_accrued_interest)
        
    else:
        print("Unknown accruation method: did not accruate")
        accrued_interest = 0;
        
    return accrued_interest;

def dirty_price(clean_price, settle_date, last_coupon, next_coupon, coupon_rate, face_value = 100, coupon_freq = 2, method = "linear"):
    dirty_price = clean_price + accrued_interest(settle_date, last_coupon, next_coupon, coupon_rate, face_value, coupon_freq, method)
    return dirty_price;