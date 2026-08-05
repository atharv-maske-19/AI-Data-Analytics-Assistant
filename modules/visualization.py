import streamlit as st
import pandas as pd
import plotly.express as px


def visualization_dashboard(df):

    st.title(" Interactive Visualization Dashboard")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()
    all_cols = df.columns.tolist()

    chart = st.selectbox(
        "Select Chart Type",
        [
            "Bar Chart",
            "Line Chart",
            "Scatter Plot",
            "Histogram",
            "Box Plot",
            "Pie Chart",
            "Correlation Heatmap"
        ]
    )

    st.divider()

    if chart == "Bar Chart":

        x = st.selectbox("X-axis", all_cols)
        y = st.selectbox("Y-axis", numeric_cols)

        fig = px.bar(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Line Chart":

        x = st.selectbox("X-axis", all_cols)
        y = st.selectbox("Y-axis", numeric_cols)

        fig = px.line(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Scatter Plot":

        x = st.selectbox("X-axis", numeric_cols)
        y = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        color = st.selectbox("Color", categorical_cols if categorical_cols else all_cols)

        fig = px.scatter(df, x=x, y=y, color=color)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Histogram":

        column = st.selectbox("Column", numeric_cols)

        fig = px.histogram(df, x=column)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Box Plot":

        x = st.selectbox("Category", categorical_cols if categorical_cols else all_cols)
        y = st.selectbox("Numeric Column", numeric_cols)

        fig = px.box(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Pie Chart":

        names = st.selectbox("Category", categorical_cols if categorical_cols else all_cols)

        fig = px.pie(df, names=names)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Correlation Heatmap":

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Blues"
        )

        st.plotly_chart(fig, use_container_width=True)
