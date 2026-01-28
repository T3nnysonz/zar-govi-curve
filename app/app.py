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

@st.dialog("Conventions Help")
def helpConventions():
    st.subheader("Day Count Convention")
    st.write("Different markets calculate the time between dates differently. Each method is called a day count")
    st.write("- ACT/365F: Considers all years to have 365 days.")
    st.write("- ACT/360: Condisders all years to have 360 days.")
    st.write("- 30/360: Considers all months to have 30 days.")
    st.subheader("Graph Interpolation method")
    st.write("The provided raw data can only be used to precisely calculate curve data at fixed pillars, the interpolation method decides how to handle the gaps.")
    st.write("- Linear: Draws a stright line between pillar datapoints.")
    st.write("- Log_linear: Takes the log of the output values, linearly interpolates between them, and reverses the logarithms")
    st.subheader("Dirty Price accumulation method")
    st.write("The amount paid for a bond is the dirty price. When buying a bond between coupon issues, one must pay the immature coupon value. There are many ways this coupon value is calculated:")
    st.write("- Linear: linearly increases accrued amount as time between passes between pillar times.")
    st.write("- Log_linear: linearly increases the log of the accrued amount as time between passes between pillar times.")
    st.write("- None: Does not accrue any interest.")
    st.write("- Midpoint: Accrues half a full coupon every time.")
    st.subheader("Face value")
    st.write("The amount the will be paid at maturity. It is strongly advised to keep this parameter at 100.")
    st.subheader("Frequency")
    st.write("This bond exclusive parameter holds the coupon frequency of all bonds in the instrument list.")
    st.write("The value inputted is the number of coupons issued per year.")
    
@st.dialog("Conventions Help")
def helpBounds():
    st.subheader("Discount factor bounds")
    st.write("Here you can decide what to tolerate as the maximal and minimal discount factors of your curve are.")
    st.write("Hard limits:")
    st.write("- Upper bounds above 1.01 are never accepted. This is because the Time Value of Money says that the value of money should decrease with time")
    st.write("- Lower bounds greater than upper bounds are never accepted. Illogical")
    st.write("- Lower bounds less than or equal to zero are never accepted. Zero correlates to worthless money and negatives make no logical sense.")
    st.subheader("Zero rate bounds")
    st.write("Here you can decide what to tolerate as the maximal and minimal rates of your curve are.")
    st.write("Hard limits:")
    st.write("- Upper bounds above 0.50 are never accepted. Even hyperinflation markets scarcely go this high.")
    st.write("- Lower bounds greater than upper bounds are never accepted. Illogical")
    st.write("- Lower bounds less than are never accepted. This would correlate to discount factor > 1.")

try:
    url = st.text_input("Enter url for csv containing bond data:","data/testbonds.csv")
    data = pd.read_csv(url, delimiter=",")
except:
    st.error("Unknown file: File by that name could not be found. Remember to add .csv to the end of your file name")

st.header("Raw data")

Instruments = []
st.write(data)
earliest = date(2099, 12, 31)

# Instrument creation.
for row in range(len(data)):
    try:
        rate = (data['rate'][row])
        clean_price = (data['clean_price'][row])
        type = (data['type'][row])
        mature_date = pd.Timestamp(data['maturity_date'][row]).date()
        settlement_date = pd.Timestamp(data['settlement_date'][row]).date()
    except:
        st.write(f"Invalid date. Bootstrapping halted. Halted on line {row}")
        st.write("At least 1 column was missing or had name mispelled.")
        st.write("Expected format: 'maturity_date',coupon_rate','clean_price','settlement_date'")
        break
    
    if(mature_date<earliest):
        earliest = mature_date
    
    inst = src.conventions.getInstrument(mature_date, rate, clean_price, settlement_date, type)
    Instruments.append(inst)

st.header("Parameters")
tab1, tab2 = st.tabs(["Conventions","Bounds"])
day_count = tab1.selectbox("Day Count Convention:",
["ACT/365F", "ACT/360", "30/360"])
interpolation = tab1.selectbox("Graph Interpolation Method:", ["log_linear", "linear"])
accruation = tab1.selectbox("Dirty Price interest accumulation method:", ["linear", "log_linear", "none", "midpoint"])
face_val = tab1.number_input("Face value:",min_value=90.0,max_value=110.0, value=100.0)
coupon_freq = tab1.number_input("Frequency:",min_value=1,max_value=12, value = 2)
helpConvs = tab1.button("Conventions help")
if(helpConvs):
    helpConventions()

convs = src.conventions.getConventions(day_count, coupon_freq, interpolation, face_val, accruation)

df_upp = tab2.number_input("Maximum accepted discount factor", max_value=1.01, min_value=0.01, value = 1.0)
df_low = tab2.number_input("Minimum accepted discount factor", max_value= df_upp, min_value=0.01)
rates_upp = tab2.number_input("Maximum accepted zero rate", max_value=0.5, min_value=0.0, value = 0.25)
rates_low = tab2.number_input("Minimum accepted zero rate", max_value=rates_upp, min_value=0.0)
helpBnds = tab2.button("Bounds help")
if(helpBnds):
    helpBounds()

bnds = src.conventions.getBounds(rates_low, rates_upp, df_low, df_upp)
try:
    dfs_data, dates, rates_data = bootstrap_govi_curve(Instruments, conventions = convs, bounds = bnds)#
    dfs_curve = DiscountCurve(dfs_data, interpolation=convs["interpolation_method"], bounds=bnds)
except Exception as e:
    st.error("An error occured during bootstrapping: " + str(e))

try:
    x,y = dfs_curve.plot()
except Exception as e:
    st.error("Error occured while plotting Discount Factors, " + str(e))
    x = []
    y = []
    passed = False
try:
    x1, y1 = dfs_curve.plot_zero_rates()
except Exception as e:
    st.error("An error occured while computing zero-rates, "+ str(e))
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
    st.error("Did not generate table due to failure to generate graph(s)")

fn = 'Discount Curve.png'
img = io.BytesIO()
plt.savefig(img, format='png')
 
btn = st.download_button(
   label="Download image",
   data=img,
   file_name=fn,
   mime="image/png"
)