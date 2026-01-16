import streamlit as st
from datetime import date
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bootstrap import bootstrap_govi_curve
from src.curve import DiscountCurve
import matplotlib.pyplot as plt

print("1")

st.set_page_config(layout="wide")

dummyX = [0,1]
dummyY = [1,0]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4)) #
fig.set_figwidth(8)
fig.set_figheight(3)

bonds = ""

# Plot data on the first subplot (ax1)
ax1.plot(dummyX, dummyY)
ax1.set_title('Sine Wave')
ax1.set_ylabel('Amplitude')
ax1.set_xlabel('Angle (radians)')
ax1.grid(True)

dummyX = [0,1]
dummyY = [0.08,0.092]

# Plot data on the second subplot (ax2)
ax2.plot(dummyX, dummyY, 'r-') # 'r-' for a red line
ax2.set_title('Cosine Wave')
ax2.set_xlabel('Angle (radians)')
ax2.grid(True)

st.title("ZAR Government Bootstrapper")
bonds_area = st.text(body="Bonds")

bond_on=False

with st.sidebar:

    if(st.button("Add bond")):
        print("2")
        print(bond_on)
        if(bond_on):
            print("on")
            bond_on=False
        else:
            print("off")
            bond_on=True
            print("3")
            print(bond_on)
            bonds_area.text(body =f"james's, {bonds}")
            st.write("No bond is stonger than family")
            day_input = st.date_input("Date:") # Maturity date
            st.number_input("Rate:") # Coupon rate
            st.number_input("Pate:") # Clean price
            enter = st.button("Enter")
            if(enter):
                day = day_input.timetuple
                print(day)
                bonds += str(day)
                bonds_area.text(body =f"bonds, {bonds}")

    if(st.button("Conventions")):
        st.selectbox("Day count conventions:", ['ACT/365F', 'ACT/ACT', 'ACT/360', '30/360'])
        st.selectbox("Interpolation conventions:", ['ACT/365F', 'ACT/ACT', 'ACT/360', '30/360'])
        st.selectbox("Accruement conventions:", ['ACT/365F', 'ACT/ACT', 'ACT/360', '30/360'])
        st.button("Enter")
    st.button("Data Bounds")
st.pyplot(fig=fig)
