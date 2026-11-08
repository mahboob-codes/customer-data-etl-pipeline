"""Load: write the valid customer records into SQLite.

SQLite is a database stored in one file. Pandas can create the table
and insert the rows. Replacing the table on each run lets you execute
the pipeline again without primary-key clashes.
"""

import sqlite3
from pathlib import Path

import pandas as pd


def load_customers(customers: pd.DataFrame, database_path: Path, table_name: str) -> int:
    """Create the database file if needed, then replace the customers table."""
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
        customers.to_sql(table_name, connection, if_exists="replace", index=False)
        row_count = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    return int(row_count)
