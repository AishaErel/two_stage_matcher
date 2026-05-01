from ollama import llm_score
import pandas as pd


def stage2_rerank(source_df, target_df, topk_df, evaluator=None, k=3):

    final_results = []

    for s_col in source_df.columns:

        candidates = topk_df[topk_df["source"] == s_col]["target"].tolist()[:k]

        best_score = -1
        best_target = None

        for t_col in candidates:

            # fallback safety
            if evaluator is not None:
                s_series = evaluator.source_df[s_col]
                t_series = evaluator.target_df[t_col]
            else:
                s_series = source_df[s_col]
                t_series = target_df[t_col]

            score = llm_score(
                s_col,
                t_col,
                s_series,
                t_series
            )

            # fallback if LLM fails
            if score is None:
                score = 0.0

            # keep best candidate
            if score > best_score:
                best_score = score
                best_target = t_col

        # append ONCE per source column
        final_results.append({
            "source": s_col,
            "target": best_target,
            "score": best_score
        })

    return pd.DataFrame(final_results)