# The Goal of Bootstrapping

Using the known discount factors for the next n coupon periods, we seek the discount factor for the n+1'th coupon period

# How to Bootstrap

1. Obtain the prices for n bonds, each of different maturity dates.
2. Sort the bonds by maturity date, shortest to longest.
3. The bond with the shortest maturity date may be treated as a **zero-coupon** bond as there are no coupon issues until the bond matures.
4. Treating the bond with the shortest maturity date as a **zero-coupon** bond. It is critical that the forst bond used is a **zero-coupon bond** or some equivalent, or our initial equation will be missing data. With the zero-coupon bond, calculate the discount factor using:
$$ DF = \frac{Dirty Price}{Face Value}$$

5. Proceed the following by induction until the n+1'th discount factor is known:
    1. Assume the first k discount factors are known.
    2. Select the bond with shortest maturity date that uses the k+1'th discount factor in its price calculation.
    3. Calculate the **dirty price** of the selected bond, which will be equivalent to the **present value** of the bond using the k known discount factors.
    4. Use the **dirty price** as the **present value** in the formula:
     $$ PV = \sum_{i=1}^{k+1} Cashflow(t_i)*DF(t_i) $$
     which in this case becomes:
     $$ Dirty Price = \sum_{i=1}^{k+1} CouponRate*DiscountFactor(t_i) + Principal*DiscountFactor(t_{k+1})$$
    5. Solve the above formula for the **Discount Factor** at the k+1'th coupon issueing which is also the maturity date of the selected bond
    
# Other Documents:
previous : - [Bond Pricing](bond_pricing.md) - Cash flows, Coupon conevntions, clean/dirty prices  
next: - 