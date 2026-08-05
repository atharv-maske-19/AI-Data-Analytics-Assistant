import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.express as px


def forecasting(df):

    st.title(" Time Series Forecasting")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    # ----------------------------
    # Detect Date Columns
    # ----------------------------
    date_cols = []

    for col in df.columns:

        # Check if column name contains Date or Time
        if "date" in col.lower() or "time" in col.lower():
            date_cols.append(col)
            continue

        # Check only object/string columns
        if df[col].dtype == "object":
            try:
                temp = pd.to_datetime(df[col], errors="coerce")

                if temp.notna().sum() > len(df) * 0.8:
                    date_cols.append(col)

            except Exception:
                pass

    # Remove duplicates
    date_cols = list(dict.fromkeys(date_cols))

    if len(date_cols) == 0:
        st.error("❌ No valid date column found.")
        return

    # ----------------------------
    # Select Date & Target
    # ----------------------------
    date_col = st.selectbox("📅 Select Date Column", date_cols)

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if len(numeric_cols) == 0:
        st.error(" No numeric columns found.")
        return

    target = st.selectbox(" Select Target Column", numeric_cols)

    future_days = st.slider(
        "Forecast Days",
        min_value=7,
        max_value=365,
        value=30
    )

    # ----------------------------
    # Generate Forecast
    # ----------------------------
    if st.button(" Generate Forecast"):

        data = df[[date_col, target]].copy()

        data.columns = ["ds", "y"]

        # Convert date
        data["ds"] = pd.to_datetime(data["ds"], errors="coerce")

        # Convert target
        data["y"] = pd.to_numeric(data["y"], errors="coerce")

        # Remove missing values
        data = data.dropna()

        st.write(" Valid Rows:", len(data))

        if len(data) < 2:
            st.error(" Not enough valid rows for forecasting.")
            return

        # Sort by date
        data = data.sort_values("ds")

        # Train Prophet
        model = Prophet()

        model.fit(data)

        future = model.make_future_dataframe(periods=future_days)

        forecast = model.predict(future)

        st.success("Forecast Generated Successfully!")

        st.subheader("Forecast Results")

        st.dataframe(
            forecast[
                ["ds", "yhat", "yhat_lower", "yhat_upper"]
            ]
        )

        fig = px.line(
            forecast,
            x="ds",
            y="yhat",
            title="Forecast"
        )

        st.plotly_chart(fig, use_container_width=True)

        csv = forecast.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Forecast CSV",
            data=csv,
            file_name="forecast.csv",
            mime="text/csv"
        )
