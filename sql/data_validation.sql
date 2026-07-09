-- Row counts
SELECT COUNT(*) AS borrower_count FROM borrowers;
SELECT COUNT(*) AS loan_count FROM loans;

-- Missing IDs
SELECT COUNT(*) AS missing_member_id_borrowers
FROM borrowers
WHERE member_id IS NULL;

SELECT COUNT(*) AS missing_member_id_loans
FROM loans
WHERE member_id IS NULL;

-- Duplicate check
SELECT member_id, COUNT(*)
FROM borrowers
GROUP BY member_id
HAVING COUNT(*) > 1;

SELECT loan_id, COUNT(*)
FROM loans
GROUP BY loan_id
HAVING COUNT(*) > 1;

-- Loan records without borrower match
SELECT COUNT(*) AS unmatched_loans
FROM loans l
LEFT JOIN borrowers b
    ON l.member_id = b.member_id
WHERE b.member_id IS NULL;