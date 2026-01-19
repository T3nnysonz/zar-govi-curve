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
st.write("data goes here")

#data = pd.read_csv("goes in data.csv")
#st.write(data)

#
# Logic for computing dfs
#

st.header("Conventions")
day_count = st.selectbox("Day Count Convention: (ZAR Government Bonds default to ACT/365F)",
["ACT/365F", "ACT/360", "30/360"])
interpolation = st.selectbox("Graph Interpolation Method:", ["log_linear", "linear"])
accruation = st.selectbox("Dirty Price interest accumulation method:", ["linear", "log_linear", "none", "midpoint"])
face_val = st.number_input("Face value (treated as universal)",min_value=90.0,max_value=110.0)
coupon_freq = st.number_input("Coupon issueing rate: (Issues per year)",min_value=1,max_value=12)

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

st.header("Bounds")
df_upp = st.number_input("Maximum accepted discount factor", max_value=1.01, min_value=0.01)
df_low = st.number_input("Minimum accepted discount factor", max_value= df_upp, min_value=0.01)
rates_upp = st.number_input("Maximum accepted zero rate", max_value=0.5, min_value=0.0)
rates_low = st.number_input("Minimum accepted zero rate", max_value=rates_upp, min_value=0.0)
