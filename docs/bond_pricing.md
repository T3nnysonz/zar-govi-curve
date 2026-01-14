# Cashflow Schedule

Money does not sit idly. Therefore when predicting the financial situation of any entity it's important to consider the movement of money. This naturally has to be estimated as it is impossible to see the future, but the general strategy is to clearly document all predicted gains and losses of money, which are called **cash inflows** and **cash outflows.**

### Cash Inflows

Cash inflows are expected sources of income during the period that the Cashflow Schedule considers such as: salary, donations, sales, or investments.

### Cash Outflows

Cash outflows are expected expenditures during the period that the Cashflow Schedule considers such as: payments, bills, loans, or purchases.

Over the period of the cashflow schedule, the predicted **net cash flow** is simply the expected **cash inflow** - the expected **cash outflow.** Then the expected amount of money held at the the end of the cashflow schedule is simply the amount of money that was started with + the change in amount of money during the period of the cashflow schedule. Or simply:

**End Balance = Start Balance + Net Cash Flow**

# Coupon Conventions

## Day Count Conventions

When determining how much interest a bond has accrued, the amount of time in years since the bond's issueing is needed. However, different companies and countries use different conventions.

| Convention | Description|
|------------|------------|
|ACT/365F    |Actual amount of days / 365 (assumes no leap years) |
|ACT/ACT     |The actual amount of days passed / Actual number of days in the year |
|30/360      |Assumes every month has exactly 30 days|
|ACT/360     |Assumes a year has exactly 360 days |

**South African Government Bonds use ACT/365F.**

## Payment Frequency

Different bonds issue coupons at different rates:

* Never : Zero-Coupon Bonds
* Monthly : Every month with a month defined in the standard way (relative to the Gregorian Calendar
)
* Quaterly: Every 3 months
* Semi-Anually: Every 6 months (used by South African Government Bonds)
* Anually: Every full year

## Date Adjustment

Sometimes payment dates full on non-business days; Once again, different entities have different solution conventions to this problem:

* No adjustment: Pay on payment date even if it falls on a non-business day. (South African Government Bonds)
* Preceding: The payment moves to the preceding business day.
* Following: The payment moves to the following business day.

# Clean vs Dirty Price

Coupons are issued at fixed points in the year, and are not issued relative to the issueing of the bond. Therefore, when buying a bond at any point between 2 coupon dates the buyer has to pay the initial price of the bond, (Clean Price) as well as the interest that would have been earned should the bond have been purchased on a coupon date (Accrued Interest). This total sum is called the Dirty Price and is thus calculated as:

$$ DP = CP + AI $$

* DP = Dirty Price (honest, therefore useful in settlement and necessary in bootsrapping)
* CP = Clean Price (stable, therefore useful in trading)
* AI = Accrued Interest

**Bootstrapping formula uses Dirty Prices**