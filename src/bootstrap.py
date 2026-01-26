from src.bonds import generate_cashflows
from src.bonds import dirty_price
import pandas as pd
from src.daycount import year_fraction
from src.curve import DiscountCurve
import numpy as np

def bootstrap_govi_curve(bonds, conventions = None, bounds = None):
        
    # Find the earliest settlement date as the reference point
    reference_date = min([b['settlement_date'] for b in bonds])
    
    # Sort bonds by maturity date
    sorted_bonds = sorted(bonds, key=lambda b: b['mature_date'])
    
    known_dfs = [(0, 1)]  # t=0, DF=1 at reference date
    known_rates = []
    conventions = getConventions(conventions)
    
    day_count = conventions["day_count"]
    default_freq = conventions["coupon_frequency"]
    face_value = conventions["face_value"]
    accrue_method = conventions["accrued_method"]
    interpolation_method = conventions["interpolation_method"]
    
    df = DiscountCurve(known_dfs, interpolation=interpolation_method, bounds=bounds)
    
    for bond in sorted_bonds:
        mature_date = bond["mature_date"]
        coupon_rate = bond["coupon_rate"]
        clean_price = bond["clean_price"]
        settlement_date = bond["settlement_date"]
        
        # Allow per-bond frequency override
        freq = bond.get("coupon_frequency", default_freq)
        
        # Generate cashflows with correct frequency
        cashflows = generate_cashflows(settlement_date, mature_date, coupon_rate, coupon_freq=freq)
        
        # Find previous and next coupon dates
        previous_coupon = mature_date
        while previous_coupon > settlement_date:
            previous_coupon = (pd.Timestamp(previous_coupon) - pd.DateOffset(months=12//freq)).date()
        next_coupon = (pd.Timestamp(previous_coupon) + pd.DateOffset(months=12//freq)).date()
        
        # Calculate dirty price
        dirtyPrice = dirty_price(clean_price, settlement_date, previous_coupon, next_coupon, 
                                coupon_rate, face_value, coupon_freq=freq, method=accrue_method)
        
        # Time from reference date to settlement date
        t_settle = year_fraction(reference_date, settlement_date, day_count)
        df_settle = df.calcDF(t_settle)
        
        # KEY CHANGE: Use interpolation for ALL cashflows except the final one
        known = 0
        final_cashflow = None
        
        for i, (date, flow) in enumerate(cashflows):
            t_cf = year_fraction(reference_date, date, day_count)
            
            if i == len(cashflows) - 1:
                # This is the final cashflow - we'll bootstrap this
                final_cashflow = (date, flow, t_cf)
            else:
                # For all intermediate cashflows, use interpolated DF
                known += flow * df.calcDF(t_cf)
        
        if final_cashflow is not None:
            date1, final_payment, t_final = final_cashflow
            
            # Check if we already have this maturity (avoid duplicates)
            if t_final in [t for t, _ in known_dfs]:
                print(f"Skipping duplicate maturity at t={t_final:.4f}")
                continue
            
            # Bootstrap the new DF
            new_DF = (dirtyPrice * df_settle - known) / final_payment
            
            # Validate the new DF is reasonable
            if new_DF <= 0 or new_DF > 1.02:
                print(f"Warning: Unusual DF={new_DF:.6f} for bond maturing {mature_date}")
                print(f"  Dirty price: {dirtyPrice:.4f}, Known PV: {known:.4f}, Final payment: {final_payment:.4f}")
                # You can choose to skip or continue here
            
            known_dfs.append((t_final, new_DF))
            df.update_data(known_dfs)
            
            # Use the bond's frequency for rate calculation
            known_rates.append((t_final, df.rate_from_df(t_final, freq)))
        else:
            print(f"No cashflows for bond maturing {mature_date}")
    
    return known_dfs, [reference_date] + [cf[0] for cf in sorted(known_dfs)[1:]], known_rates
    
    bonds = sorted(bonds, key= lambda b: b['settlement_date'])
    dates = [(bonds[0]["settlement_date"])]
    sorted_bonds = sorted(bonds, key= lambda b: b['mature_date']) ## Sorts bonds by maturity date
    
    known_dfs = [(0,1)] # Being that holds year fractions
    known_rates = []
    conventions = getConventions(conventions); # Method built at the bottom of this file
    
    day_count = conventions["day_count"] # Extracting convention data
    freq = conventions["coupon_frequency"]
    face_value = conventions["face_value"]
    accrue_method = conventions["accrued_method"]
    interpolation_method = conventions["interpolation_method"]
    
    df = DiscountCurve(known_dfs, interpolation=interpolation_method, bounds=bounds)
    
    for bond in sorted_bonds: # Go through the bonds from shortest to longest
        mature_date = bond["mature_date"] # Extracting bond data
        coupon_rate = bond["coupon_rate"]
        clean_price = bond["clean_price"]
        settlement_date = bond["settlement_date"]#
        cashflows = generate_cashflows(settlement_date, mature_date, coupon_rate, coupon_freq=freq)  # Generates cashflows  
        previous_coupon = mature_date # Temporary
        while(previous_coupon>settlement_date): # Loop moves back in time at regular intervals until previous coupon falls before sttlement date
            previous_coupon = (pd.Timestamp(previous_coupon) - pd.DateOffset(months=12//freq)).date()
        next_coupon = (pd.Timestamp(previous_coupon) + pd.DateOffset(months=12//freq)).date()    
        known = 0
        unknown_cashflows = [] # Where final cashflows of the bond being bootstrapped    
        dirtyPrice = dirty_price(clean_price, settlement_date, previous_coupon, next_coupon, coupon_rate, face_value, coupon_freq=freq, method=accrue_method)
        # Above uses dirty price = clean price + accrued interest    
        
        for i, (date, flow) in enumerate(cashflows):
            t_cf = year_fraction(dates[0], date, day_count)
            
            if i == len(cashflows) - 1:
                # This is the final cashflow - we'll bootstrap this
                unknown_cashflows.append((date, flow, t_cf))
            else:
                # For all intermediate cashflows, use interpolated DF
                known += flow * df.calcDF(t_cf)
                
        if(len(unknown_cashflows)==1): # We can only work with 1 unknown which is what this checks for
            date1, final_payment, t_cf = unknown_cashflows[0] # Extracts data from unknown cashflows
            year_frac = year_fraction(dates[0], date1, day_count)
            new_DF = df.calcDF(year_fraction(dates[0], settlement_date, day_count))*(dirtyPrice-known)/final_payment # Solves for the desired Discount Factor
            known_dfs.append((year_frac, new_DF))
            df.update_data(known_dfs) # Updates Discount Curve
            known_rates.append((year_frac, df.rate_from_df(year_frac, freq)))
            dates.append(date1)
        else:
            print("Unable to calculate df's") # Handles exceptions
            print(unknown_cashflows)
    return known_dfs, dates, known_rates;

def getConventions(conventions):
    if(conventions is None):
        conventions = {
            'day_count': 'ACT/365F',
            'coupon_frequency': 2,
            'interpolation_method': 'log_linear',
            'face_value': 100,
            'accrued_method': 'linear'
        }
    return conventions