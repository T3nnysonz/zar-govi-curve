import streamlit as st
from datetime import date
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bootstrap import bootstrap_govi_curve
from src.curve import DiscountCurve
import matplotlib.pyplot as plt
import pandas as pd
import io
import src.conventions

st.set_page_config(layout="wide")
st.title("ZAR Government Bootstrapper")
data = ""
passed = True

try:
    url = st.text_input("Enter url for csv containing bond data:","data/testbonds.csv")
    data = pd.read_csv(url, delimiter=",")
except:
    st.write("Unknown file: File by that name could not be found. Remember to add .csv to the end of your file name")

st.header("Raw data")

bonds = []
st.write(data)
earliest = date(2099, 12, 31)

# Bond creation.
for row in range(len(data)):
    try:
        coupon_rate = (data['coupon_rate'][row])
        clean_price = (data['clean_price'][row])
    except:
        st.write("At least 1 column was missing or had name mispelled.")
        st.write("Expected format: 'maturity_date',coupon_rate','clean_price','settlement_date'")
        break;
    
    try:
        mature_date = pd.Timestamp(data['maturity_date'][row]).date()
        settlement_date = pd.Timestamp(data['settlement_date'][row]).date()
    except:
        st.write(f"Invalid date. Bootstrapping halted. Halted on line {row}")
        break
    
    if(mature_date<earliest):
        earliest = mature_date
    
    bond = src.conventions.getBond(mature_date, coupon_rate, clean_price, settlement_date)#
    bonds.append(bond)

st.header("Parameters")
tab1, tab2 = st.tabs(["Conventions","Bounds"])
day_count = tab1.selectbox("Day Count Convention: (ZAR Government Bonds default to ACT/365F)",
["ACT/365F", "ACT/360", "30/360"])
interpolation = tab1.selectbox("Graph Interpolation Method:", ["log_linear", "linear"])
accruation = tab1.selectbox("Dirty Price interest accumulation method:", ["linear", "log_linear", "none", "midpoint"])
face_val = tab1.number_input("Face value (treated as universal)",min_value=90.0,max_value=110.0, value=100.0)
coupon_freq = tab1.number_input("Coupon issueing rate: (Issues per year)",min_value=1,max_value=12, value = 2)

convs = src.conventions.getConventions(day_count, coupon_freq, interpolation, face_val, accruation)

df_upp = tab2.number_input("Maximum accepted discount factor", max_value=1.01, min_value=0.01, value = 1.0)
df_low = tab2.number_input("Minimum accepted discount factor", max_value= df_upp, min_value=0.01)
rates_upp = tab2.number_input("Maximum accepted zero rate", max_value=0.5, min_value=0.0, value = 0.25)
rates_low = tab2.number_input("Minimum accepted zero rate", max_value=rates_upp, min_value=0.0)

bnds = src.conventions.getBounds(rates_low, rates_upp, df_low, df_upp)
try:
    dfs_data, dates, rates_data = bootstrap_govi_curve(bonds, conventions = convs, bounds = bnds)#
    dfs_curve = DiscountCurve(dfs_data, interpolation=convs["interpolation_method"], bounds=bnds)
except Exception as e:
    st.warning("An error occured during bootstrapping: " + str(e))

try:
    x,y = dfs_curve.plot()
except Exception as e:
    st.warning("Error occured while plotting Discount Factors" + str(e))
    x = []
    y = []
    passed = False
try:
    x1, y1 = dfs_curve.plot_zero_rates()
except Exception as e:
    st.warning("An error occured while computing zero-rates, this usually means that the upper bound was exceeded. To prevent this, choose an earlier settlement date. "+ str(e))
    x1 = []
    y1 = []
    passed = False

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4)) #
fig.set_figwidth(10)
fig.set_figheight(4)

# Plot data on the first subplot (ax1)
ax1.plot(x, y)
ax1.set_title('Discount Factors')
ax1.set_ylabel('Discount Factor')
ax1.set_xlabel('Time since settlement date')
ax1.grid(True)

# Plot data on the second subplot (ax2)
ax2.plot(x1, y1, 'r-') # 'r-' for a red line
ax2.set_title('Zero Rates')
ax2.set_ylabel('Zero Rate')
ax2.set_xlabel('Time since settlement date')
ax2.grid(True)

st.pyplot(fig=fig)

# Table

if(passed):
    year_fracs, rates_raw = zip(*rates_data)
    rates = ["Na"]
    for r in rates_raw:
        rates.append(r)
    year_fracs, dfs = zip(*dfs_data)
    frame = pd.DataFrame({"Date:":dates,"Time in years since settlement:":year_fracs,"Discount Factor:":dfs,"Zero Rates:":rates})
    st.write(frame)

    st.download_button("Download curve as .csv", data=frame.to_csv().encode("utf-8"),file_name="bootstrapped_data.csv")
else:
    st.warning("Did not generate table due to failure to generate graph(s)")

fn = 'Discount Curve.png'
img = io.BytesIO()
plt.savefig(img, format='png')
 
btn = st.download_button(
   label="Download image",
   data=img,
   file_name=fn,
   mime="image/png"
)
