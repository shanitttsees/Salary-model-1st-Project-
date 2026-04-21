import streamlit as st
from pathlib import Path

from salary_model import load_or_train_model, predict_salary

MODEL_PATH = Path("models/salary_model.joblib")

st.set_page_config(page_title="Salary Predictor", page_icon="💼", layout="centered")

st.title("Salary Predictor")
st.write(
    "Estimate annual base salary using experience, education, city tier, and role. "
    "The model is trained on a synthetic dataset to demonstrate a deployable salary prediction app."
)

model = load_or_train_model(MODEL_PATH)

experience = st.slider("Years of experience", min_value=0, max_value=30, value=3, step=1)
education = st.selectbox("Education level", ["High School", "Bachelor's", "Master's", "PhD"])
city = st.selectbox("City tier", ["Tier 1", "Tier 2", "Tier 3"])
role = st.selectbox(
    "Job role",
    ["Software Engineer", "Data Analyst", "Senior Engineer", "Manager"],
)

if st.button("Predict salary"):
    input_data = {
        "experience": experience,
        "education": education,
        "city": city,
        "role": role,
    }
    salary = predict_salary(model, input_data)
    st.success(f"Predicted annual salary: ${salary:,.0f}")
    st.write(
        "This estimate is generated from a sample salary model. Use it for exploration and testing."
    )

with st.expander("How it works"):
    st.write(
        "The application trains a regression model from a synthetic dataset and uses it to predict salary based on the selected inputs. "
        "You can change features and rerun predictions instantly."
    )
