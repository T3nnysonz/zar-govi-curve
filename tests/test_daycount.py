import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from src.daycount import year_fraction

def test():
    s_year = int(input("Start year"))
    s_month = int(input("Start month"))
    s_day = int(input("Start day"))
    e_year = int(input("End year"))
    e_month = int(input("End month"))
    e_day = int(input("End day"))
    StartDate = date(s_year, s_month, s_day)
    EndDate = date(e_year, e_month, e_day)
    print("ACT/365F:", year_fraction(StartDate, EndDate))
    print("ACT/360:", year_fraction(StartDate, EndDate, "ACT/360"))
    print("30/360:", year_fraction(StartDate, EndDate, "30/360"))
    choice = input("rerun test? enter [y/n]")
    if(choice == 'y'):
        test()
    elif(choice == 'n'):
        pass
    else:
        print("unregistered input")
        pass

test()