import pandas as pd
from evaluator import Evaluator
from pathlib import Path

def run_stage1(source_df, target_df, k_list=[1,3,5,7]):
    #find the column in target that best matches in source col?

    source_path = "temp_source.csv"
    target_path = "temp_target.csv"

    source_df.to_csv(source_path, index=False)
    target_df.to_csv(target_path, index=False)

    evaluator = Evaluator(Path(source_path), Path(target_path)) 

    results = []

    #compare every source column with every target column

    for s_col in source_df.columns:
        for t_col in target_df.columns:

            score = evaluator.total_cheap_score(s_col, t_col)

            results.append({
                "source": s_col,
                "target": t_col,
                "score": score
            })

    results_df = pd.DataFrame(results).sort_values(
        ["source", "score"],
        ascending=[True, False]
    ).reset_index(drop=True)

    top1_df = results_df.groupby("source", as_index=False).first()

    topk_outputs = {
        k: results_df.groupby("source", as_index=False).head(k)
        for k in k_list
    }

    return results_df, top1_df, topk_outputs
