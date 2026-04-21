from pathlib import Path

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

CATEGORICAL_FEATURES = ["education", "city", "role"]
NUMERIC_FEATURES = ["experience"]


def build_dataset(n_samples: int = 1200, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.RandomState(random_state)
    experience = rng.randint(0, 21, size=n_samples)
    education = rng.choice(
        ["High School", "Bachelor's", "Master's", "PhD"],
        size=n_samples,
        p=[0.15, 0.5, 0.25, 0.1],
    )
    city = rng.choice(["Tier 1", "Tier 2", "Tier 3"], size=n_samples, p=[0.35, 0.4, 0.25])
    role = rng.choice(
        ["Software Engineer", "Data Analyst", "Senior Engineer", "Manager"],
        size=n_samples,
        p=[0.4, 0.25, 0.2, 0.15],
    )

    education_value = {
        "High School": -5000,
        "Bachelor's": 0,
        "Master's": 8000,
        "PhD": 15000,
    }
    city_value = {"Tier 1": 10000, "Tier 2": 4000, "Tier 3": 0}
    role_value = {
        "Software Engineer": 0,
        "Data Analyst": -3000,
        "Senior Engineer": 12000,
        "Manager": 18000,
    }

    salary = (
        35000
        + experience * 2500
        + np.array([education_value[e] for e in education])
        + np.array([city_value[c] for c in city])
        + np.array([role_value[r] for r in role])
        + rng.normal(0, 7000, size=n_samples)
    )

    return pd.DataFrame(
        {
            "experience": experience,
            "education": education,
            "city": city,
            "role": role,
            "salary": salary,
        }
    )


def build_pipeline() -> Pipeline:
    encoder = OneHotEncoder(handle_unknown="ignore")
    transformer = ColumnTransformer(
        transformers=[("cat", encoder, CATEGORICAL_FEATURES)], remainder="passthrough"
    )
    model = RandomForestRegressor(n_estimators=120, random_state=42)
    return Pipeline([("preprocessor", transformer), ("regressor", model)])


def train_salary_model(model_path: Path) -> Pipeline:
    df = build_dataset()
    pipeline = build_pipeline()
    pipeline.fit(df[CATEGORICAL_FEATURES + NUMERIC_FEATURES], df["salary"])
    model_path.parent.mkdir(parents=True, exist_ok=True)
    dump(pipeline, model_path)
    return pipeline


def load_or_train_model(model_path: Path) -> Pipeline:
    if model_path.exists():
        return load(model_path)
    return train_salary_model(model_path)


def predict_salary(model: Pipeline, input_data: dict) -> float:
    frame = pd.DataFrame([input_data])
    prediction = model.predict(frame)[0]
    return float(np.clip(prediction, 15000, 250000))
