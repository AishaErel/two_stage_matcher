import pandas as pd
from pathlib import Path
from evaluator import Evaluator


source_path = Path("source_1.csv")
target_path = Path("healthcare.csv")

evaluator = Evaluator(source_path, target_path)

source_columns = evaluator.source_df.columns.tolist()
target_columns = evaluator.target_df.columns.tolist()

results = []

for s_col in source_columns:
    for t_col in target_columns:
        score = evaluator.total_cheap_score(s_col, t_col, sample_size=10, seed=42)

        results.append({
            "source": s_col,
            "target": t_col,
            "score": score
        })

results_df = pd.DataFrame(results)
results_df = results_df.sort_values(["source", "score"], ascending=[True, False]).reset_index(drop=True)

results_df.to_csv("stage1_scores.csv", index=False)

top1_df = results_df.groupby("source", as_index=False).first()
top1_df.to_csv("stage1_top1.csv", index=False)

k = 3
topk_df = results_df.groupby("source", as_index=False).head(k)
topk_df.to_csv("stage1_topk.csv", index=False)

print("Saved:")
print("- stage1_scores.csv")
print("- stage1_top1.csv")
print("- stage1_topk.csv")