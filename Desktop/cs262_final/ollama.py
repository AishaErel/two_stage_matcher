import requests
import random
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def serialize_column(name, series, sample_size=10):
    values = series.dropna().astype(str).tolist()

    if len(values) > sample_size:
        values = random.sample(values, sample_size)

    return {
        "column_name": name,
        "values": values
    }


def build_prompt(source_obj, target_obj):
    return f"""
You are a schema matching expert.

Task:
Given two columns, estimate how likely they represent the same concept.

Return ONLY valid JSON in this format:

{{
  "score": float between 0 and 1
}}

Rules:
- No explanations
- No extra text
- Only JSON

SOURCE:
{json.dumps(source_obj)}

TARGET:
{json.dumps(target_obj)}
"""


def extract_score(raw_text):
    try:
        data = json.loads(raw_text)
        score = float(data.get("score", 0.0))
        return max(0.0, min(1.0, score))
    except:
        return None

def llm_score(source_col, target_col, source_series, target_series):

    source_obj = serialize_column(source_col, source_series)
    target_obj = serialize_column(target_col, target_series)

    prompt = build_prompt(source_obj, target_obj)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "temperature": 0
            },
            timeout=20
        )

        data = response.json()
        raw = data.get("response", None)

        if raw is None:
            print("LLM WARNING: no 'response' field ->", data)
            return None

        raw = raw.strip()

        # try parsing float directly (better than regex)
        try:
            return float(raw)
        except:
            return None

    except Exception as e:
        print("LLM ERROR:", e)
        return None
