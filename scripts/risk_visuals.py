import os
from pathlib import Path

import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing. Please create a .env file.")

engine = create_engine(database_url)

queries = {
    "loan_status_summary": """
        SELECT
            loan_status,
            COUNT(*) AS total_loans,
            ROUND(SUM(loan_amount), 2) AS total_loan_amount
        FROM loans
        GROUP BY loan_status
        ORDER BY total_loans DESC;
    """,

    "grade_default_rate": """
        SELECT
            LEFT(grade, 1) AS grade_band,
            COUNT(*) AS total_loans,
            SUM(CASE WHEN loan_status = 'Default' THEN 1 ELSE 0 END) AS default_loans,
            ROUND(
                100.0 * SUM(CASE WHEN loan_status = 'Default' THEN 1 ELSE 0 END) / COUNT(*),
                2
            ) AS default_rate_percentage
        FROM loans
        GROUP BY LEFT(grade, 1)
        ORDER BY grade_band;
    """,

    "dti_group_summary": """
        SELECT
            dti_group,
            COUNT(*) AS borrower_count,
            ROUND(AVG(annual_income), 2) AS average_income,
            ROUND(AVG(dti_ratio), 2) AS average_dti
        FROM vw_credit_risk_reporting
        GROUP BY dti_group
        ORDER BY borrower_count DESC;
    """
}

dataframes = {}

for name, query in queries.items():
    df = pd.read_sql(query, engine)
    dataframes[name] = df
    df.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)

# Visual 1: Loan status summary
fig1 = px.bar(
    dataframes["loan_status_summary"],
    x="loan_status",
    y="total_loans",
    text="total_loans",
    title="Loan Status Summary",
    labels={
        "loan_status": "Loan Status",
        "total_loans": "Total Loans"
    }
)
fig1.update_traces(textposition="outside")
fig1.update_layout(
    template="plotly_white",
    xaxis_title="Loan Status",
    yaxis_title="Total Loans"
)
fig1.write_image(SCREENSHOT_DIR / "loan_status_summary.png", scale=2)
fig1.write_html(OUTPUT_DIR / "loan_status_summary.html")

# Visual 2: Default rate by grade band
fig2 = px.bar(
    dataframes["grade_default_rate"],
    x="grade_band",
    y="default_rate_percentage",
    text="default_rate_percentage",
    title="Default Rate by Risk Grade",
    labels={
        "grade_band": "Risk Grade",
        "default_rate_percentage": "Default Rate (%)"
    }
)
fig2.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)
fig2.update_layout(
    template="plotly_white",
    xaxis_title="Risk Grade",
    yaxis_title="Default Rate (%)"
)
fig2.write_image(SCREENSHOT_DIR / "default_rate_by_grade.png", scale=2)
fig2.write_html(OUTPUT_DIR / "default_rate_by_grade.html")

# Visual 3: DTI group summary
fig3 = px.pie(
    dataframes["dti_group_summary"],
    names="dti_group",
    values="borrower_count",
    title="Borrower Distribution by DTI Group"
)
fig3.update_traces(textinfo="percent+label")
fig3.update_layout(template="plotly_white")
fig3.write_image(SCREENSHOT_DIR / "dti_group_distribution.png", scale=2)
fig3.write_html(OUTPUT_DIR / "dti_group_distribution.html")

print("Risk visuals created successfully.")