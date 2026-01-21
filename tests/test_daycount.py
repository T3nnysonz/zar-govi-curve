import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from src.daycount import year_fraction

def test():
    s_year = int(input())
    s_month = int(input())
    s_day = int(input())
    e_year = int(input())
    e_month = int(input())
    e_day = int(input())
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