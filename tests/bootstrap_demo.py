from datetime import date
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bootstrap import bootstrap_govi_curve
from src.curve import DiscountCurve

bond1 = {
    'mature_date': date(2026, 6, 15),
    'coupon_rate': 0.05,
    'clean_price': 97
}

bond2 = {
    'mature_date': date(2026, 12, 15),
    'coupon_rate': 0.06,
    'clean_price': 99.5
}

bond3 = {
    'mature_date': date(2025, 12, 15),
    'coupon_rate': 0.055,
    'clean_price': 98
}

bond4 = {
    'mature_date': date(2027, 6, 15),
    'coupon_rate': 0.07,
    'clean_price': 100
}

bond5 = {
    'mature_date': date(2025, 6, 15),
    'coupon_rate': 0,
    'clean_price': 99
}

bonds = [bond1, bond2, bond3, bond4, bond5]
settle_date = date(2024,12, 15)

data = bootstrap_govi_curve(bonds, settle_date)
graph = DiscountCurve(data)
graph.plot()
print(data)