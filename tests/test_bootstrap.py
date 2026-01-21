from datetime import date
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bootstrap import bootstrap_govi_curve
from src.curve import DiscountCurve
from src.daycount import year_fraction
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    data = pd.read_csv(url, delimiter=",")
    
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
    expected_df = pd.read_csv(expected_path, delimiter=",")
    
    # Run bootstrap
    settlement = date(2025,10,2)  # All bonds should have same settlement
    discount_factors, dates = bootstrap_govi_curve(bonds, settlement, conventions)
    disc_curve = DiscountCurve(discount_factors, conventions["interpolation_method"])
    
    # Compare at key points
    time_points = []
    exp_dfs = []
    exp_rates = []
    act_dfs = []
    act_rates = []
    for row in range(len(expected_df)):
        day = (expected_df['day'][row])
        month = (expected_df['month'][row])
        year = (expected_df['year'][row])
        dsFact = (expected_df['dsFactor'][row])
        dsRate = (expected_df['dsRate'][row])   
        
        exp_dfs.append(dsFact)
        exp_rates.append(dsRate)
    
        mature_date = date(year,month,day)
        time_point = year_fraction(settlement, mature_date, conventions['day_count'])
        time_points.append(time_point)
        
        actual_df = disc_curve.calcDF(time_point)
        actual_zero = disc_curve.rate_from_df(time_point)
        act_dfs.append(actual_df)
        act_rates.append(actual_zero)

    plt.plot(time_points, act_dfs, label = "Mine")
    plt.plot(time_points, exp_dfs, label = "Murex")
    plt.title("Discount factor comparison")
    plt.xlabel("Time in years since settlement")
    plt.ylabel("Discount factor")
    plt.legend()
    plt.grid()
    plt.show()
    
    plt.plot(time_points, act_rates, label = "Mine")
    plt.plot(time_points, exp_rates, label = "Murex")
    plt.title("Zero rate comparison")
    plt.xlabel("Time in years since settlement")
    plt.ylabel("Zero rate")
    plt.legend()
    plt.grid()
    plt.show()
    
    act_dfs = np.array(act_dfs)
    exp_dfs = np.array(exp_dfs)
    act_rates = np.array(act_rates)
    exp_rates = np.array(exp_rates)
    print(abs(act_dfs-exp_dfs)/exp_dfs)
    print("---------------")
    print(abs(act_rates-exp_rates)/exp_rates)
choice1 = input("Test bootstrapping for zero coupon bond? Enter [y/n]")
if(choice1 == 'y'):
    test_zero_coupon_bond()
elif(choice1 == 'n'):
    pass
else:
    print("Unrecognised input, enter either 'y' for yes or 'n' for no")

choice2 = input("Test bootstrapping for two par bonds? Enter [y/n]")
if(choice2 == 'y'):
    test_two_par_bonds_flat_curve()
elif(choice2 == 'n'):
    pass
else:
    print("Unrecognised input, enter either 'y' for yes or 'n' for no")

choice3 = input("Test bootstrapping for sample murex data? Enter [y/n]")
if(choice3 == 'y'):
    test_sample_dataset_regression()
elif(choice3 == 'n'):
    pass
else:
    print("Unrecognised input, enter either 'y' for yes or 'n' for no")