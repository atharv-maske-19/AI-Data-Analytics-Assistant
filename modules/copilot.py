import streamlit as st
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# =====================================================
# Load Gemini API
# =====================================================

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)


# =====================================================
# Dataset Summary
# =====================================================

def create_summary(df):

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    summary = f"""
Dataset Information

Rows : {df.shape[0]}
Columns : {df.shape[1]}

Numeric Columns

{numeric_cols}

Categorical Columns

{categorical_cols}

Missing Values

{df.isnull().sum().to_string()}

Duplicate Rows

{df.duplicated().sum()}

Statistics

{df.describe(include='all').fillna('').to_string()}
"""

    return summary


# =====================================================
# AI Analytics Copilot
# =====================================================

def analytics_copilot(df):

    st.title(" AI Analytics Copilot")

    st.caption("Analyze your dataset with Google Gemini AI")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    if client is None:
        st.error(" GEMINI_API_KEY not found.")
        return

    # ============================================
    # KPI Cards
    # ============================================

    rows = df.shape[0]
    cols = df.shape[1]
    missing = int(df.isnull().sum().sum())
    duplicate = int(df.duplicated().sum())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(" Rows", f"{rows:,}")
    c2.metric(" Columns", cols)
    c3.metric(" Missing", missing)
    c4.metric(" Duplicate", duplicate)

    st.divider()

    # ============================================
    # Dataset Preview
    # ============================================

    st.subheader(" Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.divider()

    # ============================================
    # Quick Actions
    # ============================================

    st.subheader(" AI Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(" Dataset Summary", use_container_width=True):
            st.session_state.question = "Summarize this dataset."

        if st.button(" Cleaning Suggestions", use_container_width=True):
            st.session_state.question = "Suggest data cleaning improvements."

    with col2:

        if st.button(" Business Insights", use_container_width=True):
            st.session_state.question = "Generate business insights."

        if st.button(" Best ML Model", use_container_width=True):
            st.session_state.question = "Recommend the best machine learning model."

    with col3:

        if st.button(" Forecast Recommendation", use_container_width=True):
            st.session_state.question = "Should I perform forecasting?"

        if st.button("📄 Executive Summary", use_container_width=True):
            st.session_state.question = "Generate an executive summary."

    st.divider()

    # ============================================
    # Ask AI
    # ============================================

    default_question = st.session_state.get("question", "")

    question = st.text_area(
        "💬 Ask anything about your dataset",
        value=default_question,
        height=140,
        placeholder="Example : Which city has the highest sales?"
    )
    
    # ============================================
    # Ask AI Button
    # ============================================

    if st.button(" Ask AI", use_container_width=True):

        if question.strip() == "":
            st.warning(" Please enter a question.")
            return

        with st.spinner(" Gemini is analyzing your dataset..."):

            summary = create_summary(df)

            prompt = f"""
You are a Senior Data Scientist, Business Analyst, and Machine Learning Engineer.

Analyze the following dataset.

Dataset Summary:

{summary}

User Question:

{question}

Provide your answer professionally in Markdown.

Your response should include (whenever applicable):

# Executive Summary

# Key Insights

# Business Trends

# Missing Value Analysis

# Data Quality Assessment

# Best Machine Learning Algorithm

# Forecast Recommendation

# Actionable Business Recommendations

# Final Conclusion

Keep the answer detailed, clear, and professional.
"""

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                answer = response.text

                st.success(" AI Analysis Completed")

                st.divider()

                st.subheader(" AI Response")

                st.markdown(answer)

                st.divider()

                # ============================================
                # Download Response
                # ============================================

                st.download_button(
                    label=" Download AI Report",
                    data=answer,
                    file_name="AI_Analysis_Report.md",
                    mime="text/markdown",
                    use_container_width=True
                )

                # ============================================
                # Save Chat History
                # ============================================

                if "history" not in st.session_state:
                    st.session_state.history = []

                st.session_state.history.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )

            except Exception as e:

                st.error(f" {e}")

    # ============================================
    # Chat History
    # ============================================

    if "history" in st.session_state:

        if len(st.session_state.history) > 0:

            st.divider()

            st.subheader(" Previous Questions")

            for i, item in enumerate(reversed(st.session_state.history), start=1):

                with st.expander(f"Question {i}"):

                    st.markdown(f"**Question:** {item['question']}")

                    st.markdown("---")

                    st.markdown(item["answer"])

    # ============================================
    # Clear History
    # ============================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🗑 Clear History", use_container_width=True):

            st.session_state.history = []
            st.success("History Cleared")
            st.rerun()

    with col2:

        if st.button(" Reset Question", use_container_width=True):

            st.session_state.question = ""
            st.rerun()
