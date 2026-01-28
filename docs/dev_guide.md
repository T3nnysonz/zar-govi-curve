All programs should be run from the parent folder, which is where the directory will naturally land after following the steps of the README. However, if you enter a sub folder you can exit it by running

`cd ..`

# Run tests

To test cashflow generation for bonds:
`python tests\test_bonds.py`

To test the output of year_fraction() for various **Day Count** conventions:
`python tests\test_daycount.py`

To test the validity of the bootstrapping against known data:
`python tests\test_bootstrap.py`

# Run app
`streamlit run app\app.py`

# Project structure

repo/
- README.md # Project overview and quick start
- requirements.txt
- LICENSE
- .gitattributes

- src/ # Core curve bootstrapping library
    - __pycache__
        - caches
    - conventions.py # Definitions of convention, bound, and bond dictionaries
    - daycount.py # Calculating year fractions using day count conventions
    - curve.py # Creation, validation of disocount curves as well as general related calculations.
    - bonds.py # Bond cashflow generation and dirty price calculation
    - bootstrap.py # Main bootstrapping algorithm
- app/ # Web application
    - app.py # Plotting and chart generation
- data/ # Sample data and test datasets
    - testbonds.csv # Test dataset 1
    - sample_govi.csv # Test dataset 2
    - real_data.csv # Genuine market data
    - expected_output.csv # Murex bootstrapping output for real_data.csv
- docs/ # Project documentation
    - tvm.md # Time Value of Money concepts
    - curve_concepts.md # Curve construction theory
    - bond_pricing.md # Bond mathematics
    - bootstrap.md # Bootstrapping algorithm
    - input_format.md # Expected input CSV format
    - architecture.md # System architecture
    - dev_guide.md # This file - developer instructions
    - murex_validation.md # Validation against Murex
    - final_report.md # Project summary and lessons learned
    - Day_11.md # Personal notes on swaps and FRAs
    - **Images used in docs**
- tests/ # Test suite
    - test_daycount.py # Day count convention tests
    - test_bonds.py # Bond cashflow and pricing tests
    - test_bootstrap.py # Bootstrapping algorithm tests, including validation against Murex reference data
- reports/ # Daily progress reports
    - 2024-01-15.md
    - 2024-01-16.md
    - ... (daily reports)

# Other Documents
previous - [Architecture](architecture.md) - Basic architecture for Webapp and bootstrapping logic

next - [Input Format](input_format.md) - Required csv format for the app to run successfully