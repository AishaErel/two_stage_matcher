import difflib
import random
import re
from pathlib import Path

import pandas as pd


class Evaluator:
    def __init__(self, source_path: Path, target_path: Path) -> None:
        self.source_df: pd.DataFrame = pd.read_csv(source_path)
        self.target_df: pd.DataFrame = pd.read_csv(target_path)

        # Cache inferred column types once
        self.source_types = {
            col: Evaluator._infer_column_type(self.source_df[col])
            for col in self.source_df.columns
        }
        self.target_types = {
            col: Evaluator._infer_column_type(self.target_df[col])
            for col in self.target_df.columns
        }

    def total_cheap_score(self, ref_col: str, hyp_col: str, sample_size: int = 10, seed: int = 42) -> float:
        name_sim: float = Evaluator._cheap_str_sim_score(ref_col, hyp_col)

        value_sim: float = Evaluator._column_value_similarity(
            self.source_df[ref_col],
            self.target_df[hyp_col],
            sample_size=sample_size,
            seed=seed
        )

        data_sim: float = self._datatype_sim_score(ref_col, hyp_col)

        result = 0.5 * name_sim + 0.3 * value_sim + 0.2 * data_sim
        return result

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = str(text).lower().replace("_", " ")
        text = re.sub(r"[^a-z0-9 ]", "", text)
        return text.strip()

    @staticmethod
    def _cheap_str_sim_score(ref: str, hyp: str) -> float:
        ref = Evaluator._normalize_text(ref)
        hyp = Evaluator._normalize_text(hyp)
        return difflib.SequenceMatcher(None, ref, hyp).ratio()

    @staticmethod
    def _sample_values(series: pd.Series, sample_size: int = 10, seed: int = 42) -> list[str]:
        values = series.dropna().astype(str).tolist()
        if not values:
            return []

        random.seed(seed)
        if len(values) <= sample_size:
            return values
        return random.sample(values, sample_size)

    @staticmethod
    def _column_value_similarity(
        ref_series: pd.Series,
        hyp_series: pd.Series,
        sample_size: int = 10,
        seed: int = 42
    ) -> float:
        ref_values = Evaluator._sample_values(ref_series, sample_size, seed)
        hyp_values = Evaluator._sample_values(hyp_series, sample_size, seed)

        ref_tokens = set()
        hyp_tokens = set()

        for val in ref_values:
            ref_tokens.update(Evaluator._normalize_text(val).split())

        for val in hyp_values:
            hyp_tokens.update(Evaluator._normalize_text(val).split())

        if not ref_tokens and not hyp_tokens:
            return 0.0

        intersection = len(ref_tokens & hyp_tokens)
        union = len(ref_tokens | hyp_tokens)

        return intersection / union if union > 0 else 0.0

    @staticmethod
    def _infer_column_type(series: pd.Series) -> str:
        non_null = series.dropna()

        if non_null.empty:
            return "unknown"

        # numeric check
        numeric_count = pd.to_numeric(non_null, errors="coerce").notna().sum()
        if numeric_count / len(non_null) > 0.8:
            return "numeric"

        # simple date-like heuristic before expensive parsing
        sample_as_str = non_null.astype(str).head(20)
        date_like_count = sample_as_str.str.contains(r"[-/]").sum()

        if date_like_count >= max(1, len(sample_as_str) // 2):
            parsed = pd.to_datetime(sample_as_str, errors="coerce")
            if parsed.notna().mean() > 0.8:
                return "date"

        unique_ratio = non_null.nunique() / len(non_null)
        if unique_ratio < 0.5:
            return "categorical"

        return "text"

    def _datatype_sim_score(self, ref_col: str, hyp_col: str) -> float:
        ref_type = self.source_types[ref_col]
        hyp_type = self.target_types[hyp_col]
        return 1.0 if ref_type == hyp_type else 0.0