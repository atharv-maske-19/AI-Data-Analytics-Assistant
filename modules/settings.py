import streamlit as st
import pandas as pd


def settings_page(df):

    st.title("⚙️ Settings")

    st.markdown("---")

    # ======================================
    # Project Information
    # ======================================
    st.subheader("👤 Project Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Project Name:** AI-Powered Data Analytics Assistant")
        st.write("**Developer:** Atharv Maske")
        st.write("**Version:** 1.0")

    with col2:
        st.write("**Domain:** Data Analytics & Data Science")
        st.write("**Framework:** Streamlit")
        st.write("**Status:** ✅ Active")

    st.markdown("---")

    # ======================================
    # Dataset Information
    # ======================================
    st.subheader("📊 Dataset Information")

    if df is not None:

        rows, cols = df.shape
        missing = int(df.isnull().sum().sum())
        duplicates = int(df.duplicated().sum())
        memory = round(df.memory_usage(deep=True).sum() / 1024, 2)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Rows", rows)
        c2.metric("Columns", cols)
        c3.metric("Missing Values", missing)
        c4.metric("Duplicates", duplicates)

        st.metric("Memory Usage (KB)", memory)

    else:
        st.warning("⚠️ No dataset uploaded.")

    st.markdown("---")

    # ======================================
    # Download Dataset
    # ======================================
    st.subheader("📥 Export Dataset")

    if df is not None:

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download Current Dataset",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

    else:
        st.info("Upload a dataset to enable downloading.")

    st.markdown("---")

    # ======================================
    # Clear Dataset
    # ======================================
    st.subheader("🗑 Dataset Management")

    if st.button("🗑 Clear Uploaded Dataset"):

        st.session_state.df = None

        st.success("✅ Dataset cleared successfully.")

        st.rerun()

    st.markdown("---")

    # ======================================
    # Theme Selection
    # ======================================
    st.subheader("🎨 Appearance")

    theme = st.selectbox(
        "Choose Theme",
        [
            "Light",
            "Dark",
            "System Default"
        ]
    )

    st.info(f"Current Theme : {theme}")

    st.markdown("---")

    # ======================================
    # AI Configuration
    # ======================================
    st.subheader("🤖 AI Configuration")

    st.success("Google Gemini Connected")

    st.write("**Model:** Gemini 2.5 Flash")
    st.write("**Provider:** Google AI")
    st.write("**Status:** Connected ✅")

    st.markdown("---")

    # ======================================
    # Technology Stack
    # ======================================
    st.subheader("💻 Technology Stack")

    tech = pd.DataFrame({
        "Technology": [
            "Python",
            "Streamlit",
            "Pandas",
            "Plotly",
            "Scikit-Learn",
            "Prophet",
            "Google Gemini AI",
            "ReportLab"
        ]
    })

    st.dataframe(tech, use_container_width=True)

    st.markdown("---")

    # ======================================
    # About
    # ======================================
    st.subheader("ℹ️ About")

    st.info("""
AI-Powered Data Analytics Assistant is an intelligent analytics platform that helps users:

• Upload CSV & Excel datasets

• Clean and preprocess data

• Perform Exploratory Data Analysis

• Generate Interactive Visualizations

• Generate AI Insights

• Chat with datasets using Gemini AI

• Train Machine Learning Models

• Perform Time Series Forecasting

• Generate PDF Reports

Designed as a Final Year Project for Artificial Intelligence & Data Science.
""")

    st.markdown("---")

    st.success("🎉 AI-Powered Data Analytics Assistant Version 1.0")