# Input Format

**day,month,year,coupon_rate,clean_price**

## Notes:
- Use the above line exactly as is as a header line of the .csv used
- day, month, and year are integers. Make sure that the combination of day, month, and year used form a valid date with the earliest allowed date being 10 years before the date the bootstrapper is used.
- Ensure that the earliest date inputted is at latest 11 years exactly after the date the bootstrapper is used.
- coupon_rate is a float containing the coupon rate offered by the bond. Example: a 5% yearly bond should be treated as 0.05. If coupons are issued more often than yearly, do not correct for that here, there is an option on the Webapp for coupon issueing frequency. Note that the coupon issueing frequency option is treated as the universal frequency of all bonds in the csv.
- Clean price is the percentage of the face value that the bond is priced at. no % sign is needed, a 99.5% clean price is simply 99.5.
- As the input type is a csv, which is being read as a dataframe by pandas, the order of the columns does not matter, as long as the actual data used correctly corresponds to the column in which it was inputted.

## Example:
```csv
day,month,year,coupon_rate,clean_price
15,3,2025,0.055,100
15,9,2025,0.046,102
15,3,2026,0.07,100
15,9,2026,0.0714,100
10,12,2026,0.0718,101
15,3,2026,0.0719,100
15,9,2027,0.0729,100
```

# Other Documents
previous - [Developer Guide](dev_guide.md) - Repo structure and basic usage instructions

next - [Murex Validation](murex_validation.md) -  Discussion of validation of bootstrapping algorithm relative to Murex results.