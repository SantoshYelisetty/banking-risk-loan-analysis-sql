-- 1. Loan status summary
SELECT
    loan_status,
    COUNT(*) AS total_loans,
    ROUND(SUM(loan_amount), 2) AS total_loan_amount,
    ROUND(AVG(loan_amount), 2) AS average_loan_amount
FROM loans
GROUP BY loan_status
ORDER BY total_loans DESC;

-- 2. Risk grade default rate
SELECT
    LEFT(grade, 1) AS grade_band,
    COUNT(*) AS total_loans,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) AS charged_off_loans,
    ROUND(
        100.0 * SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS charged_off_rate_percentage
FROM loans
GROUP BY LEFT(grade, 1)
ORDER BY grade_band;

-- 3. Loan purpose risk analysis
SELECT
    purpose,
    COUNT(*) AS total_loans,
    ROUND(SUM(loan_amount), 2) AS total_loan_amount,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) AS charged_off_loans,
    ROUND(
        100.0 * SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS charged_off_rate_percentage
FROM loans
GROUP BY purpose
ORDER BY charged_off_rate_percentage DESC;


-- 4. Debt-to-income risk grouping
SELECT
    CASE
        WHEN dti_ratio < 10 THEN 'Low DTI'
        WHEN dti_ratio BETWEEN 10 AND 25 THEN 'Medium DTI'
        ELSE 'High DTI'
    END AS dti_group,
    COUNT(*) AS borrower_count,
    ROUND(AVG(annual_income), 2) AS average_income,
    ROUND(AVG(dti_ratio), 2) AS average_dti
FROM borrowers
GROUP BY dti_group
ORDER BY borrower_count DESC;

-- 5. Borrower profile and loan risk
SELECT
    b.home_ownership,
    COUNT(l.loan_id) AS total_loans,
    ROUND(AVG(b.annual_income), 2) AS average_income,
    ROUND(AVG(b.dti_ratio), 2) AS average_dti,
    ROUND(AVG(l.loan_amount), 2) AS average_loan_amount,
    SUM(CASE WHEN l.loan_status = 'Charged Off' THEN 1 ELSE 0 END) AS charged_off_loans
FROM borrowers b
JOIN loans l
    ON b.member_id = l.member_id
GROUP BY b.home_ownership
ORDER BY charged_off_loans DESC;


-- 6. High-risk borrower list
SELECT
    l.loan_id,
    l.member_id,
    l.loan_amount,
    l.grade,
    l.loan_status,
    b.annual_income,
    b.dti_ratio,
    b.revolving_utilization_rate,
    b.num_delinquency_2_years,
    b.num_chargeoff_1_year
FROM loans l
JOIN borrowers b
    ON l.member_id = b.member_id
WHERE l.loan_status = 'Charged Off'
   OR b.dti_ratio > 25
   OR b.num_delinquency_2_years > 0
ORDER BY b.dti_ratio DESC, l.loan_amount DESC
LIMIT 100;