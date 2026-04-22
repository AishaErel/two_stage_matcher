##  Import Standard Libraries
import difflib
import Levenshtein
import pandas as pd
from pathlib import Path

##  Import Local Libraries
import model.resource as resource

class Evaluator:
    def __init__(self, source_path:Path, target_path:Path) -> None:
        self.source_df:pd.DataFrame = pd.read_csv(source_path)
        self.target_df:pd.DataFrame = pd.read_csv(target_path)

    def total_cheap_score(self, ref_col:str, hyp_col:str) -> float:
        result:float = 0.0
        
        ##  tmp note:: 
        ##      source data is reference
        ##      target data is hypothesis

        ##  TODO:: batch random (average?) and collision avoidance
        rand_ref_val = self.source_df[ref_col].sample(n=1).iloc[0]
        rand_hyp_val = self.target_df[hyp_col].sample(n=1).iloc[0]

        name_sim:float = Evaluator._cheap_str_sim_score(ref_col, hyp_col)
        value_sim:float = Evaluator._generic_value_eval(rand_ref_val, rand_hyp_val)
        data_sim:float = Evaluator._datatype_sim_score(rand_ref_val, rand_hyp_val)

        result = 0.5 * name_sim + 0.3 * value_sim + 0.2 * data_sim
        return result

    def _cheap_str_sim_score(ref:str, hyp:str, method:int=1) -> float:
        """
            Returns a similarity score between `ref` and `hyp` using the specified `method`.
        """
        match method:
            case 1:
                return difflib.SequenceMatcher(None, ref, hyp).ratio()
            case 2:
                return Levenshtein.ratio(ref, hyp)
            case _:
                raise ValueError(f"Unsupported evaluation method: {method}")
            
    def _generic_value_eval(ref:object, hyp:object) -> float:
        """
            Evaluates the similarity between `ref` and `hyp` based on their generic values.

            TODO:: Evaluation not really generic yet
        """
        result:float = 0.0
        
        if type(ref) == type(hyp):
            if ref == hyp:
                result = 1.0
        elif isinstance(ref, str) and isinstance(hyp, str):
            result = Evaluator.cheap_str_sim_score(ref, hyp)
        elif isinstance(ref, (int, float)) and isinstance(hyp, (int, float)):
            result = max(float(ref), float(hyp)) / min(float(ref), float(hyp))

        return result

    def _datatype_sim_score(ref:object, hyp:object) -> float:
        """
            Returns a similarity score between the datatypes of `ref` and `hyp`.

            TODO::  For now, finds score by comparing attributes of each datatype.  
                    May be circumstantially accurate.  Consider binary/categorical score...
        """
        ref_attrs = set(dir(ref))
        hyp_attrs = set(dir(hyp))
        intersection = ref_attrs.intersection(hyp_attrs)
        union = ref_attrs.union(hyp_attrs)
        return len(intersection) / len(union)
    
    def __example_datatype_sim_score() -> None:
        """
            Example usage of `datatype_sim_score()`.
            """
        ##  str vs str :: 1.0
        print(f"\"hello\"{type("hello")} vs \"123\"{type("123")}: {Evaluator.datatype_sim_score("hello", "123")}")
        ##  str vs int :: 0.24
        print(f"\"hello\"{type("hello")} vs 123{type(123)}: {Evaluator.datatype_sim_score("hello", 123)}")
        ##  str vs float :: 0.272727...
        print(f"\"hello\"{type("hello")} vs 123.0{type(123.0)}: {Evaluator.datatype_sim_score("hello", 123.0)}")
        ##  int vs float :: 0.727272...
        print(f"123{type(123)} vs 123.0{type(123.0)}: {Evaluator.datatype_sim_score(123, 123.0)}")
