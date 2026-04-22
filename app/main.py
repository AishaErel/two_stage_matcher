##  Import Standard Libraries
import pandas as pd

##  Import Local Libraries
import model.resource as resource
from model.initialization import initialGeneration
from model.evaluation import Evaluator

def main():
    ##  Generate initial sources and truths from healthcare data.
    ##  Uses `initialGeneration()` from `model/initialization.py`.
    # initialGeneration()

    test_evaluator:Evaluator = Evaluator(resource.getDataFile("source_1.csv"), resource.getDataFile("healthcare.csv"))
    print(f"Test Cheap Score (Columns `Gender` vs. `Sex`): {test_evaluator.total_cheap_score('Sex', 'Gender')}")

if __name__ == "__main__":
    main()