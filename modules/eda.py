import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def perform_eda(df):

    st.title(" Exploratory Data Analysis")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    st.subheader("Dataset Shape")

    col1, col2 = st.columns(2)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    st.divider()

    st.subheader("Data Types")
    st.dataframe(df.dtypes.astype(str))

    st.divider()

    st.subheader("Statistical Summary")
    st.dataframe(df.describe(include="all"))

    st.divider()

    st.subheader("Missing Values")

    missing = df.isnull().sum()

    st.dataframe(missing)

    st.divider()

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        st.info("No numeric columns available.")
        return

    # Histogram
    st.subheader("Histogram")

    column = st.selectbox(
        "Select Numeric Column",
        numeric_df.columns
    )

    fig, ax = plt.subplots(figsize=(8,4))
    sns.histplot(df[column], kde=True, ax=ax)
    st.pyplot(fig)

    # Box Plot
    st.subheader("Box Plot")

    fig2, ax2 = plt.subplots(figsize=(8,4))
    sns.boxplot(x=df[column], ax=ax2)
    st.pyplot(fig2)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")

    fig3, ax3 = plt.subplots(figsize=(10,6))

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="Blues",
        ax=ax3
    )

    st.pyplot(fig3)

    # Categorical Charts
    categorical = df.select_dtypes(include="object").columns

    if len(categorical) > 0:

        st.subheader("Categorical Distribution")

        cat = st.selectbox(
            "Select Categorical Column",
            categorical
        )

        st.bar_chart(df[cat].value_counts())
