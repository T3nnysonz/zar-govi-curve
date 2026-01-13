# Time Value of Money Basics:

Time Value of Money (TVM) is the idea that a sum of money that is invested is worth more than money that isn't. In particular:

Money invested today will earn interest over time, gradually increasing the value of the investment. Whereas money that isn't invested will not experience interest, making that money effectively less valuable than invested money over long periods of time.

## Future Value

With regard to interest, the future value of an invested sum may be calculated using an appropriate future value formula. The most widely used formula is:

$ FV = PV(1 + \frac{i}{n})^{n\times t} $

with:
* FV = The **Future Value** of the investment.
* PV = The **Present Value** of the money.
* n = The **number of compounding periods per year**
* t = The **number of years the investment earns interest for.**
* i = The **interest rate** the money experiences, and is equal to the percentage increase in the money's value after 1 year.

## Discounting

The idea behind the future value formula is to predict the value of a sum of money in the future based off of current interest and investment information. It is critical to note that this process is reversible. Upon reversing this process, the future value formula transforms into an equation that describes what should be invested in the present in order to accrue a value of the desired future amount.

This is valuable in bond pricing as it allows us to calculate what the present value of the future payout of a bond is, which allows companies to determine bond prices.

### Discount Factors
To actually compute the present value of an investment in order to reach a desired future value, the rate at which the value of money changes must be known. The **Discount Factor** is such a rate and is defined as the ratio of a given present value to the future value of the same investment. In practice, this means that under compound interest, the **Discount Factor** takes form:

$ DF = \frac{1}{(1+r)^n}$

With:

* DF = The Discount factor.
* r = periodic discount rate, which usually takes the form of the interest rate **i** as discussed in the Future Value Formula.
* n = the number of compounding intervals between the present and future.

The bond prices in the market can be used to determine discount factors

Note 1: The calculation of the **Discount Factor** may often be simplified under the assumption of a constant interest rate, in which case one may simply compare the present value of an investment/bond and the future value 1 compounding period in the future. (Setting n = 1). In such a case:

$ DF = \frac{1}{(1+r)}$

Note 2: In the alternate case that compounding is done continously then it is appropriate to calculate the **Discount Factor** using the equation:

$ DF = e^{-r\times t}$

As continuous compounding is the compounding method used in actual finance, the exponential formula is the most appropriate for financial settings.

3