import pandas as pd

from stage_1_heuristic import run_stage1 as run_stage1_cheap
from stage_1_SLM import run_stage1 as run_stage1_embedding
import time


def evaluate_topk(topk_df, gt_df, k):
    hits = 0
    total = len(gt_df)

    for _, row in gt_df.iterrows():
        source_col = row["source"]
        true_target = row["target"]

        predicted_targets = topk_df[topk_df["source"] == source_col]["target"].tolist()

        if true_target in predicted_targets:
            hits += 1

    return hits / total if total else 0.0


def evaluate_top1(top1_df, gt_df):
    merged = top1_df.merge(gt_df, on="source", suffixes=("_pred", "_true"))
    merged["correct"] = merged["target_pred"] == merged["target_true"]

    return merged["correct"].mean() if not merged.empty else 0.0


def run_comparison(source_file, target_file, gt_file):
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)
    gt_df = pd.read_csv(gt_file)

    rows = []

    methods = {
        "cheap_score": run_stage1_cheap,
        "small_lm_embedding": run_stage1_embedding
    }

    for method_name, run_func in methods.items():
        print(f"Running {method_name} on {source_file}")

   
        start = time.time()

        results_df, top1_df, topk_dict = run_func(source_df, target_df)


        end = time.time()
        runtime = end - start

        top1_accuracy = evaluate_top1(top1_df, gt_df)

        row = {
            "dataset": source_file,
            "method": method_name,
            "top1_accuracy": top1_accuracy,
            "runtime_seconds": runtime   
        }

        for k, topk_df in topk_dict.items():
            row[f"recall_at_{k}"] = evaluate_topk(topk_df, gt_df, k)

        rows.append(row)

        dataset_tag = source_file.replace(".csv", "")
        results_df.to_csv(f"{dataset_tag}_{method_name}_stage1_scores.csv", index=False)
        top1_df.to_csv(f"{dataset_tag}_{method_name}_stage1_top1.csv", index=False)

    return rows


if __name__ == "__main__":
    DATASETS = [
        ("source_1.csv", "ground_truth_1.csv"),
        ("source_2.csv", "ground_truth_2.csv"),
        ("source_3.csv", "ground_truth_3.csv"),
    ]

    TARGET_FILE = "target_wide.csv"

    all_rows = []

    for source_file, gt_file in DATASETS:
        all_rows.extend(run_comparison(source_file, TARGET_FILE, gt_file))

    summary_df = pd.DataFrame(all_rows)
    summary_df.to_csv("stage1_method_comparison.csv", index=False)

    print("\nStage 1 Comparison:")
    print(summary_df)
