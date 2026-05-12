# Magneto-Inspired Two-Stage Column Matching Framework

A research-oriented prototype that explores efficient matching using a two-stage candidate ranking pipeline. The framework first applies lightweight similarity functions to rank candidates cheaply, followed by stronger and more computationally expensive similarity analysis on only the top-k candidates.

## File Structure
```
.
└── cs_262_final/
    ├── app/
    │   ├── archive/
    │   │   └── ...
    │   ├── data/
    │   │   ├── healthcare.csv
    │   │   └── *.csv
    │   ├── model/
    │   │   ├── evaluation.py
    │   │   ├── initialization.py
    │   │   └── resource.py
    │   └── main.py
    ├── .gitignore
    ├── readme.md
    └── requirements.txt
```

## File Usage
- `./app/main.py` hosts the main runtime code.
- `./app/model/resource.py` hosts file management and directory standardization code.
- `./app/model/initialization.py` hosts code for generating base "source" and "ground_truth" `.csv` files from `healthcare.csv`.
- `./app/model/evaluation.py` hosts code for evaluating cheap similarity scores.
