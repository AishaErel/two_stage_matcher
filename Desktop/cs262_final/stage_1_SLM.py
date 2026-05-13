import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_column(name, series):
    values = series.dropna().astype(str).head(10)
    text = f"Column name: {name}. Values: {', '.join(values)}"
    return model.encode(text)

def embedding_similarity(vec1, vec2):
    return cosine_similarity([vec1], [vec2])[0][0]

def run_stage1(source_df, target_df, k_list=[1,3,5,7]):

    source_embeddings = {
        col: embed_column(col, source_df[col])
        for col in source_df.columns
    }

    target_embeddings = {
        col: embed_column(col, target_df[col])
        for col in target_df.columns
    }

    results = []

    for s_col in source_df.columns:
        for t_col in target_df.columns:

            score = embedding_similarity(
                source_embeddings[s_col],
                target_embeddings[t_col]
            )

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
