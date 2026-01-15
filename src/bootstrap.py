from src.bonds import generate_cashflows
from src.bonds import dirty_price
import pandas as pd
from src.daycount import year_fraction
from src.curve import DiscountCurve

def bootstrap_govi_curve(bonds, settlement_date, conventions = None):
    sorted_bonds = sorted(bonds, key= lambda b: b['mature_date'])
    DF_data = [(settlement_date, 1)]
    known_dfs = [(0,1)]
    df = DiscountCurve(known_dfs)
    conventions = getConventions(conventions);
    day_count = conventions["day_count"]
    freq = conventions["coupon_frequency"]
    face_value = conventions["face_value"]
    
    for bond in sorted_bonds:
        known = 0
        mature_date = bond["mature_date"]
        coupon_rate = bond["coupon_rate"]
        clean_price = bond["clean_price"]
        face_value = bond["face_value"]
        cashflows = generate_cashflows(settlement_date, mature_date, coupon_rate, coupon_freq=freq)    
        previous_coupon = mature_date
        while(previous_coupon>settlement_date):
            previous_coupon = (pd.Timestamp(previous_coupon) - pd.DateOffset(months=12//freq)).date()
        next_coupon = (pd.Timestamp(previous_coupon) + pd.DateOffset(months=12//freq)).date()             
        unknown_cashflows = []
        year_frac = 0       
        dirtyPrice = dirty_price(clean_price, settlement_date, previous_coupon, next_coupon, coupon_rate, face_value)
        
        for date, flow in cashflows:           
            year_frac = year_fraction(settlement_date, date, day_count)
            if(year_frac<=max([time for time, _ in known_dfs])):
                known += flow * df.calcDF(year_frac)
            else:
                unknown_cashflows.append((date, flow))
        if(len(unknown_cashflows)==1):
            date1, amount1 = unknown_cashflows[0]
            final_payment = amount1
            new_DF = (dirtyPrice-known)/final_payment
            DF_data.append((date1, new_DF))
            known_dfs.append((year_frac, new_DF))
            df = DiscountCurve(known_dfs)
        else:
            print(len(unknown_cashflows))
            print(unknown_cashflows)
            print("Unable to calculate df's")
            return [];
    return known_dfs;

def getConventions(conventions):
    if conventions is None:
        conventions = {
            'day_count': 'ACT/365F',
            'coupon_frequency': 2,
            'interpolation_method': 'log_linear',
            'face_value': 100,
            'accrued_method': 'linear'
        }
        return conventions