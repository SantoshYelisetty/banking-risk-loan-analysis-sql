CREATE OR REPLACE VIEW vw_credit_risk_reporting AS
SELECT
    l.loan_id,
    l.member_id,
    l.loan_date,
    l.purpose,
    l.loan_amount,
    l.term,
    l.interest_rate,
    l.monthly_payment,
    l.grade,
    LEFT(l.grade, 1) AS grade_band,
    l.loan_status,
    b.residential_state,
    b.home_ownership,
    b.annual_income,
    b.dti_ratio,
    b.revolving_utilization_rate,
    b.num_delinquency_2_years,
    b.num_chargeoff_1_year,
    CASE
        WHEN b.dti_ratio < 10 THEN 'Low DTI'
        WHEN b.dti_ratio BETWEEN 10 AND 25 THEN 'Medium DTI'
        ELSE 'High DTI'
    END AS dti_group,
    CASE
        WHEN l.loan_status = 'Charged Off'
          OR b.dti_ratio > 25
          OR b.num_delinquency_2_years > 0
          OR b.num_chargeoff_1_year > 0
        THEN 'High Risk'
        ELSE 'Normal Risk'
    END AS risk_flag
FROM loans l
JOIN borrowers b
    ON l.member_id = b.member_id;