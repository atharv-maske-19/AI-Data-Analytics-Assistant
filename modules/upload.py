import streamlit as st
import pandas as pd


def upload_dataset():
    st.title("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload a CSV or Excel file",
        type=["csv", "xlsx"]
    )

    if uploaded_file is None:
        st.info("Please upload a dataset to continue.")
        return None

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Dataset uploaded successfully!")

    st.divider()

    # Dataset Information
    st.subheader("📊 Dataset Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    st.divider()

    st.subheader("📋 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    st.subheader("📝 Column Names")
    st.write(list(df.columns))

    st.subheader("🔍 Data Types")
    st.dataframe(df.dtypes.astype(str).reset_index().rename(
        columns={"index": "Column", 0: "Data Type"}
    ))

    st.subheader("❌ Missing Values")
    st.dataframe(df.isnull().sum().reset_index().rename(
        columns={"index": "Column", 0: "Missing Values"}
    ))

    st.subheader("🔁 Duplicate Rows")
    st.write(df.duplicated().sum())

    st.subheader("📈 Statistical Summary")
    st.dataframe(df.describe(include="all"))

    return df