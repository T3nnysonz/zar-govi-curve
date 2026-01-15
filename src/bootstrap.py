from src.bonds import generate_cashflows
from src.bonds import dirty_price
import pandas as pd
from src.daycount import year_fraction
from src.curve import DiscountCurve

def bootstrap_govi_curve(bonds, settlement_date, conventions = ""):
    sorted_bonds = sorted(bonds, key= lambda b: b['mature_date'])
    DF_data = []
    
    for bond in sorted_bonds:
        known = 0
        mature_date = bond["mature_date"]
        coupon_rate = bond["coupon_rate"]
        clean_price = bond["clean_price"]
        face_value = bond["face_value"]
        cashflows = generate_cashflows(settlement_date, mature_date, coupon_rate, coupon_freq=2)
        i = len(cashflows)
        last_coupon = (pd.Timestamp(sorted_bonds[0]["mature_date"]) - pd.DateOffset(months=6)).date()
        next_coupon = sorted_bonds[0]["mature_date"]
        known_dfs = []
        unknown_cashflows = []
        
        dirtyPrice = dirty_price(clean_price, settlement_date, last_coupon, next_coupon, coupon_rate, face_value)
        
        for date, flow in cashflows:
            count = 0
            if(count<i-2):
                year_frac = year_fraction(settlement_date, date)
                df = DiscountCurve([known_dfs])
                known += flow * df.calcDF(date)
                i+=1
            else:
                unknown_cashflows.append((date, flow))
        if(len(unknown_cashflows)==2):
            date1, amount1 = unknown_cashflows[0]
            filler, amount2 = unknown_cashflows[1]
            final_payment = amount1+amount2
            new_DF = (dirtyPrice-known)/final_payment
            DF_data.append(date1, new_DF)
            known_dfs.append((year_frac, new_DF))
        else:
            print("Unable to calculate df's")
            return [];
    return DF_data;