"""Write a plain-text data quality report for one pipeline run."""

from datetime import datetime
from pathlib import Path


def write_quality_report(stats: dict, source_path: Path, report_path: Path) -> str:
    """Save the four required counts and return the same text for printing."""
    report_path.parent.mkdir(parents=True, exist_ok=True)

    accounted_for = (
        stats["valid_records"] + stats["rejected_records"] + stats["duplicate_records"]
    )
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = "\n".join(
        [
            "Customer Data ETL - Data Quality Report",
            "=======================================",
            f"Generated at: {generated_at}",
            f"Source file: {source_path}",
            "",
            f"Total records:     {stats['total_records']}",
            f"Valid records:     {stats['valid_records']}",
            f"Rejected records:  {stats['rejected_records']}",
            f"Duplicate records: {stats['duplicate_records']}",
            "",
            f"Check (valid + rejected + duplicates): {accounted_for}",
            "",
            "Valid records are loaded into the SQLite customers table.",
            "Rejected records fail a required field or the email check.",
            "Duplicate records repeat a customer_id. The first copy is kept.",
            "",
        ]
    )

    report_path.write_text(report, encoding="utf-8")
    return report
