import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.curve import DiscountCurve

from datetime import date
from src.bonds import generate_cashflows

def test():
    issue_year = int(input("issue year:\n"))
    issue_month = int(input("issue month:\n"))
    issue_day = int(input("issue day:\n"))
    issueing = date(issue_year, issue_month, issue_day)
    mature_year = int(input("maturity year:\n"))
    mature_month = int(input("maturity month:\n"))
    mature_day = int(input("maturity day:\n"))
    maturing = date(mature_year, mature_month, mature_day)
    coupon_rate = float(input(f"Coupon rate: Enter as a float, e.g. for 5% rate enter 0.05" + "\n"))
    coupon_freq = int(input("Coupon frequency: number of coupons issued per year: \n"))

    if(maturing<issueing):
        print("Illogical input. A bond cannot mature before it's settlement date")
        choice = input("rerun test? enter [y/n]")
        if(choice == 'y'):
            test()
        elif(choice == 'n'):
            pass
        else:
            print("unregistered input")
            pass
    else:
        cash = generate_cashflows(issueing, maturing, coupon_rate, coupon_freq)
        print(cash)
        choice = input("rerun test? enter [y/n]")
        if(choice == 'y'):
            test()
        elif(choice == 'n'):
            pass
        else:
            print("unregistered input")
            pass

test()