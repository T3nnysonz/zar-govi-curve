from datetime import date
import daycount

print(daycount.df_from_rate(0.1, 5))
print(daycount.df_from_rate(0.2, 3))
print(daycount.df_from_rate(0.1, 5, False))

StartDate = date(2026, 1, 12)
EndDate = date(2026, 5, 10)
print(daycount.year_fraction(StartDate, EndDate))
print(daycount.year_fraction(StartDate, EndDate, "ACT/360"))
print(daycount.year_fraction(StartDate, EndDate, "30/360"))