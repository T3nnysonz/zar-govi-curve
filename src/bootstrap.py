from src.bonds import generate_cashflows
from src.bonds import dirty_price
import pandas as pd
from src.daycount import year_fraction
from src.curve import DiscountCurve

def bootstrap_govi_curve(bonds, settlement_date, conventions = None, bounds = None):
    
    sorted_bonds = sorted(bonds, key= lambda b: b['mature_date']) ## Sorts bonds by maturity date
    
    known_dfs = [(0,1)] # Being that known_dfs holds year fractions
    dates = [settlement_date]
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
        cashflows = generate_cashflows(settlement_date, mature_date, coupon_rate, coupon_freq=freq)  # Generates cashflows  
        previous_coupon = mature_date # Temporary
        while(previous_coupon>settlement_date): # Loop moves back in time at regular intervals until previous coupon falls before sttlement date
            previous_coupon = (pd.Timestamp(previous_coupon) - pd.DateOffset(months=12//freq)).date()
        next_coupon = (pd.Timestamp(previous_coupon) + pd.DateOffset(months=12//freq)).date()    
        known = 0
        unknown_cashflows = [] # Where final cashflows of the bond being bootstrapped    
        dirtyPrice = dirty_price(clean_price, settlement_date, previous_coupon, next_coupon, coupon_rate, face_value, coupon_freq=freq, method=accrue_method)
        # Above uses dirty price = clean price + accrued interest    
        
        for date, flow in cashflows:           
            year_frac = year_fraction(settlement_date, date, day_count) # How long has passed since settlement date
            if(year_frac<=max([time for time, _ in known_dfs])):
                known += flow * df.calcDF(year_frac) # Adds all calculable data about current bond to known
            else:
                unknown_cashflows.append((date, flow)) # Adds the rest of the data to unknown cashflows
                
        if(len(unknown_cashflows)==1): # We can only work with 1 unknown which is what this checks for
            
            date1, final_payment = unknown_cashflows[0] # Extracts data from unknown cashflows
            new_DF = (dirtyPrice-known)/final_payment # Solves for the desired Discount Factor
            known_dfs.append((year_frac, new_DF))
            df.update_data(known_dfs) # Updates Discount Curve
            dates.append(date1)
        else:
            print("Unable to calculate df's") # Handles exceptions
    return known_dfs, dates;

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