import pandas as pd

pred = pd.read_csv("top1_name_matches.csv")
gt = pd.read_csv("ground_truth_1.csv")

merged = pred.merge(gt, on="source", suffixes=("_pred", "_true"))
merged["correct"] = merged["target_pred"] == merged["target_true"]

print(merged[["source", "target_pred", "target_true", "correct"]])

accuracy = merged["correct"].mean()
print(f"\nTop-1 Accuracy: {accuracy:.4f}")