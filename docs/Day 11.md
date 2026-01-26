# Instruments
An instrument in finance refers to any binding contract which compels 1 party to buy and 1 party to sell.

# Market Rates
There are entities such as JIBAR that keep track of the **current** interest rates of a large family of **instruments**. These current interest rates are the **market rates**.

## Floaters
When bond pricing, it is not uncommon to use the market rate as the coupon rate of the bond. In which case, the coupon recieved is essentially just the interest earned by the bond's principal.
Since the coupon rate is tied to the market rate, which is variable, the coupons received throughout then bond's maturity is also variable. Thus it is natural to say that a floater has **variable rate** where as standard bonds such as the ones I have been using thus far have been **fixed rate**.

### Implementation
The implementation of **variable rates** when bootstrapping is difficult. In theory, I would need the market rates at various points in the future that may be referred to when generating bond cashflows in order to reflect the variable interest rate. However this obviously means I need information from the future, and the market rates are only accurate to the present, with no reliable method to discern the future.

Therefore, assumptions need to be made. The market quotes rates for every bond; while I am not completely sure of the origins of the numbers used in these quotes, they are likely themselves tied to predictions regarding future market rates. Thus, by trusting the provided quotes, and interpolating between them, there is a semblance of a method at guessing the market rate.

# Swaps
The most common kind of swap is an interest rate swap. In which case, two parties essentially bet against each other about market rates:

Party A has issued a variable interest rate bond, while party B has issued a fixed rate bond. If party A believes that the market rate will grow rapidly, they expect to have to pay out more in coupons than they bargained for. If party B expects the market rate to not grow rapidly, they expect that it would be more profitable to hold a variable interest rate bond which would have them paying less than the current fixed rate (assuming the market rate indeed does not grow rapidly). Thus, party A and B desire each other's bond and as such they swap. Then the bet begins, if party A was correct about market trends, they save money in payouts whereas party B loses money in payouts. 

If party B is correct, they save money in payouts whereas party A loses money in payouts.

# Forward Rate agreements

Not understood yet. Something about risk management. The quoted rate and the market rate are compared at maturity to determine payout, but the I don't understand the specifics.