from datetime import date
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bootstrap import bootstrap_govi_curve
from src.curve import DiscountCurve
from src.daycount import year_fraction
import pandas as pd
import numpy as np
from pathlib import Path

def test_zero_coupon_bond():
    """Zero coupon bonds should bootstrap directly from price"""
    
    conventions = {
        'day_count': 'ACT/365F',
        'coupon_frequency': 1,
        'interpolation_method': 'log_linear',
        'face_value': 100,
        'accrued_method': 'linear'
    }
    bonds = [
        {
            'mature_date': date(2025,1,15),
            'coupon_rate': 0.00,  # 0% coupon = zero-coupon bond
            'clean_price': 95.00
        }
    ]
    settlement_date = date(2024,1,15)
    
    known_dfs, dates = bootstrap_govi_curve(bonds, settlement_date, conventions)
    disCurve = DiscountCurve(known_dfs, interpolation=conventions["interpolation_method"])
    
    # DF at 1 year should be 0.95 (95/100)
    expected_df = 0.95
    actual_df = disCurve.calcDF(1.0)  # 1 year
    
    print(f"expected: {expected_df} actual: {actual_df}, absoulute error: {abs(expected_df-actual_df)}")
    
    # Use assertAlmostEqual for floating point comparison
    #assert abs(actual_df - expected_df) < 1e-10

def test_two_par_bonds_flat_curve():
    """Two bonds at par should give flat zero curve"""
    conventions = {
        'day_count': 'ACT/365F',
        'coupon_frequency': 1,
        'interpolation_method': 'log_linear',
        'face_value': 100,
        'accrued_method': 'linear'
    }
    settlement_date=date(2024,1,15)
    bonds = [
        {
            'mature_date': date(2025,1,15),
            'coupon_rate': 0.05,  # 5%
            'clean_price': 100.0  # at par
        },
        {
            'mature_date': date(2026,1,15),
            'coupon_rate': 0.05,  # 5%
            'clean_price': 100.0
        }
    ]
    
    known_dfs, dates = bootstrap_govi_curve(bonds, settlement_date, conventions)
    times, dfs = zip(*known_dfs)
    disCurve = DiscountCurve(known_dfs, interpolation=conventions["interpolation_method"])
    
    
    # Zero rates should be ~5% at both maturities
    zero1 = disCurve.rate_from_df(times[1])   # 1 year
    zero2 = disCurve.rate_from_df(times[2])   # 2 years
    
    # Should be close to 5% (allow for compounding differences)
    print(f"zero-rate after 1 year:{zero1} Expected: 0.05, absolute difference: {abs(zero1 - 0.05)}")
    print(f"zero-rate after 2 years:{zero2} Expected: 0.05, absolute difference: {abs(zero2 - 0.05)}")
    
def test_known_cashflow_sequence():
    """Test with bonds where we can manually verify"""
    # This is a more complex example where you'd
    # pre-calculate the expected DFs
    pass

#test_zero_coupon_bond()
#test_two_par_bonds_flat_curve()

def test_sample_dataset_regression():
    """Test that bootstrap produces same results as saved reference"""
    bonds = []
    conventions = {
        'day_count': 'ACT/365F',
        'coupon_frequency': 1,
        'interpolation_method': 'log_linear',
        'face_value': 100,
        'accrued_method': 'linear'
    }
    
    # Load sample dataset
    url = "data/real_data.csv"
    data = pd.read_csv(url, delimiter=";")
    
    # Convert to list of dicts
    for row in range(len(data)):
        day = (data['day'][row])
        month = (data['month'][row])
        year = (data['year'][row])
        coupon_rate = (data['coupon_rate'][row])
        clean_price = (data['clean_price'][row])
    
        mature_date = date(year,month,day)
        
        bond = {
            'mature_date': mature_date,
            'coupon_rate': coupon_rate,
            'clean_price': clean_price
        }
        bonds.append(bond)
    
    # Load expected results (saved from a known-good run)
    expected_path = "data/expected_output.csv" # Some approximations were made when copying the murex data
    expected_df = pd.read_csv(expected_path, delimiter=";")
    
    # Run bootstrap
    settlement = date(2025,10,2)  # All bonds should have same settlement
    discount_factors, dates = bootstrap_govi_curve(bonds, settlement, conventions)
    disc_curve = DiscountCurve(discount_factors, conventions["interpolation_method"])
    
    # Compare at key points
    print("Murex comparison")
    for row in range(len(expected_df)):
        day = (expected_df['day'][row])
        month = (expected_df['month'][row])
        year = (expected_df['year'][row])
        dsFact = (expected_df['dsFactor'][row])
        dsRate = (expected_df['dsRate'][row])
    
        mature_date = date(year,month,day)
        
        actual_df = disc_curve.calcDF(year_fraction(settlement, mature_date, conventions['day_count']))
        actual_zero = disc_curve.rate_from_df(year_fraction(settlement, mature_date, conventions['day_count']))

        print(date)
        print(f"Expected Discount Factor:{dsFact}, got: {actual_df}")
        print(f"Expected Zero rate:{dsRate}, got: {actual_zero}")

test_sample_dataset_regression()