import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load .env
# -----------------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def get_gemini_client():
    """Create Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(api_key=api_key)


# -----------------------------
# Dataset Summary
# -----------------------------
def create_dataset_summary(df):

    return f"""
Dataset Information

Rows: {df.shape[0]}
Columns: {df.shape[1]}

Column Names:
{list(df.columns)}

Data Types:
{df.dtypes.to_string()}

Missing Values:
{df.isnull().sum().to_string()}

Statistical Summary:
{df.describe(include='all').to_string()}
"""


# -----------------------------
# AI Insights
# -----------------------------
def generate_ai_insights(df):

    st.title(" AI Insights")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    client = get_gemini_client()

    if client is None:
        st.error(" GEMINI_API_KEY not found in the .env file.")
        return

    summary = create_dataset_summary(df)

    st.subheader("Dataset Summary")

    with st.expander("View Dataset Summary"):
        st.text(summary)

    if st.button(" Generate AI Insights"):

        with st.spinner("Analyzing dataset..."):

            prompt = f"""
You are an expert Data Analyst.

Analyze the following dataset summary.

{summary}

Generate:
1. Dataset Overview
2. Key Insights
3. Business Trends
4. Missing Value Analysis
5. Data Quality Issues
6. Recommendations

Return the answer in Markdown format.
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.success("✅ Analysis Completed")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ Error: {e}")
