##  Import Standard Libraries
import difflib
import numbers
import Levenshtein
import numpy as np
import pandas as pd
from pathlib import Path

##  Import Local Libraries
# Evaluator answers if two columns represent the same kind of data

class Evaluator: 
    def __init__(self, source_path:Path, target_path:Path) -> None:
        self.source_df:pd.DataFrame = pd.read_csv(source_path) 
        self.target_df:pd.DataFrame = pd.read_csv(target_path)

    

    def total_cheap_score(self, ref_col:str, hyp_col:str, n_samples:int=50) -> float:
        """
            Temporary cheap score.  Change.
            its meant to test soes column A look like column B based on their data
            
        """
        result:float = 0.0
        
        ##  tmp note:: 
        ##      source data is reference (ground truth table)
        ##      target data is hypothesis (predicted table)

        ##  TODO:: batch random (average?) and collision avoidance
        rand_ref_val = self.source_df[ref_col].sample(n=1).iloc[0]
        rand_hyp_val = self.target_df[hyp_col].sample(n=1).iloc[0]

        name_sim:float = Evaluator._cheap_str_sim_score(ref_col, hyp_col)
        #compare age vs patient_age
        
        sample_size = min(n_samples, len(self.source_df), len(self.target_df))
        ref_samples = self.source_df[ref_col].sample(n=sample_size).values
        hyp_samples = self.target_df[hyp_col].sample(n=sample_size).values

        scores = []
        for r, h in zip(ref_samples, hyp_samples): #for each pair,
            t_sim = Evaluator._datatype_sim_score(r, h) #if number vs number its good, string vs string good
            v_sim = Evaluator._generic_value_eval(r, h) #checs actual closeness such that if numbers close 
            scores.append(t_sim * v_sim)  #combines them

        avg_content_sim = sum(scores) / len(scores) if scores else 0.0

        result = (0.3 * name_sim) + (0.7 * avg_content_sim) #final score form paper
        return result

    def _cheap_str_sim_score(ref:str, hyp:str, method:int=1) -> float:
        """
            Returns a similarity score between `ref` and `hyp` using the specified `method`.
            Checks text similarity
        """
        ref = ref.strip().lower()
        hyp = hyp.strip().lower()
        match method:
            case 1:
                return difflib.SequenceMatcher(None, ref, hyp).ratio()
            # case 2:
            #     return Levenshtein.ratio(ref, hyp)
            case _:
                raise ValueError(f"Unsupported evaluation method: {method}")
            
    def _generic_value_eval(ref:object, hyp:object) -> float:
        """
            Evaluates the similarity between `ref` and `hyp` based on their generic values.
            checks value similairty

            TODO:: Evaluation not really generic yet
        """
        result:float = 0.0
        
        if type(ref) == type(hyp):
            if ref == hyp:
                result = 1.0
        elif isinstance(ref, str) and isinstance(hyp, str):
            result = Evaluator._cheap_str_sim_score(ref, hyp) 

        if isinstance(ref, (numbers.Number, np.number)) and isinstance(hyp, (numbers.Number, np.number)):
            diff = abs(float(ref) - float(hyp))
            result = 1.0 / (1.0 + diff)

        return result
    


    def _datatype_sim_score(ref:object, hyp:object) -> float:
        """
            Returns a similarity score between the datatypes of `ref` and `hyp`.
            checks type compatibility
        """
        if type(ref) == type(hyp):
            return 1.0
        
        is_ref_num = isinstance(ref, (numbers.Number, np.number))
        is_hyp_num = isinstance(hyp, (numbers.Number, np.number))
        
        if is_ref_num and is_hyp_num:
            return 0.9
        
        if isinstance(ref, str) and isinstance(hyp, str):
            return 1.0
            
        return 0.0
    
    # def __example_datatype_sim_score() -> None:
    #     """
    #         Example usage of `datatype_sim_score()`.
    #         """
    #     ##  str vs str :: 1.0
    #     print(f"\"hello\"{type("hello")} vs \"123\"{type("123")}: {Evaluator.datatype_sim_score("hello", "123")}")
    #     ##  str vs int :: 0.24
    #     print(f"\"hello\"{type("hello")} vs 123{type(123)}: {Evaluator.datatype_sim_score("hello", 123)}")
    #     ##  str vs float :: 0.272727...
    #     print(f"\"hello\"{type("hello")} vs 123.0{type(123.0)}: {Evaluator.datatype_sim_score("hello", 123.0)}")
    #     ##  int vs float :: 0.727272...
    #     print(f"123{type(123)} vs 123.0{type(123.0)}: {Evaluator.datatype_sim_score(123, 123.0)}")