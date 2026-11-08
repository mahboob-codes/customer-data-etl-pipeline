"""Transform: clean customer records and separate the bad ones.

The rules used here are:

1. Trim extra spaces and make email addresses lowercase.
2. Treat a repeated customer_id as a duplicate. The first row is kept.
3. Reject a row when customer_id, first_name, last_name, or email is blank.
4. Reject a row when the email does not look like name@company.com.
5. Keep a row when only phone, city, or signup_date is blank.
6. Fill a blank status with the word "unknown".
"""

import re

import pandas as pd

# Local part, one @, a domain, a dot, then a short ending such as com.
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

STRING_COLUMNS = [
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "phone",
    "city",
    "signup_date",
    "status",
]


def _clean_text_columns(customers: pd.DataFrame) -> pd.DataFrame:
    """Strip spaces. Turn blank strings into real missing values."""
    cleaned = customers.copy()
    cleaned.columns = [column.strip().lower() for column in cleaned.columns]

    for column in STRING_COLUMNS:
        cleaned[column] = cleaned[column].str.strip()
        cleaned[column] = cleaned[column].replace("", pd.NA)

    cleaned["email"] = cleaned["email"].str.lower()
    return cleaned


def _is_valid_email(email: object) -> bool:
    """Return True when the value matches the email pattern."""
    if pd.isna(email):
        return False
    return EMAIL_PATTERN.fullmatch(str(email)) is not None


def _rejection_reason(row: pd.Series) -> str:
    """Build a short reason string. An empty string means the row is valid."""
    reasons = []

    if pd.isna(row["customer_id"]) or not str(row["customer_id"]).isdigit():
        reasons.append("missing or invalid customer_id")
    if pd.isna(row["first_name"]):
        reasons.append("missing first_name")
    if pd.isna(row["last_name"]):
        reasons.append("missing last_name")

    if pd.isna(row["email"]):
        reasons.append("missing email")
    elif not _is_valid_email(row["email"]):
        reasons.append("invalid email")

    if pd.notna(row["signup_date"]):
        parsed_date = pd.to_datetime(row["signup_date"], format="%Y-%m-%d", errors="coerce")
        if pd.isna(parsed_date):
            reasons.append("invalid signup_date")

    return "; ".join(reasons)


def transform_customers(customers: pd.DataFrame) -> dict:
    """Clean the extract and split it into valid, rejected, and duplicate rows.

    The returned dictionary carries the two tables plus the counts the
    quality report needs. Duplicate rows are counted on their own, so:

        total records = valid + rejected + duplicates
    """
    cleaned = _clean_text_columns(customers)
    duplicate_mask = cleaned.duplicated(subset=["customer_id"], keep="first")

    duplicates = cleaned.loc[duplicate_mask].copy()
    duplicates["reject_reason"] = "duplicate customer_id"

    unique_rows = cleaned.loc[~duplicate_mask].copy()
    unique_rows["reject_reason"] = unique_rows.apply(_rejection_reason, axis=1)

    rejected = unique_rows.loc[unique_rows["reject_reason"] != ""].copy()
    valid = unique_rows.loc[unique_rows["reject_reason"] == ""].copy()

    valid = valid.drop(columns=["reject_reason"])
    valid["customer_id"] = valid["customer_id"].astype(int)
    valid["status"] = valid["status"].fillna("unknown")

    review_rows = pd.concat([duplicates, rejected], ignore_index=True)

    return {
        "valid": valid,
        "rejected": review_rows,
        "total_records": int(len(cleaned)),
        "valid_records": int(len(valid)),
        "rejected_records": int(len(rejected)),
        "duplicate_records": int(len(duplicates)),
    }
