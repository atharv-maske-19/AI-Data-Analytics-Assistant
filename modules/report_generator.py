import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


def generate_report(df):

    st.title(" AI Report Generator")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    rows, cols = df.shape
    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    st.subheader("Report Preview")

    st.write(f"Rows : {rows}")
    st.write(f"Columns : {cols}")
    st.write(f"Missing Values : {missing}")
    st.write(f"Duplicate Rows : {duplicates}")

    if st.button(" Generate PDF Report"):

        os.makedirs("reports", exist_ok=True)

        pdf_path = "reports/AI_Analytics_Report.pdf"

        doc = SimpleDocTemplate(pdf_path)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b><font size=18>AI-Powered Data Analytics Report</font></b>",
                styles["Title"],
            )
        )

        story.append(
            Paragraph(
                f"Generated On : {datetime.now().strftime('%d-%m-%Y %H:%M')}",
                styles["Normal"],
            )
        )

        story.append(Paragraph("<br/><br/>", styles["Normal"]))

        story.append(
            Paragraph("<b>Dataset Summary</b>", styles["Heading2"])
        )

        story.append(Paragraph(f"Rows : {rows}", styles["Normal"]))
        story.append(Paragraph(f"Columns : {cols}", styles["Normal"]))
        story.append(Paragraph(f"Missing Values : {missing}", styles["Normal"]))
        story.append(Paragraph(f"Duplicate Rows : {duplicates}", styles["Normal"]))

        story.append(Paragraph("<br/>", styles["Normal"]))

        story.append(
            Paragraph("<b>Column Data Types</b>", styles["Heading2"])
        )

        for col in df.columns:
            story.append(
                Paragraph(
                    f"{col} : {df[col].dtype}",
                    styles["Normal"],
                )
            )

        story.append(Paragraph("<br/>", styles["Normal"]))

        story.append(
            Paragraph("<b>Statistical Summary</b>", styles["Heading2"])
        )

        summary = df.describe(include="all").fillna("").to_string()

        for line in summary.split("\n"):
            story.append(Paragraph(line, styles["Code"]))

        story.append(Paragraph("<br/>", styles["Normal"]))

        story.append(
            Paragraph(
                "<b>Thank you for using AI Data Analytics Assistant.</b>",
                styles["Heading2"],
            )
        )

        doc.build(story)

        st.success(" PDF Report Generated Successfully!")

        with open(pdf_path, "rb") as file:

            st.download_button(
                "⬇ Download Report",
                file,
                file_name="AI_Analytics_Report.pdf",
                mime="application/pdf",
            )
