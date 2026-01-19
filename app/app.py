import streamlit as st
from datetime import date
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bootstrap import bootstrap_govi_curve
from src.curve import DiscountCurve
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.title("ZAR Government Bootstrapper")

st.header("Raw data")

data = pd.read_csv("data/testbonds.csv", delimiter=";")
bonds = []
st.write(data)

#
# Logic for computing dfs
for row in range(len(data)):
    day = (data['day'][row])
    month = (data['month'][row])
    year = (data['year'][row])
    coupon_rate = (data['coupon_rate'][row])
    clean_price = (data['clean_price'][row])
    
    mature_date = date(year,month,day)
    
    bond = {
        "mature_date":mature_date,
        "coupon_rate":coupon_rate,
        "clean_price":clean_price
    }
    bonds.append(bond)
#

st.header("Conventions")
day_count = st.selectbox("Day Count Convention: (ZAR Government Bonds default to ACT/365F)",
["ACT/365F", "ACT/360", "30/360"])
interpolation = st.selectbox("Graph Interpolation Method:", ["log_linear", "linear"])
accruation = st.selectbox("Dirty Price interest accumulation method:", ["linear", "log_linear", "none", "midpoint"])
face_val = st.number_input("Face value (treated as universal)",min_value=90.0,max_value=110.0)
coupon_freq = st.number_input("Coupon issueing rate: (Issues per year)",min_value=1,max_value=12)

convs = {
    'day_count': day_count,
    'coupon_frequency': coupon_freq,
    'interpolation_method': interpolation,
    'face_value': face_val,
    'accrued_method': accruation
}

#print(conventions)

st.header("Bounds")
df_upp = st.number_input("Maximum accepted discount factor", max_value=1.01, min_value=0.01)
df_low = st.number_input("Minimum accepted discount factor", max_value= df_upp, min_value=0.01)
rates_upp = st.number_input("Maximum accepted zero rate", max_value=0.5, min_value=0.0)
rates_low = st.number_input("Minimum accepted zero rate", max_value=rates_upp, min_value=0.0)

bnds = {
    'min_rate': rates_low,     # Rates shouldn't be negative (usually)
    'max_rate': rates_upp,    # 50% maximum (adjust for hyperinflation markets)
    'min_df': df_low,      # Discount factors shouldn't be near zero
    'max_df': df_upp,       # Discount factors may barely go above 1 for overnight market differences
}

st.header("Settlement Date")
settlement_date = st.date_input("")#

dfs = bootstrap_govi_curve(bonds, settlement_date, conventions = convs, bounds = bnds)#

dummyX = [0,face_val]
dummyY = [1,0]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4)) #
fig.set_figwidth(10)
fig.set_figheight(3)

# Plot data on the first subplot (ax1)
ax1.plot(dummyX, dummyY)
ax1.set_title('Discount Factors')
ax1.set_ylabel('Discount Factor')
ax1.set_xlabel('Time since settlement date')
ax1.grid(True)

dummyX = [0,1]
dummyY = [0.08,0.092]

# Plot data on the second subplot (ax2)
ax2.plot(dummyX, dummyY, 'r-') # 'r-' for a red line
ax2.set_title('Zero Rates')
ax2.set_ylabel('Zero Rate')
ax2.set_xlabel('Time since settlement date')
ax2.grid(True)

st.pyplot(fig=fig)
