DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS borrowers;

CREATE TABLE borrowers (
    member_id BIGINT PRIMARY KEY,
    residential_state VARCHAR(20),
    years_employment VARCHAR(50),
    home_ownership VARCHAR(50),
    annual_income NUMERIC(15,2),
    income_verified VARCHAR(50),
    dti_ratio NUMERIC(8,2),
    length_credit_history INT,
    num_total_credit_lines INT,
    num_open_credit_lines INT,
    num_open_credit_lines_1_year INT,
    revolving_balance NUMERIC(15,2),
    revolving_utilization_rate NUMERIC(8,2),
    num_derogatory_records INT,
    num_delinquency_2_years INT,
    num_chargeoff_1_year INT,
    num_inquiries_6_months INT
);

CREATE TABLE loans (
    loan_id BIGINT PRIMARY KEY,
    member_id BIGINT,
    loan_date DATE,
    purpose VARCHAR(100),
    is_joint_application VARCHAR(50),
    loan_amount NUMERIC(15,2),
    term VARCHAR(50),
    interest_rate NUMERIC(8,2),
    monthly_payment NUMERIC(15,2),
    grade VARCHAR(20),
    loan_status VARCHAR(50),
    CONSTRAINT fk_member
        FOREIGN KEY (member_id)
        REFERENCES borrowers(member_id)
);