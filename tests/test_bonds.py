import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.curve import DiscountCurve

from datetime import date
from src.bonds import generate_cashflows
from src.bonds import price_from_curve

disCurve1 = DiscountCurve([(0,1),(1,0.75),(2,0.5),(3,0.25)])

print("Test: bond purchased between coupon payments")
issueing = date(2024, 7, 15)
maturing = date(2025, 12, 15)
cash1 = generate_cashflows(issueing, maturing, 0.05, 2)
print(cash1)
print(price_from_curve(issueing, cash1, disCurve1))

print("Test: zero-coupon bond")
issueing = date(2024, 6, 15)
maturing = date(2025, 12, 15)
cash2 = generate_cashflows(issueing, maturing, 0, 2)
print(cash2)
print(price_from_curve(issueing, cash2, disCurve1))

### Different discount curve

disCurve2 = DiscountCurve([(0,1),(1,0.7),(2,0.49),(3,0.343), (4,0.2401)])
#disCurve2.interpolate()
#disCurve2.plot()

print("Test: bond purchased between coupon payments")
issueing = date(2024, 7, 15)
maturing = date(2025, 12, 15)
cash3 = generate_cashflows(issueing, maturing, 0.05, 2)
print(cash3)
print(price_from_curve(issueing, cash3, disCurve2))

print("Test: zero-coupon bond")
issueing = date(2024, 6, 15)
maturing = date(2025, 12, 15)
cash4 = generate_cashflows(issueing, maturing, 0, 2)
print(cash4)
print(price_from_curve(issueing, cash4, disCurve2))