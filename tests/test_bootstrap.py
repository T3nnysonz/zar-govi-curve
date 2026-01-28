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
            'rate': 0.00,  # 0% coupon = zero-coupon bond
            'clean_price': 95.00,
            'settlement_date': date(2024,1,15),
            'type': "bond"
        }
    ]
    
    known_dfs, dates, known_rates = bootstrap_govi_curve(bonds, conventions)
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
    bonds = [
        {
            'mature_date': date(2025,1,15),
            'rate': 0.05,  # 5%
            'clean_price': 100.0,  # at par
            'settlement_date': date(2024,1,15),
            'type': "bond"
        },
        {
            'mature_date': date(2026,1,15),
            'rate': 0.05,  # 5%
            'clean_price': 100.0,
            'settlement_date': date(2024,1,15),
            'type': "bond"
        }
    ]
    
    known_dfs, dates, rates = bootstrap_govi_curve(bonds, conventions)
    times, dfs = zip(*known_dfs)
    disCurve = DiscountCurve(known_dfs, interpolation=conventions["interpolation_method"])
    
    
    # Zero rates should be ~5% at both maturities
    zero1 = rates[0][1]   # 1 year
    zero2 = rates[1][1]   # 2 years
    
    # Should be close to 5% (allow for compounding differences)
    print(f"zero-rate after 1 year:{zero1} Expected: 0.05, absolute difference: {abs(zero1 - 0.05)}")
    print(f"zero-rate after 2 years:{zero2} Expected: 0.05, absolute difference: {abs(zero2 - 0.05)}")

def test_sample_dataset_regression():
    """Test that bootstrap produces same results as saved reference"""
    instruments = []
    conventions = {
        'day_count': 'ACT/365F',
        'coupon_frequency': 4,
        'interpolation_method': 'log_linear',
        'face_value': 100,
        'accrued_method': 'linear'
    }
    
    # Load sample dataset
    url = "data/real_data.csv"
    data = pd.read_csv(url, delimiter=",")
    
    earliest = date(2099,12,31)
    
    # Convert to list of dicts
    for row in range(len(data)):
        rate = (data['rate'][row])
        clean_price = (data['clean_price'][row])
        type = (data['type'][row])
    
        mature_date = pd.Timestamp(data['maturity_date'][row]).date()
        settlement = pd.Timestamp(data['settlement_date'][row]).date()
        if(settlement<earliest):
            earliest=settlement
        
        inst = {
            'mature_date': mature_date,
            'rate': rate,
            'clean_price': clean_price,
            'settlement_date': settlement,
            'type': type
        }
        instruments.append(inst)
    
    # Load expected results (saved from a known-good run)
    expected_path = "data/expected_output.csv" # Some approximations were made when copying the murex data
    expected_df = pd.read_csv(expected_path, delimiter=",")
    
    # Run bootstrap
    discount_factors, dates, rates = bootstrap_govi_curve(instruments, conventions)
    df_times, df_vals = zip(*discount_factors)
    rate_times, rate_vals = zip(*rates)
    
    # Compare at key points
    comparison_times = [0]
    exp_dfs = [1]
    exp_rates = []
    for row in range(len(expected_df)):
        day = (expected_df['day'][row])
        month = (expected_df['month'][row])
        year = (expected_df['year'][row])
        dsFact = (expected_df['dsFactor'][row])
        dsRate = (expected_df['dsRate'][row])   
        
        exp_dfs.append(dsFact)
        exp_rates.append(dsRate)
        comp = date(year, month, day)
        comparison_times.append(year_fraction(earliest, comp, conventions['day_count']))

    plt.plot(df_times, df_vals, label = "Mine")
    plt.plot(comparison_times, exp_dfs, label = "Murex")
    plt.title("Discount factor comparison")
    plt.xlabel("Time in years since settlement")
    plt.ylabel("Discount factor")
    plt.legend()
    plt.grid()
    plt.show()
    
    plt.plot(rate_times, rate_vals, label = "Mine")
    plt.plot(comparison_times[1:], exp_rates, label = "Murex")
    plt.title("Zero rate comparison")
    plt.xlabel("Time in years since settlement")
    plt.ylabel("Zero rate")
    plt.legend()
    plt.grid()
    plt.show()
    
    
    df_vals = np.array(df_vals)
    exp_dfs = np.array(exp_dfs)
    rate_vals = np.array(rate_vals)
    exp_rates = np.array(exp_rates)
    print(abs(df_vals-exp_dfs))
    print("---------------")
    print(abs(rate_vals-exp_rates))
    
    print(f"worst absolute df error, {max(abs(df_vals-exp_dfs))}")
    print(f"worst absolute zero rate error, {max(abs(rate_vals-exp_rates))}")
    print(f"worst relative df error, {max(abs(df_vals-exp_dfs)/exp_dfs)}")
    print(f"worst relative zero rate error, {max(abs(rate_vals-exp_rates)/exp_rates)}")
    
def test_simple_bootstrap():
    """Test with known values"""
    bonds = [
        {
            'mature_date': pd.Timestamp('2025-01-15').date(),
            'rate': 0.05,  # 5%
            'clean_price': 100.0,  # At par
            'settlement_date': pd.Timestamp('2024-01-15').date(),
            'type': "bond"
        },
        {
            'mature_date': pd.Timestamp('2026-01-15').date(),
            'rate': 0.06,  # 6%
            'clean_price': 99.0,
            'settlement_date': pd.Timestamp('2024-01-15').date(),
            'type': "bond"
        }
    ]
    conventions = {
        'day_count': 'ACT/365F',
        'coupon_frequency': 2,
        'interpolation_method': 'log_linear',
        'face_value': 100,
        'accrued_method': 'linear'
    }
    
    dfs, dates, rates = bootstrap_govi_curve(bonds,conventions)
    
    print("Discount Factors:")
    for t, df in dfs:
        print(f"  t={t:.4f}, DF={df:.6f}")
    
    print("\nZero Rates:")
    for t, rate in rates:
        print(f"  t={t:.4f}, Rate={rate:.6%}")
    
    # First bond at par: zero rate should be ~5%
    assert abs(rates[0][1] - 0.05) < 0.001
    
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
    
choice4 = input("Test simple bootstrap? Enter [y/n]")
if(choice4 == 'y'):
    test_simple_bootstrap()
elif(choice4 == 'n'):
    pass
else:
    print("Unrecognised input, enter either 'y' for yes or 'n' for no")