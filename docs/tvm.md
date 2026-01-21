# Time Value of Money Basics:

Time Value of Money (TVM) is the idea that a sum of money today is worth more than the same sum of money in the future.

Money invested today will earn interest over time, gradually increasing the value of the investment. Whereas money that isn't invested will not experience interest. This makes money lose some of its effective purchasing power over time as its value shrinks relative other money that is circulating in markets and growing economies.

## Future Value

The future value of an invested sum may be calculated using an appropriate future value formula. The most widely used formula is:

$ FV = PV(1 + \frac{i}{n})^{n\times t} $

with:
* FV = The **Future Value** of the investment.
* PV = The **Present Value** of the money.
* n = The **number of compounding periods per year**
* t = The **number of years the investment earns interest for.**
* i = The **interest rate** the money experiences, and is equal to the percentage increase in the money's value after 1 year.

## Discounting

The idea behind the future value formula is to predict the value of a sum of money in the future based off of present information. It is critical to note that this process is reversible. Upon making PV the subject of the formula, we reverse the process, and the future value formula transforms into an equation that describes what should be invested in the present in order to accrue a value of the desired future amount, the **Present Value Formula**.

This is valuable in bond pricing as it allows us to calculate what the present value of the future payout of a bond is, which allows companies to determine bond prices.

### Discount Factors
To actually compute the present value of an investment in order to reach a desired future value, the rate at which the value of money changes must be known. The **Discount Factor** is such a rate and is defined as the ratio of a given present value to the future value of the same investment. In practice, this means that under compound interest, the **Discount Factor** takes form:

$ DF = \frac{1}{(1+r(t))^t}$

With:

* DF = The Discount factor.
* r(t) = periodic discount rate, which usually takes the form of the interest rate **i** as discussed in the Future Value Formula.
* t = the number of compounding intervals between the present and future.

The bond prices in the market can be used to determine discount factors, often using bootstrapping to achieve this.

Note 1: The calculation of the **Discount Factor** may sometimes be simplified under the assumption of a constant interest rate. In such a case:

$ DF = \frac{1}{(1+r)^t}$

Note 2: In the alternate case that compounding is done continously then it is appropriate to calculate the **Discount Factor** using the equation:

$ DF = e^{-r\times t}$

As continuous compounding is the compounding method used in actual finance, the exponential formula is the most appropriate for financial settings.

# Other Documents:
next: - [Curve Concepts](curve_concepts.md) - Zero curves, Par yield curves, Discount Factor Curves, Interpolation methods.