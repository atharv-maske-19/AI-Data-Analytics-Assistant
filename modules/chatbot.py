import streamlit as st
import pandas as pd
import os

from dotenv import load_dotenv
from google import genai
from pathlib import Path

# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)


def chat_with_dataset(df):

    st.title("💬 Chat with Your Dataset")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    if client is None:
        st.error("Gemini API Key not found.")
        return

    st.success("Dataset Loaded Successfully")

    question = st.text_input(
        "Ask any question about your dataset"
    )

    if st.button("Ask AI"):

        if question == "":
            st.warning("Please enter a question.")
            return

        sample = df.head(100).to_string()

        prompt = f"""
You are an expert Data Analyst.

Dataset Sample:

{sample}

User Question:

{question}

Answer only using the dataset.

If the answer cannot be determined from the dataset,
say "I cannot determine that from the uploaded data."
"""

        with st.spinner("Thinking..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.markdown("## 🤖 Answer")

        st.write(response.text)