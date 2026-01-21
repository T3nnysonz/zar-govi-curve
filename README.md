# ZAR Government Bond Curve Bootstrapping

A web application for bootstrapping zero curves from South African government bond data.

## Project Overview

- 

## Setup

### Prerequisites
- Python 3.10 or higher
- Git (for version control)

### Installation

1. Clone repository:
```
git clone https://github.com/T3nnysonz/zar-govi-curve.git
cd zar-govi-curve
```

2. Virtual Environment:

On Windows:
```
python -m venv venv
venv\Scripts\activate
```

On Mac or Linux:
```
python -m venv venv
source venv/bin/activate
```

3. Dependencies:
```
pip install -r requirements.txt
```

4. Run Demo:
```
cd app
python app.py
```

## Documentation

- [Time Value of Money](docs/tvm.md) - Future Values, Discounting & Discount Factors
- [Curve Concepts](docs/curve_concepts.md) - Zero curves, Par yield curves, Discount Factor Curves, Interpolation methods.
- [Bond Pricing](docs/bond_pricing.md) - Cash flows, Coupon conevntions, clean/dirty prices  
- [Bootstrapping Algorithm](docs/bootstrap.md) - What Bootstrapping is and how to perform it.
- [Dev Guide](docs/dev_guide.md) - Project structure and how to run tests, and the app.
- [Input format](docs/input_format.md) - Input format expected for bond list CSVs.
- [Murex validation](docs/murex_validation) - Discussion of validation of bootstrapping algorithm relative to Murex results.
- [Architecture](docs/architecture.md) - Overview of overall project architecture and logic flow.