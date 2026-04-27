import pandas as pd
import difflib
import random
import re


def normalize_text(text: str) -> str:
    text = str(text).lower().replace("_", " ")
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return text.strip()


def name_similarity(a: str, b: str) -> float:
    a = normalize_text(a)
    b = normalize_text(b)
    return difflib.SequenceMatcher(None, a, b).ratio()


def sample_values(series: pd.Series, sample_size: int = 10, seed: int = 42) -> list[str]:
    values = series.dropna().astype(str).tolist()
    if not values:
        return []

    random.seed(seed)
    if len(values) <= sample_size:
        return values
    return random.sample(values, sample_size)


def value_similarity(series1: pd.Series, series2: pd.Series, sample_size: int = 10, seed: int = 42) -> float:
    vals1 = sample_values(series1, sample_size, seed)
    vals2 = sample_values(series2, sample_size, seed)

    tokens1 = set()
    tokens2 = set()

    for v in vals1:
        tokens1.update(normalize_text(v).split())

    for v in vals2:
        tokens2.update(normalize_text(v).split())

    if not tokens1 and not tokens2:
        return 0.0

    intersection = len(tokens1 & tokens2)
    union = len(tokens1 | tokens2)
    return intersection / union if union > 0 else 0.0


def infer_column_type(series: pd.Series) -> str:
    non_null = series.dropna()
    if non_null.empty:
        return "unknown"

    numeric_count = pd.to_numeric(non_null, errors="coerce").notna().sum()
    if numeric_count / len(non_null) > 0.8:
        return "numeric"

    sample_as_str = non_null.astype(str).head(20)
    if len(sample_as_str) > 0:
        date_like_count = sample_as_str.str.contains(r"[-/]").sum()
        if date_like_count >= max(1, len(sample_as_str) // 2):
            parsed = pd.to_datetime(sample_as_str, errors="coerce")
            if parsed.notna().mean() > 0.8:
                return "date"

    unique_ratio = non_null.nunique() / len(non_null)
    if unique_ratio < 0.5:
        return "categorical"

    return "text"


def type_similarity(series1: pd.Series, series2: pd.Series) -> float:
    return 1.0 if infer_column_type(series1) == infer_column_type(series2) else 0.0


def evaluate_method(results_df: pd.DataFrame, gt_df: pd.DataFrame, method_name: str, dataset_name: str, k: int = 3) -> dict:
    sorted_df = results_df.sort_values(["source", "score"], ascending=[True, False]).reset_index(drop=True)

    top1_df = sorted_df.groupby("source", as_index=False).first()
    merged_top1 = top1_df.merge(gt_df, on="source", suffixes=("_pred", "_true"))
    merged_top1["correct"] = merged_top1["target_pred"] == merged_top1["target_true"]
    top1_accuracy = merged_top1["correct"].mean()

    topk_df = sorted_df.groupby("source", as_index=False).head(k)

    hits = 0
    total = 0
    for _, row in gt_df.iterrows():
        s_col = row["source"]
        true_target = row["target"]
        predicted_targets = topk_df[topk_df["source"] == s_col]["target"].tolist()
        if true_target in predicted_targets:
            hits += 1
        total += 1

    recall_at_k = hits / total if total > 0 else 0.0

    return {
        "dataset": dataset_name,
        "method": method_name,
        "top1_accuracy": top1_accuracy,
        f"recall_at_{k}": recall_at_k
    }


datasets = [
    ("source_1.csv", "ground_truth_1.csv"),
    ("source_2.csv", "ground_truth_2.csv"),
    ("source_3.csv", "ground_truth_3.csv"),
]

target_file = "healthcare.csv"
summary_rows = []

for source_file, gt_file in datasets:
    print(f"\nRunning experiment for {source_file}")

    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)
    gt_df = pd.read_csv(gt_file)

    source_columns = source_df.columns.tolist()
    target_columns = target_df.columns.tolist()

    all_results = {
        "name_only": [],
        "value_only": [],
        "type_only": [],
        "name_value": [],
        "name_value_type": []
    }

    for s_col in source_columns:
        for t_col in target_columns:
            n_sim = name_similarity(s_col, t_col)
            v_sim = value_similarity(source_df[s_col], target_df[t_col], sample_size=10, seed=42)
            t_sim = type_similarity(source_df[s_col], target_df[t_col])

            all_results["name_only"].append({
                "source": s_col,
                "target": t_col,
                "name_sim": n_sim,
                "value_sim": v_sim,
                "type_sim": t_sim,
                "score": n_sim
            })

            all_results["value_only"].append({
                "source": s_col,
                "target": t_col,
                "name_sim": n_sim,
                "value_sim": v_sim,
                "type_sim": t_sim,
                "score": v_sim
            })

            all_results["type_only"].append({
                "source": s_col,
                "target": t_col,
                "name_sim": n_sim,
                "value_sim": v_sim,
                "type_sim": t_sim,
                "score": t_sim
            })

            all_results["name_value"].append({
                "source": s_col,
                "target": t_col,
                "name_sim": n_sim,
                "value_sim": v_sim,
                "type_sim": t_sim,
                "score": 0.7 * n_sim + 0.3 * v_sim
            })

            all_results["name_value_type"].append({
                "source": s_col,
                "target": t_col,
                "name_sim": n_sim,
                "value_sim": v_sim,
                "type_sim": t_sim,
                "score": 0.5 * n_sim + 0.3 * v_sim + 0.2 * t_sim
            })

    dataset_tag = source_file.replace(".csv", "")

    for method_name, rows in all_results.items():
        method_df = pd.DataFrame(rows)

        score_filename = f"{dataset_tag}_{method_name}_scores.csv"
        top1_filename = f"{dataset_tag}_{method_name}_top1.csv"

        method_df.to_csv(score_filename, index=False)

        top1_df = (
            method_df
            .sort_values(["source", "score"], ascending=[True, False])
            .groupby("source", as_index=False)
            .first()
        )
        top1_df.to_csv(top1_filename, index=False)

        metrics = evaluate_method(method_df, gt_df, method_name, dataset_tag, k=3)
        summary_rows.append(metrics)

summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv("experiment_summary_all.csv", index=False)

print("\nExperiment Summary:")
print(summary_df)
print("\nSaved experiment_summary_all.csv and all per-dataset score files.")