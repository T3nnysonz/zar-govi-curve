# The Goal of Bootstrapping

Using the known discount factors up until time t, we use financial instruments to deduce the discount factor at time $t+\Delta t$

# How to Bootstrap Bonds

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

# How to Bootstrap FRAs:
Given a reference date, the start and end date of the FRA, the forward rate of the FRA, and the **discount curve** accurate until at least the start date of the FRA:

1. Calculate the discount factor at the start date of the FRA.
2. Calculate the year fraction from the start to the end of the FRA.
3. The new DF is equal to: $\frac{DF_{old}}{1+FR\times YF}$

FR = Forward rate; obtained through databases such as JIBAR
YF = Year fraction

# How to Bootstrap Swaps:
The principle behind a swap is that one party is exchanging payments of fixed amount for payments of variable amounts. Swap prices are quoted such that the present value of both types are equal.
$$PV_{fixed} = \text{Swap rate} \times \sum_i \left(DF_i \times \Delta t_i \right)$$
$$PV_{var} = \sum_j (DF_j \times \text{Forward Rate}_{j-1\rightarrow j}\times \Delta t_j)$$
$$PV_{fixed} = PV_{var} \implies \text{Swap rate} \times \sum_i \left(DF_i \times \Delta t_i \right) = \sum_j (DF_j \times \text{Forward Rate}_{j-1\rightarrow j}\times \Delta t_j)$$

As the forward rate is given by:
$$\frac{\frac{DF_1}{DF_2}-1}{T_2-T_1}$$
The equation simplifies to:
$$PV_{fixed} = PV_{var} \implies \text{Swap rate} \times \sum_i \left(DF_i \times \Delta t_i \right) = \sum_j (\frac{DF_{j-1}-DF_j}{t_j-t_{j-1}}\times \Delta t_j)$$
$$\text{Swap rate} \times \sum_i \left(DF_i \times \Delta t_i \right) = \sum_j (\frac{DF_{j-1}-DF_j}{\Delta t_j}\times \Delta t_j)$$
$$\text{Swap rate} \times \sum_i \left(DF_i \times \Delta t_i \right) = \sum_j (DF_{j-1}-DF_j)$$
$$\text{Swap rate} \times \sum_i \left(DF_i \times \Delta t_i \right) = DF_{start}-DF_{end}$$
# Other Documents:
previous : - [Bond Pricing](bond_pricing.md) - Cash flows, Coupon conevntions, clean/dirty prices 
 
next: - [Architecture](architecture.md) - Basic architecture for Webapp and bootstrapping logic