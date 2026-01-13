import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from src.daycount import df_from_rate
from src.daycount import year_fraction

print(df_from_rate(0.1, 5))
print(df_from_rate(0.2, 3))
print(df_from_rate(0.1, 5, False))

StartDate = date(2026, 1, 12)
EndDate = date(2026, 5, 10)
print(year_fraction(StartDate, EndDate))
print(year_fraction(StartDate, EndDate, "ACT/360"))
print(year_fraction(StartDate, EndDate, "30/360"))