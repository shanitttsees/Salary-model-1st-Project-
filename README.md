# Salary Predictor Web App

A simple salary prediction web application built with Streamlit and scikit-learn.

## Files added

- `app.py` - Streamlit web interface for entering experience, education, city tier, and role
- `salary_model.py` - builds and loads a regression model from synthetic salary data
- `requirements.txt` - Python dependencies for the app

## Run locally

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Start the Streamlit app:

```bash
streamlit run app.py
```

3. Open the URL shown in the terminal (usually `http://localhost:8501`).

## Notes

- The model is trained on synthetic sample data for demonstration.
- You can customize the app or deploy it to Streamlit Cloud, Azure App Service, or any Python web host.
