"""Run the four ETL stages in order: extract, transform, load, report."""

from src.config import (
    CLEAN_CSV_PATH,
    DATABASE_PATH,
    RAW_CSV_PATH,
    REJECTED_CSV_PATH,
    REPORT_PATH,
    TABLE_NAME,
)
from src.extract import extract_customers
from src.load import load_customers
from src.quality_report import write_quality_report
from src.transform import transform_customers


def run_pipeline() -> dict:
    """Execute one full pass over the sample customer file."""
    print("1. Extract: reading raw customer records")
    raw_customers = extract_customers(RAW_CSV_PATH)
    print(f"   Rows read: {len(raw_customers)}")

    print("2. Transform: removing duplicates and checking each record")
    result = transform_customers(raw_customers)

    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    result["valid"].to_csv(CLEAN_CSV_PATH, index=False)
    result["rejected"].to_csv(REJECTED_CSV_PATH, index=False)
    print(f"   Valid rows written to: {CLEAN_CSV_PATH}")
    print(f"   Rows held for review: {REJECTED_CSV_PATH}")

    print("3. Load: writing valid records to SQLite")
    loaded_rows = load_customers(result["valid"], DATABASE_PATH, TABLE_NAME)
    print(f"   Rows in {TABLE_NAME}: {loaded_rows}")
    print(f"   Database file: {DATABASE_PATH}")

    print("4. Report: writing the data quality summary")
    report = write_quality_report(result, RAW_CSV_PATH, REPORT_PATH)
    print(f"   Report file: {REPORT_PATH}")
    print()
    print(report)

    return result
