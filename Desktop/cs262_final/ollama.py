import requests
import random
import re


def serialize_column(name, series, sample_size=10):
    values = series.dropna().astype(str).tolist()

    if len(values) > sample_size:
        values = random.sample(values, sample_size)

    return f"""Column Name: {name}
Values:
- """ + "\n- ".join(values)


def build_prompt(source_serialized, target_serialized):
    return f"""
You are a schema matching expert.

Return ONLY a number between 0 and 1.

SOURCE:
{source_serialized}

TARGET:
{target_serialized}

Score:
"""


def extract_score(text):
    match = re.search(r"0(\.\d+)?|1(\.0+)?", text)
    if not match:
        return None
    try:
        return float(match.group())
    except:
        return None


def llm_score(source_col, target_col, source_series, target_series):

    source_serialized = serialize_column(source_col, source_series)
    target_serialized = serialize_column(target_col, target_series)

    prompt = build_prompt(source_serialized, target_serialized)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )

        raw = response.json()["response"].strip()

        score = extract_score(raw)

        if score is None:
            return None

        return min(max(score, 0.0), 1.0)

    except Exception:
        return None