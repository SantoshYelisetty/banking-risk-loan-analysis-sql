from pathlib import Path
import re
import pandas as pd


# -----------------------------
# 1. File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

raw_dir = BASE_DIR / "dataset" / "raw"
processed_dir = BASE_DIR / "dataset" / "processed"
processed_dir.mkdir(parents=True, exist_ok=True)

loan_path = raw_dir / "Loan.txt"
borrower_path = raw_dir / "Borrower.txt"

loans_output_path = processed_dir / "loans_clean.csv"
borrowers_output_path = processed_dir / "borrowers_clean.csv"


# -----------------------------
# 2. Helper functions
# -----------------------------
def camel_to_snake(name):
    """
    Converts names like loanAmount, interestRate, numOpenCreditLines1Year
    into loan_amount, interest_rate, num_open_credit_lines_1_year.
    """
    name = name.strip()

    # Convert camelCase to snake_case
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)

    # Add underscore between letters and numbers
    name = re.sub(r"([a-zA-Z])([0-9])", r"\1_\2", name)
    name = re.sub(r"([0-9])([a-zA-Z])", r"\1_\2", name)

    # Clean final name
    name = name.lower()
    name = name.replace(" ", "_")
    name = re.sub(r"_+", "_", name)

    return name


def clean_column_names(df):
    df.columns = [camel_to_snake(col) for col in df.columns]
    return df


def convert_whole_number_columns_to_int(df):
    """
    Converts values like 9.0 into 9 for whole-number columns.
    """
    for col in df.columns:
        if col in ["loan_date"]:
            continue

        numeric_col = pd.to_numeric(df[col], errors="coerce")
        non_null_values = numeric_col.dropna()

        if len(non_null_values) > 0 and (non_null_values % 1 == 0).all():
            df[col] = numeric_col.astype("Int64")

    return df


# -----------------------------
# 3. Load raw data
# Important: Microsoft files are tab-separated
# -----------------------------
loans = pd.read_csv(loan_path, sep="\t")
borrowers = pd.read_csv(borrower_path, sep="\t")

print("Raw loan columns:")
print(loans.columns.tolist())

print("Raw borrower columns:")
print(borrowers.columns.tolist())


# -----------------------------
# 4. Clean column names
# -----------------------------
loans = clean_column_names(loans)
borrowers = clean_column_names(borrowers)

print("Cleaned loan columns:")
print(loans.columns.tolist())

print("Cleaned borrower columns:")
print(borrowers.columns.tolist())


# -----------------------------
# 5. Rename date column to loan_date
# -----------------------------
if "date" in loans.columns:
    loans = loans.rename(columns={"date": "loan_date"})


# -----------------------------
# 6. Convert loan_date timestamp to normal date
# -----------------------------
if "loan_date" in loans.columns:
    print("Raw loan_date values before conversion:")
    print(loans["loan_date"].head())

    # Convert date column to string and keep only digits
    loan_timestamp = (
        loans["loan_date"]
        .astype(str)
        .str.strip()
        .str.extract(r"(\d+)", expand=False)
    )

    loan_timestamp = pd.to_numeric(loan_timestamp, errors="coerce")

    print("Numeric timestamp preview:")
    print(loan_timestamp.head())

    # The Microsoft loan date is stored as Unix timestamp in microseconds
    loans["loan_date"] = pd.to_datetime(
        loan_timestamp,
        unit="us",
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    print("Loan date conversion completed.")
    print(loans[["loan_date"]].head())

else:
    print("loan_date column still not found.")
    print(loans.columns.tolist())

# -----------------------------
# 7. Convert whole-number columns
# -----------------------------
loans = convert_whole_number_columns_to_int(loans)
borrowers = convert_whole_number_columns_to_int(borrowers)


# -----------------------------
# 8. Save processed CSV files
# -----------------------------
borrowers.to_csv(borrowers_output_path, index=False)
loans.to_csv(loans_output_path, index=False)

print("Cleaned borrowers dataset saved successfully:")
print(borrowers_output_path)

print("Cleaned loans dataset saved successfully:")
print(loans_output_path)

print("Loan date preview:")
print(loans[["loan_date"]].head())

print("Loan data preview:")
print(loans.head())

print("Borrower data preview:")
print(borrowers.head())