# Input Format

**maturity_date,coupon_rate,clean_price,settlement_date**

## Notes:
- Refer to the above line for the exact naming convention of each data type.
- All dates should be inputted in the form yyyy-mm-dd
- Ensure that the earliest date inputted is at earliest 10 years exactly before the date the bootstrapper is used.
- Ensure that the latest date inputted is at latest 11 years exactly after the date the bootstrapper is used.
- coupon_rate is a float containing the coupon rate offered by the bond. Example: a 5% yearly bond should be treated as 0.05. If coupons are issued more often than yearly, do not correct for that here, there is an option on the Webapp for coupon issueing frequency. Note that the coupon issueing frequency option is treated as the universal frequency of all bonds in the csv.
- Clean price is the percentage of the face value that the bond is priced at. no % sign is needed, a 99.5% clean price is simply 99.5.
- As the input type is a csv, which is being read as a dataframe by pandas, the order of the columns does not matter, as long as the actual data used correctly corresponds to the column in which it was inputted.

## Example:
```csv
coupon_rate,clean_price,maturity_date,settlement_date
0.05,97,2026-06-15,2025-1-1
0.06,99.5,2026-12-15,2025-1-1
0.055,98,2025-12-15,2025-1-1
0.07,100,2027-06-15,2025-1-1
0.0,99,2025-06-15,2025-1-1
```

# Other Documents
previous - [Developer Guide](dev_guide.md) - Repo structure and basic usage instructions

next - [Murex Validation](murex_validation.md) -  Discussion of validation of bootstrapping algorithm relative to Murex results.