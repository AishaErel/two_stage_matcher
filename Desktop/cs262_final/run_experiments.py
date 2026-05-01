import pandas as pd

from stage_1 import run_stage1
from stage_2 import stage2_rerank
from evaluator import Evaluator
from initialization import initialGeneration

initialGeneration() 
# loads source_df (ground truth data) and target_df (predicted_data)

def evaluate_mappings(pred_df, gt_df):

    gt_dict = dict(zip(gt_df["source"], gt_df["target"]))
    pred_dict = dict(zip(pred_df["source"], pred_df["target"]))

    correct = 0
    total = len(gt_dict)

    for src, true_target in gt_dict.items():
        pred_target = pred_dict.get(src)
        if pred_target == true_target:
            correct += 1

    return {
        "accuracy": correct / total if total else 0.0,
        "total": total,
        "correct": correct
    }


DATASETS = [
    ("source_1.csv", "ground_truth_1.csv"),
    ("source_2.csv", "ground_truth_2.csv"),
    ("source_3.csv", "ground_truth_3.csv"),
]

TARGET_FILE = "healthcare.csv"


from pathlib import Path

def run_experiment(source_file, gt_file):

    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(TARGET_FILE)
    gt_df = pd.read_csv(gt_file)

    # stage 1
    results_df, top1_df, topk_dict = run_stage1(source_df, target_df)
    topk_df = topk_dict[3] #best scores per column based on stage 1 results (which uses diff k values)

    #stage 2
    final_df = stage2_rerank(source_df, target_df, topk_df)

    # save predictions temporarily (Evaluator needs file paths)
    pred_path = "temp_predictions.csv"
    final_df.to_csv(pred_path, index=False)
    print(final_df.head())
    print(final_df.columns)

    #evaluation
    metrics = evaluate_mappings(final_df, gt_df)
    

    return final_df, metrics

def main():

    summary = []

    for source_file, gt_file in DATASETS:

        print(f"Running {source_file}")

        final_df, metrics = run_experiment(source_file, gt_file)

        final_df.to_csv(f"{source_file}_stage2_results.csv", index=False)

        metrics["dataset"] = source_file
        summary.append(metrics)

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv("summary.csv", index=False)

    print("\nFINAL RESULTS:")
    print(summary_df)


if __name__ == "__main__":
    main()