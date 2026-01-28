# Zero curve vs par/yield curve

## Zero curve

 The zero rate on a bond is usually variable with time. Therefore, it is useful to keep track of the zero rate on a bond throughout its lifespan. This is done through the **Zero curve,** which plots the zero rate of the bond at a certain time as a function of the amount of time since the issueing of the bond.

# Par yield curve:

 ## Par yield

 Unlike zero-coupon bonds, most bonds are issued with the assumption that coupons will be paid while the bonds matures. However, at the end of the bonds maturity, the principal must also be paid pack. Before issueing the bond, we may calculate the present value of the total payout of the bond, (principal and coupons) using the percentage of the principal that the coupon is priced at. The **par yield** is the coupon rate that results in the present value of the bond payout equalling the principal payment of the bond. (Price = Face Value)

 ### Calculation of the par yield

 The present value of the bond after the full payout is equal to:

 $$ PV = \sum_{t=1}^n \frac{CR\times F}{(1+ZR(t))^t}+\frac{F}{(1+ZR(n))^n}$$

 Where:

 - PV is the present value of the bond.
 - CR is the coupon rate offered by the bond.
 - F is the face value of the bond.
 - ZR(t) is the Zero Rate t years after the isuueing of the bond.
 - n is the duration of the bond in years.

 The 2'nd term is the present value of the principal of the bond.
 The first term is the sum of the present values of all the coupons issued throughout the bond.

 To find the par yield, we want Face Value = Present Value = Price. On simplifying, this reduces to:

 $$ 1 =  \sum_{t=1}^n \frac{CR}{(1+ZR(t))^t} + \frac{1}{(1+ZR(n))^n}$$

 Which must then be solved for CR.

 ## Par yield curve

 The **par yield** curve is then a graph for bonds of varying maturity dates indicating the **par yield** of each hypothetical bond.

# Discount Factor Curves

 **Discount Factor Curves** are far more simple than par yield curves. They plot the discount factor of an arbitrary sum of money relative to today with time. Under the assumption that money is at its most valuable in the present (TVM), discount curves must be monotonically decreasing.

 As the **discount factor** is calculated solely through the interest/zero rate, and discount factors are what are directly used in finance to adjust for the **time value of money,** the discount curve may be considered a more useful version of the zero curve due to its simpler implementation. Due to this they are referred to as the **primary object.**

# Interpolation Choices and Tradeoffs

 ### Context:
 In all curve graphs, the exact value of the graph is only known/calculated at very specific timepoints known as **pillars.** The graph values between any 2 pillars must then be interpolated to allow for a useable graph. But there is no single correct interpolation technique, and thus the pros and cons of several methods should be known. This is primarily done for **Discount Factor Graphs,** but is also done for **zero curves.**

 ### Linear on Discount Factors
 This is the simplest interpolation method, where we assume that the difference factor changes linearly between 2 consecutive pillars. This assumption, while simplistic, does a relatively good job at modelling interpolation. This is because the linearity forces monotonicity of the discount factor between pillars, and ensures that the DF never leaves the range 0-1.

 On the other hand, **Linear on DF** may lead to discontinuous forward rates and the final graph will end up jagged which is both unappealing to look at and slighty innacurate.

 ### Log-Linear on Discount Factors

 This is the most commonly used interpolation method in finance. For a slight increase in computational difficulty, (which is merely running linear interpolation on a modified rather than raw dataset) the benefits of the **Linear on DF** method are retained while also being marginally smoother, more realistic of a model, and also keeps the forward rate constant between 2 pillars.

 ### Cubic Spline on Log Discount Factors

 This is visually the cleanest interpolation method. As by plotting a cubic polynomial between **Log-DF** points, we ensure continuous first and second order derivatives on the final graph. The implementation is also relatively simple.

 However, this method has 2 major problems: It may produce non positive **discount factors** which are non-sensical, and it may not be monotonic which violates the principle of **TVM.**

 ### Linear on Zero-Rates

 **Linear on Zero-Rates** is simply performing linear interpolation on the zero-rates then converting the extended dataset into difference factors, rather than the other way around. This makes the implementaion of this technique relatively simple.

 However, in some cases this method too violates the principle of **TVM** and allows for increasing discount factors. This method is scarce in practice.

 ### Monotonic Complex Spline

 This is the most powerful and realistic interpolation method. It never allows for increasing discount factors, is smooth, and keeps forward rates positive.

 It is however by far the most complicated method to implement and also runs slowly in practice.

## Project

 With regard to the curve engine, **Log-DF** interpolation will the default method used due to the high quality curve it produces relative to the complexity of the code behind it. However, the code also supports linear interpolation.

# Other Documents:
 previous : - [Time Value of Money](tvm.md) - Future Values, Discounting & Discount Factors

 next: - [Bond Pricing](bond_pricing.md) - Cash flows, Coupon conevntions, clean/dirty prices  