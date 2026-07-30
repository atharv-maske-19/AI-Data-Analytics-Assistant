import streamlit as st

# ===============================
# Import Modules
# ===============================

from modules.upload import upload_dataset
from modules.preprocessing import data_cleaning
from modules.eda import perform_eda
from modules.visualization import visualization_dashboard
from modules.insights import generate_ai_insights
from modules.chatbot import chat_with_dataset
from modules.ml_models import machine_learning
from modules.forecasting import forecasting
from modules.report_generator import generate_report
from modules.settings import settings_page
from modules.copilot import analytics_copilot

# ===============================
# Page Configuration
# ===============================

st.set_page_config(
    page_title="AI-Powered Data Analytics Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# Session State
# ===============================

if "df" not in st.session_state:
    st.session_state.df = None

# ===============================
# Sidebar
# ===============================

st.sidebar.title("📊 AI Analytics Assistant")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Home",
        "📂 Upload Dataset",
        "🧹 Data Cleaning",
        "📊 Exploratory Data Analysis",
        "📈 Visualization",
        "🤖 AI Insights copilot",
        "🧠 Machine Learning",
        "📉 Forecasting",
        "📄 Reports",
        "⚙️ Settings",
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("🟢 System Ready")
st.sidebar.caption("Version 2.0")

# ===============================
# HOME
# ===============================

if menu == "🏠 Home":

    st.title("📊 AI-Powered Data Analytics Assistant")

    st.markdown("""
### Welcome 👋

Analyze your datasets using **Artificial Intelligence, Machine Learning,
Data Analytics, Forecasting and Generative AI**.

This platform lets you upload a dataset and generate insights with just a few clicks.
""")

    st.divider()

    if st.session_state.df is not None:

        df = st.session_state.df

        rows = df.shape[0]
        cols = df.shape[1]
        missing = int(df.isnull().sum().sum())
        duplicates = int(df.duplicated().sum())

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("📄 Rows", f"{rows:,}")
        c2.metric("📊 Columns", cols)
        c3.metric("❌ Missing", missing)
        c4.metric("📌 Duplicates", duplicates)

        st.divider()

        st.subheader("📂 Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

    else:

        st.info("📂 Please upload a dataset first.")

    st.divider()

    st.subheader("🚀 Available Modules")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):
            st.markdown("### 📂 Upload Dataset")
            st.write("Upload CSV & Excel datasets.")

        with st.container(border=True):
            st.markdown("### 🧹 Data Cleaning")
            st.write("Handle missing values and duplicates.")

        with st.container(border=True):
            st.markdown("### 📊 Exploratory Data Analysis")
            st.write("Generate descriptive statistics.")

        with st.container(border=True):
            st.markdown("### 📈 Visualization")
            st.write("Create interactive charts.")

        with st.container(border=True):
            st.markdown("### 🤖 AI Insights")
            st.write("Generate insights using Gemini AI.")

    with col2:

        with st.container(border=True):
            st.markdown("### 🧠 Machine Learning")
            st.write("Train ML models automatically.")

        with st.container(border=True):
            st.markdown("### 📉 Forecasting")
            st.write("Time Series Forecasting using Prophet.")

        with st.container(border=True):
            st.markdown("### 📄 Reports")
            st.write("Generate PDF analytics reports.")

        with st.container(border=True):
            st.markdown("### ⚙️ Settings")
            st.write("Application settings.")

    st.divider()

    st.subheader("📈 Project Status")

    s1, s2, s3 = st.columns(3)

    s1.success("✅ AI Ready")
    s2.success("✅ Machine Learning Ready")
    s3.success("✅ Forecasting Ready")

# ===============================
# Upload Dataset
# ===============================

elif menu == "📂 Upload Dataset":

    df = upload_dataset()

    if df is not None:
        st.session_state.df = df

# ===============================
# Data Cleaning
# ===============================

elif menu == "🧹 Data Cleaning":

    cleaned_df = data_cleaning(st.session_state.df)

    if cleaned_df is not None:
        st.session_state.df = cleaned_df

# ===============================
# Exploratory Data Analysis
# ===============================

elif menu == "📊 Exploratory Data Analysis":

    perform_eda(st.session_state.df)

# ===============================
# Visualization
# ===============================

elif menu == "📈 Visualization":

    visualization_dashboard(st.session_state.df)
    
# ===============================
# AI Insights
# ===============================

elif menu == "🤖 AI Insights copilot":

    analytics_copilot(st.session_state.df)

# ===============================
# Machine Learning
# ===============================

elif menu == "🧠 Machine Learning":

    machine_learning(st.session_state.df)

# ===============================
# Forecasting
# ===============================

elif menu == "📉 Forecasting":

    forecasting(st.session_state.df)

# ===============================
# Reports
# ===============================

elif menu == "📄 Reports":

    generate_report(st.session_state.df)

# ===============================
# Settings
# ===============================

elif menu == "⚙️ Settings":

    settings_page(st.session_state.df)

    st.divider()

    st.subheader("🖥 Application Information")

    c1, c2 = st.columns(2)

    with c1:
        st.info("""
**Application Name**

AI-Powered Data Analytics Assistant

**Version**

2.0

**Developer**

Atharv Maske
""")

    with c2:
        st.info("""
**Technologies**

• Python

• Streamlit

• Pandas

• Plotly

• Scikit-Learn

• Prophet

• Gemini AI
""")

    st.divider()

    st.subheader("📊 Current Dataset")

    if st.session_state.df is not None:

        df = st.session_state.df

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Rows", f"{df.shape[0]:,}")
        c2.metric("Columns", df.shape[1])
        c3.metric("Memory", f"{df.memory_usage().sum()/1024:.1f} KB")
        c4.metric("Missing", int(df.isnull().sum().sum()))

    else:

        st.warning("No dataset uploaded.")

    st.divider()

    if st.button("🗑 Clear Dataset", use_container_width=True):

        st.session_state.df = None
        st.success("Dataset cleared successfully.")
        st.rerun()

    st.divider()

    st.caption("© 2026 AI-Powered Data Analytics Assistant | Final Year Project")