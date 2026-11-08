"""File locations used by every step of the pipeline.

Keeping paths in one place means extract, transform, load, and the
quality report all read and write the same files.
"""

from pathlib import Path

# This file lives in src/, so the project root is one folder above it.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_CSV_PATH = PROJECT_ROOT / "data" / "raw" / "customers.csv"
CLEAN_CSV_PATH = PROJECT_ROOT / "data" / "processed" / "customers_clean.csv"
REJECTED_CSV_PATH = PROJECT_ROOT / "data" / "processed" / "customers_rejected.csv"
DATABASE_PATH = PROJECT_ROOT / "database" / "customers.db"
REPORT_PATH = PROJECT_ROOT / "reports" / "data_quality_report.txt"

TABLE_NAME = "customers"
