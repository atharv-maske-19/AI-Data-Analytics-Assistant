import streamlit as st
import pandas as pd


def data_cleaning(df):

    st.title("🧹 Data Cleaning")

    if df is None:
        st.warning("⚠️ Please upload a dataset first.")
        return None

    cleaned_df = df.copy()

    st.subheader("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", cleaned_df.shape[0])
    col2.metric("Columns", cleaned_df.shape[1])
    col3.metric("Missing Values", cleaned_df.isnull().sum().sum())

    st.divider()

    # Missing Values Table
    st.subheader("❌ Missing Values")

    missing_df = cleaned_df.isnull().sum().reset_index()
    missing_df.columns = ["Column", "Missing Values"]

    st.dataframe(missing_df, use_container_width=True)

    # Duplicate Rows
    st.divider()

    duplicate_rows = cleaned_df.duplicated().sum()

    st.write(f"Duplicate Rows : **{duplicate_rows}**")

    if st.button("Remove Duplicate Rows"):

        cleaned_df = cleaned_df.drop_duplicates()

        st.success("Duplicate rows removed successfully.")

    st.divider()

    # Missing Value Handling
    st.subheader("Handle Missing Values")

    option = st.selectbox(
        "Choose Cleaning Method",
        [
            "None",
            "Drop Missing Rows",
            "Fill Numeric Columns with Mean",
            "Fill Numeric Columns with Median",
            "Fill All Columns with Mode"
        ]
    )

    if st.button("Apply Cleaning"):

        if option == "Drop Missing Rows":

            cleaned_df = cleaned_df.dropna()

        elif option == "Fill Numeric Columns with Mean":

            numeric_cols = cleaned_df.select_dtypes(include="number").columns

            cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(
                cleaned_df[numeric_cols].mean()
            )

        elif option == "Fill Numeric Columns with Median":

            numeric_cols = cleaned_df.select_dtypes(include="number").columns

            cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(
                cleaned_df[numeric_cols].median()
            )

        elif option == "Fill All Columns with Mode":

            cleaned_df = cleaned_df.fillna(cleaned_df.mode().iloc[0])

        st.success("Cleaning Completed Successfully!")

    st.divider()

    st.subheader("📄 Cleaned Dataset")

    st.dataframe(cleaned_df, use_container_width=True)

    csv = cleaned_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Cleaned Dataset",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

    return cleaned_df