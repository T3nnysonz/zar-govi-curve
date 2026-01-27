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
        rate = bond["rate"]
        clean_price = bond["clean_price"]
        settlement_date = bond["settlement_date"]
        type = bond["type"]
    
        if(type == "FRA"): 
            new_DF, t = bootstrapFRA(reference_date, settlement_date, mature_date, day_count, df, rate)
            known_dfs.append((t, new_DF))
            df.update_data(known_dfs)
            known_rates.append((t, df.rate_from_df(t)))
        elif(type == "swap"): # Not working
            df_settle = df.calcDF(year_fraction(reference_date, settlement_date, day_count))
            sum = 0
            dates = generate_swap_fixed_leg(settlement_date, mature_date)
            t = year_fraction(settlement_date,mature_date,day_count)
            
            for i, date in enumerate(dates):
                time = year_fraction(settlement_date, date)
                d = df.calcDF(time)
                
                if i==0:
                    deltaT = year_fraction(settlement_date,date)
                else:
                    deltaT = year_fraction(dates[i-1],dates[i])
                if date<mature_date:
                    sum += deltaT * d
                else:
                    finalT = deltaT
                
            new_DF = (df_settle-rate*sum)/(1+rate*finalT)
            
            known_dfs.append((t, new_DF))
            df.update_data(known_dfs)
            known_rates.append((t, df.rate_from_df(t)))
        else:    
            freq = default_freq
            
            # Generate cashflows with correct frequency
            cashflows = generate_cashflows(settlement_date, mature_date, rate, coupon_freq=freq)
            
            # Find previous and next coupon dates
            previous_coupon = mature_date
            while previous_coupon > settlement_date:
                previous_coupon = (pd.Timestamp(previous_coupon) - pd.DateOffset(months=12//freq)).date()
            next_coupon = (pd.Timestamp(previous_coupon) + pd.DateOffset(months=12//freq)).date()
            
            # Calculate dirty price
            dirtyPrice = dirty_price(clean_price, settlement_date, previous_coupon, next_coupon, 
                                    rate, face_value, coupon_freq=freq, method=accrue_method)
            
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
                known_rates.append((t_final, df.rate_from_df(t_final)))
            else:
                print(f"No cashflows for bond maturing {mature_date}")
    
    return known_dfs, [reference_date] + [cf[0] for cf in sorted(known_dfs)[1:]], known_rates

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

def bootstrapFRA(reference_date,start_date,end_date,day_count,df,forward_rate):
    t_1 = year_fraction(reference_date, start_date, day_count)
    t_2 = year_fraction(reference_date, end_date, day_count)
    new_DF = df.calcDF(t_1) * 1/(1+forward_rate*(t_2-t_1))
    return new_DF, t_2

def generate_swap_fixed_leg(settle_date, mature_date, fixed_freq=2):
    """
    Generate fixed leg payment dates for a swap
    
    Args:
        settle_date: Start date of the swap
        mature_date: End date of the swap
        fixed_freq: Payment frequency (2=semi-annual, 4=quarterly, 1=annual)
    
    Returns:
        List of payment dates
    """
    payment_dates = []
    current_date = mature_date
    
    while current_date > settle_date:
        payment_dates.append(current_date)
        current_date = (pd.Timestamp(current_date) - pd.DateOffset(months=12//fixed_freq)).date()
    
    return sorted(payment_dates)