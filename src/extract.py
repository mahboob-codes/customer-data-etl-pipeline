"""Extract: read the raw customer file into a Pandas table.

Extract only reads data. It does not fix duplicates, blank cells,
or bad email addresses. Those checks belong in the transform step.
"""

from pathlib import Path

import pandas as pd


def extract_customers(csv_path: Path) -> pd.DataFrame:
    """Read customer records from a CSV file.

    customer_id and phone stay as text. Phone numbers contain dashes,
    and reading the id as text avoids surprises before we check that
    every id is a whole number.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Raw customer file was not found: {csv_path}")

    customers = pd.read_csv(
        csv_path,
        dtype={
            "customer_id": "string",
            "first_name": "string",
            "last_name": "string",
            "email": "string",
            "phone": "string",
            "city": "string",
            "signup_date": "string",
            "status": "string",
        },
    )
    return customers
