import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from src.bonds import generate_cashflows

print("Test: bond purchased between coupon payments")
issueing = date(2024, 7, 15)
maturing = date(2025, 12, 15)
print(generate_cashflows(issueing, maturing, 0.05, 2))

print("Test: zero-coupon bond")
issueing = date(2024, 6, 15)
maturing = date(2025, 12, 15)
print(generate_cashflows(issueing, maturing, 0, 2))