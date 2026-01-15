from src.bonds import generate_cashflows
from src.bonds import dirty_price
import pandas as pd
from src.daycount import year_fraction
from src.curve import DiscountCurve

def bootstrap_govi_curve(bonds, settlement_date, conventions = ""):
    sorted_bonds = sorted(bonds, key= lambda b: b['mature_date'])
    DF_data = []
    known_dfs = []
    
    for bond in sorted_bonds:
        known = 0
        mature_date = bond["mature_date"]
        coupon_rate = bond["coupon_rate"]
        clean_price = bond["clean_price"]
        face_value = bond["face_value"]
        cashflows = generate_cashflows(settlement_date, mature_date, coupon_rate, coupon_freq=2)
        #print(cashflows)
        i = len(cashflows)
        last_coupon = (pd.Timestamp(sorted_bonds[0]["mature_date"]) - pd.DateOffset(months=6)).date()
        next_coupon = sorted_bonds[0]["mature_date"]
        unknown_cashflows = []
        year_frac = 0
        count = 0
        
        dirtyPrice = dirty_price(clean_price, settlement_date, last_coupon, next_coupon, coupon_rate, face_value)
        
        for date, flow in cashflows:
            #print("entered loop")
            #print(date)
            #print(i-2)
            #print(known_dfs)
            #print(count<i-2)
            #return 0;
            if(count<i-2):
                year_frac = year_fraction(settlement_date, date)
                df = DiscountCurve(known_dfs)
                known += flow * df.calcDF(year_frac)
                count+=1
            else:
                #print("entered this")
                unknown_cashflows.append((date, flow))
                #print(unknown_cashflows)
        #return 0;
        if(len(unknown_cashflows)==2):
            date1, amount1 = unknown_cashflows[0]
            filler, amount2 = unknown_cashflows[1]
            final_payment = amount1+amount2
            new_DF = (dirtyPrice-known)/final_payment
            DF_data.append((date1, new_DF))
            known_dfs.append((year_frac, new_DF))
            #print("entered 2'nd if")
            #print(known_dfs)
            #print(DF_data)
            #return 0;
        else:
            print(len(unknown_cashflows))
            print(unknown_cashflows)
            print("Unable to calculate df's")
            return [];
    return known_dfs;