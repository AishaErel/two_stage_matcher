import pandas as pd
from ollama_handler import llm_score
from evaluator import Evaluator


def stage2_rerank(source_df, target_df, topk_df, evaluator, k=3):

    final_results = []

    for s_col in source_df.columns:

        candidates = topk_df[topk_df["source"] == s_col]["target"].tolist()[:k]

        best_score = -1
        best_target = None

        for t_col in candidates:

            llm_s = llm_score(
                s_col,
                t_col,
                source_df[s_col],
                target_df[t_col]
            )

        # fallback if LLM fails
            if llm_s is None:
                llm_s = evaluator.total_cheap_score(s_col, t_col)

            if llm_s > best_score:
                best_score = llm_s
                best_target = t_col

        final_results.append({
            "source": s_col,
            "target": best_target,
            "score": best_score
        })

    return pd.DataFrame(final_results)
